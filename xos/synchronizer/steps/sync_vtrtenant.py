
# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import socket
import sys
import base64
import time
from synchronizers.new_base.SyncInstanceUsingAnsible import SyncInstanceUsingAnsible
from synchronizers.new_base.modelaccessor import *
from xos.logger import Logger, logging

# hpclibrary will be in steps/..
parentdir = os.path.join(os.path.dirname(__file__),"..")
sys.path.insert(0,parentdir)

logger = Logger(level=logging.INFO)

class SyncVTRTenant(SyncInstanceUsingAnsible):
    provides=[VTRTenant]
    observes=VTRTenant
    requested_interval=0
    template_name = "sync_vtrtenant.yaml"

    def __init__(self, *args, **kwargs):
        super(SyncVTRTenant, self).__init__(*args, **kwargs)

    def get_vtr_service(self, o):
        if not o.owner:
            return None

        # cast from Service to VTRService
        vtrs = VTRService.objects.filter(id=o.owner.id)
        if not vtrs:
            return None

        return vtrs[0]

    def get_target(self, o):
        target = o.target
        if target:
            model_name = getattr(target, "model_name", target.__class__.__name__)
            if model_name in ["ServiceInstance", "CordSubscriberRoot"]:
                # cast from ServiceInstance to CordSubscriberRoot
                csrs = CordSubscriberRoot.objects.filter(id=target.id)
                if csrs:
                    return csrs[0]
        return None

    def gather_information(self, service_instance):
        """ gather_information: inspect a service chain for information that will be useful to the VTN service, and
            try to do it in a service-agnostic way. We know what we're looking for (instances, ip addresses, etc) but
            not necessarily where we will find it.
        """

        if not service_instance:
            return {}

        # extract useful information from the service_instance
        info = {}
        for link in service_instance.subscribed_links.all():
            provider_si = link.provider_service_instance.leaf_model
            for k in ["instance", "wan_vm_ip", "wan_container_ip", "s_tag", "c_tag", "container_name"]:
                if hasattr(provider_si, k):
                    info[k] = getattr(provider_si, k)

        # now, recurse to check the children
        for link in service_instance.subscribed_links.all():
            child_info = self.gather_information(link.provider_service_instance)

            # prefer values we got from a parent to values we got from a child
            for (k,v) in child_info.items():
                if not k in info:
                    info[k] = v

        return info

    def get_instance(self, o):
        """ get_instance: Called by the SyncInstanceUsingAnslbe sync step. """
        return self.gather_information(self.get_target(o)).get("instance")

    def get_key_name(self, instance):
        if instance.slice and instance.slice.service and instance.slice.service.private_key_fn:
            # Assume the service has shared its key with VTR.
            # Look for the instance's service key name in VTR's key directory.
            service_keyfn = instance.slice.service.private_key_fn
            return os.path.join("/opt/xos/services/vtr/keys", os.path.basename(service_keyfn))
        else:
            raise Exception("VTR doesn't know how to get the private key for this instance")

    def get_extra_attributes(self, o):
        target = self.get_target(o)
        target_info = self.gather_information(target)

        instance = target_info.get("instance")
        if not instance:
            raise Exception("No instance")

        # For container scope, we need to figure out the container name. There are three ways we can do this:
        #    1) The service_instance can provide a `container_name` attribute
        #    2) The service_instance can provide `container_prefix`, `s_tag`, and `c_tag` attributes.
        #    3) The service_instance can provide `s_tag` and `c_tag` and we'll assume a default prefix of `vsg`
        container_name = target_info.get("container_name")
        if not container_name:
            if (not target_info.get("s_tag")) or (not target_info.get("c_tag")):
                raise Exception("No s_tag or no c_tag")

            container_name = "%s-%s-%s" % (target_info.get("container_prefix", "vsg"), target_info["s_tag"], target_info["c_tag"])

        fields = {"isolation": instance.isolation,
                  "container_name": container_name,
                  "result_fn": "%s-vtrserviceinstance-%s" % (o.test, str(o.id)),
                  "resultcode_fn": "code-%s-vtrserviceinstance-%s" % (o.test, str(o.id)) }

        # copy in values that we learned from inspecting the service chain
        for k in ["s_tag", "c_tag", "wan_vm_ip", "wan_container_ip"]:
            if target_info.get(k):
                fields[k] = target_info[k]

        for attribute_name in ["scope", "test", "argument"]: 
            fields[attribute_name] = getattr(o, attribute_name)

        return fields

    def sync_fields(self, o, fields):
        # the super causes the playbook to be run

        super(SyncVTRTenant, self).sync_fields(o, fields)

    def run_playbook(self, o, fields):
        o.result = ""

        result_fn = os.path.join("/opt/xos/synchronizers/vtr/result", fields["result_fn"])
        if os.path.exists(result_fn):
            os.remove(result_fn)

        resultcode_fn = os.path.join("/opt/xos/synchronizers/vtr/result", fields["resultcode_fn"])
        if os.path.exists(resultcode_fn):
            os.remove(resultcode_fn)

        super(SyncVTRTenant, self).run_playbook(o, fields)

        if os.path.exists(result_fn):
            o.result = open(result_fn).read()

        if os.path.exists(resultcode_fn):
            o.result_code = open(resultcode_fn).read()


    def delete_record(self, m):
        pass
