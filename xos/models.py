
from header import *


#from core.models.contenttype import ContentType 
from core.models import Tenant



#from core.models.service import Service
from core.models import Service






class VTRTenant(Tenant):

  KIND = 'vTR'

  class Meta:
      app_label = 'vtr'
      verbose_name = 'vTR Service Tenant'

  # Primitive Fields (Not Relations)
  test = StrippedCharField( choices = (('ping', 'Ping'), ('traceroute', 'Trace Route'), ('tcpdump', 'Tcp Dump'), ('memory', 'Memory'), ('bandwidth', 'Bandwidth')), max_length = 30, blank = False, help_text = "type of test", null = False, db_index = False )
  scope = StrippedCharField( choices = (('container', 'Container'), ('vm', 'VM')), max_length = 30, blank = False, help_text = "scope of test", null = False, db_index = False )
  argument = StrippedCharField( db_index = False, max_length = 40, null = True, blank = True )
  result = TextField( blank = True, null = True, db_index = False )
  result_code = StrippedCharField( db_index = False, max_length = 32, null = True, blank = True )
  target_id = IntegerField( blank = False, null = False, db_index = False )
  

  # Relations
  
  target_type = ForeignKey(ContentType, db_index = True, related_name = 'vtrtenant', null = False, blank = False )

  
  pass





class VTRService(Service):

  KIND = 'vTR'

  class Meta:
      app_label = 'vtr'
      verbose_name = 'vTR Service Service'

  # Primitive Fields (Not Relations)
  

  # Relations
  

  
  pass


