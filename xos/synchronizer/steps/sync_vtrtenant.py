import os
import socket
import sys
import base64
import time
from xos.config import Config
from synchronizers.new_base.SyncInstanceUsingAnsible import SyncInstanceUsingAnsible
from synchronizers.new_base.modelaccessor import *
#from services.vsg.models import VSGService, VCPE_KIND
#from services.vtr.models import VTRService, VTRTenant
#from services.volt.models import CordSubscriberRoot
from xos.logger import Logger, logging

# hpclibrary will be in steps/..
parentdir = os.path.join(os.path.dirname(__file__),"..")
sys.path.insert(0,parentdir)

logger = Logger(level=logging.INFO)

CORD_USE_VTN = getattr(Config(), "networking_use_vtn", False)

class SyncVTRTenant(SyncInstanceUsingAnsible):
    provides=[VTRTenant]
    observes=VTRTenant
    requested_interval=0
    template_name = "sync_vtrtenant.yaml"

    def __init__(self, *args, **kwargs):
        super(SyncVTRTenant, self).__init__(*args, **kwargs)

    def get_vtr_service(self, o):
        if not o.provider_service:
            return None

        vtrs = VTRService.objects.filter(id=o.provider_service.id)
        if not vtrs:
            return None

        return vtrs[0]

    def get_target(self, o):
        target = o.target
        if target:
            model_name = getattr(target, "model_name", target.__class__.__name__)
            # CordSubscriberRoot is a Proxy object, and o.target will point to
            # the base class... so fix it up.
            if model_name == "TenantRoot":
                target = CordSubscriberRoot.objects.get(id=target.id)
            return target
        return None

    def get_vcpe_service(self, o):
        target = self.get_target(o)
        if target and target.volt and target.volt.vcpe:
            vcpes = VSGService.objects.filter(id=target.volt.vcpe.provider_service.id)
            if not vcpes:
                return None
            return vcpes[0]
        return None

    def get_instance(self, o):
        target = self.get_target(o)
        if target and target.volt and target.volt.vcpe:
            return target.volt.vcpe.instance
        else:
            return None

    def get_key_name(self, instance):
#        if instance.slice.service and (instance.slice.service.kind==VCPE_KIND):
#            # We need to use the vsg service's private key. Onboarding won't
#            # by default give us another service's private key, so let's assume
#            # onboarding has been configured to add vsg_rsa to the vtr service.
#            return "/opt/xos/services/vtr/keys/vsg_rsa"

        if instance.slice and instance.slice.service and instance.slice.service.private_key_fn:
            # Assume the service has shared its key with VTR.
            # Look for the instance's service key name in VTR's key directory.
            service_keyfn = instance.slice.service.private_key_fn
            return os.path.join("/opt/xos/services/vtr/keys", os.path.basename(service_keyfn))
        else:
            raise Exception("VTR doesn't know how to get the private key for this instance")

    def get_extra_attributes(self, o):
        vtr_service = self.get_vtr_service(o)
        vcpe_service = self.get_vcpe_service(o)

        if not vcpe_service:
            raise Exception("No vcpeservice")

        instance = self.get_instance(o)

        if not instance:
            raise Exception("No instance")

        target = self.get_target(o)

        s_tags = []
        c_tags = []
        if target and target.volt:
            s_tags.append(target.volt.s_tag)
            c_tags.append(target.volt.c_tag)

        fields = {"s_tags": s_tags,
                "c_tags": c_tags,
                "isolation": instance.isolation,
                "container_name": "vcpe-%s-%s" % (s_tags[0], c_tags[0]),
#                "dns_servers": [x.strip() for x in vcpe_service.dns_servers.split(",")],
                "result_fn": "%s-vcpe-%s-%s" % (o.test, s_tags[0], c_tags[0]),
                "resultcode_fn": "code-%s-vcpe-%s-%s" % (o.test, s_tags[0], c_tags[0]) }

        # add in the sync_attributes that come from the vSG object
        # this will be wan_ip, wan_mac, wan_container_ip, wan_container_mac, ...
#        if target and target.volt and target.volt.vcpe:
#            for attribute_name in target.volt.vcpe.sync_attributes:
#                fields[attribute_name] = getattr(target.volt.vcpe, attribute_name)

        # add in the sync_attributes that come from the SubscriberRoot object
#        if target and hasattr(target, "sync_attributes"):
#            for attribute_name in target.sync_attributes:
#                fields[attribute_name] = getattr(target, attribute_name)

        for attribute_name in ["scope", "test", "argument"]: # o.sync_attributes:
            fields[attribute_name] = getattr(o,attribute_name)

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
