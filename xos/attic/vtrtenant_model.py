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

