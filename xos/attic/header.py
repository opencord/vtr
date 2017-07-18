from django.db import models
from core.models import Service, XOSBase, Slice, Instance, ServiceInstance, TenantWithContainer, Node, Image, User, Flavor, NetworkParameter, NetworkParameterType, Port, AddressPool
from core.models.xosbase import StrippedCharField
import os
from django.db import models, transaction
from django.forms.models import model_to_dict
from django.db.models import *
from operator import itemgetter, attrgetter, methodcaller
import traceback
from xos.exceptions import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class ConfigurationError(Exception):
    # FIXME log the error
    pass

VTR_KIND = "vTR"
