from django.db import models
from core.models import Service, PlCoreBase, Slice, Instance, Tenant, TenantWithContainer, Node, Image, User, Flavor, NetworkParameter, NetworkParameterType, Port, AddressPool
from core.models.plcorebase import StrippedCharField
import os
from django.db import models, transaction
from django.forms.models import model_to_dict
from django.db.models import Q
from operator import itemgetter, attrgetter, methodcaller
from core.models import Tag
from core.models.service import LeastLoadedNodeScheduler
from services.volt.models import CordSubscriberRoot
import traceback
from xos.exceptions import *
from xos.config import Config
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class ConfigurationError(Exception):
    pass

VTR_KIND = "vTR"

CORD_USE_VTN = getattr(Config(), "networking_use_vtn", False)

# -------------------------------------------
# VOLT
# -------------------------------------------

class VTRService(Service):
    KIND = VTR_KIND

    class Meta:
        app_label = "vtr"

class VTRTenant(Tenant):
    KIND = VTR_KIND

    class Meta:
        app_label = "vtr"

    TEST_CHOICES = ( ("ping", "Ping"), ("traceroute", "Trace Route"), ("tcpdump", "Tcp Dump"), ("memory", "Memory"), ("bandwidth","Bandwidth") )
    SCOPE_CHOICES = ( ("container", "Container"), ("vm", "VM") )

    test = StrippedCharField(help_text="type of test", max_length=30, choices=TEST_CHOICES, null=False, blank=False)
    scope = StrippedCharField(help_text="scope of test", max_length=30, choices=SCOPE_CHOICES, null=False, blank=False)
    argument = StrippedCharField(max_length=40, null=True, blank=True)
    result = models.TextField(blank=True, null=True)
    result_code = StrippedCharField(max_length=32, blank=True, null=True)
    target_type = models.ForeignKey(ContentType)
    target_id = models.PositiveIntegerField()
    target = GenericForeignKey("target_type", "target_id")

    sync_attributes = ( 'test', 'argument', "scope" )

    def __init__(self, *args, **kwargs):
        vtr_services = VTRService.get_service_objects().all()
        if vtr_services:
            self._meta.get_field("provider_service").default = vtr_services[0].id
        super(VTRTenant, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(VTRTenant, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(VTRTenant, self).delete(*args, **kwargs)

