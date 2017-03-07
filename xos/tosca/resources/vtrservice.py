from xosresource import XOSResource
from service import XOSService
from core.models import Service, User, CoarseTenant
from services.vtr.models import VTRService

class XOSVTRService(XOSService):
    provides = "tosca.nodes.VTRService"
    xos_model = VTRService

