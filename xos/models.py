from header import *



from core.models import ContentType#from core.models.tenant import Tenant
from core.models import Tenant



#from core.models.service import Service
from core.models import Service





class VTRTenant(Tenant):

  KIND = "vTR"

  class Meta:
      app_label = "vtr"
      name = "vtr"
      verbose_name = "Virtual Truck Roll Service"

  # Primitive Fields (Not Relations)
  test = StrippedCharField( choices = (('ping', 'Ping'), ('traceroute', 'Trace Route'), ('tcpdump', 'Tcp Dump'), ('memory', 'Memory'), ('bandwidth', 'Bandwidth')), max_length = 30, blank = False, help_text = "type of test", null = False, db_index = False )
  scope = StrippedCharField( choices = (('container', 'Container'), ('vm', 'VM')), max_length = 30, blank = False, help_text = "scope of test", null = False, db_index = False )
  argument = StrippedCharField( db_index = False, max_length = 40, null = True, blank = True )
  result = TextField( blank = True, null = True, db_index = False )
  result_code = StrippedCharField( db_index = False, max_length = 32, null = True, blank = True )
  target_id = IntegerField( blank = False, null = False, db_index = False )
  

  # Relations
  
  target_type = ForeignKey(ContentType, db_index = True, related_name = 'vtrtenant', null = False, blank = False )

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
  
  pass




class VTRService(Service):

  KIND = "vTR"

  class Meta:
      app_label = "vtr"
      name = "vtr"
      verbose_name = "Virtual Truck Roll Service"

  # Primitive Fields (Not Relations)
  

  # Relations
  

  
  pass


