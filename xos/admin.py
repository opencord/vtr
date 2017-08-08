
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


from django.contrib import admin

from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from django.contrib.contenttypes import generic
from suit.widgets import LinkedSelect
from core.admin import ServiceAppAdmin,SliceInline,ServiceAttrAsTabInline, ReadOnlyAwareAdmin, XOSTabularInline, ServicePrivilegeInline
from core.middleware import get_request

from services.vtr.models import *
from services.rcord.models import CordSubscriberRoot

from functools import update_wrapper
from django.contrib.admin.views.main import ChangeList
from django.core.urlresolvers import reverse
from django.contrib.admin.utils import quote
from django.contrib.contenttypes.models import ContentType

class VTRServiceAdmin(ReadOnlyAwareAdmin):
    model = VTRService
    verbose_name = "vTR Service"
    verbose_name_plural = "vTR Service"
    list_display = ("backend_status_icon", "name", "enabled")
    list_display_links = ('backend_status_icon', 'name', )
    fieldsets = [(None, {'fields': ['backend_status_text', 'name','enabled','versionNumber', 'description',"view_url","icon_url" ], 'classes':['suit-tab suit-tab-general']})]
    readonly_fields = ('backend_status_text', )
    inlines = [SliceInline,ServiceAttrAsTabInline,ServicePrivilegeInline]

    extracontext_registered_admins = True

    user_readonly_fields = ["name", "enabled", "versionNumber", "description"]

    suit_form_tabs =(('general', 'vTR Service Details'),
        ('administration', 'Administration'),
        ('slices','Slices'),
        ('serviceattrs','Additional Attributes'),
        ('serviceprivileges','Privileges'),
    )

    suit_form_includes = (('vtradmin.html', 'top', 'administration'),
                           ) #('hpctools.html', 'top', 'tools') )

    def get_queryset(self, request):
        return VTRService.select_by_user(request.user)

class VTRTenantForm(forms.ModelForm):
    target = forms.ModelChoiceField(queryset=CordSubscriberRoot.objects.all())

    def __init__(self,*args,**kwargs):
        super (VTRTenantForm,self ).__init__(*args,**kwargs)
        self.fields['owner'].queryset = VTRService.objects.all()
        if self.instance:
            if self.instance.target_id:
                self.fields["target"].initial = CordSubscriberRoot.get_content_object(self.instance.target_type, self.instance.target_id)
        if (not self.instance) or (not self.instance.pk):
            if VTRService.objects.exists():
               self.fields["owner"].initial = VTRService.objects.all()[0]

    def save(self, commit=True):
        if self.cleaned_data.get("target"):
            self.instance.target_type = self.cleaned_data.get("target").get_content_type_key()
            self.instance.target_id = self.cleaned_data.get("target").id
        return super(VTRTenantForm, self).save(commit=commit)

    class Meta:
        model = VTRTenant
        fields = '__all__'

class VTRTenantAdmin(ReadOnlyAwareAdmin):
    list_display = ('backend_status_icon', 'id', 'target_type', 'target_id', 'test', 'argument' )
    list_display_links = ('backend_status_icon', 'id')
    fieldsets = [ (None, {'fields': ['backend_status_text', 'owner',
                                     'target', 'scope', 'test', 'argument', 'is_synced', 'result_code', 'result'],
                          'classes':['suit-tab suit-tab-general']})]
    readonly_fields = ('backend_status_text', 'service_specific_attribute', 'is_synced')
    form = VTRTenantForm

    suit_form_tabs = (('general','Details'),)

    def is_synced(self, obj):
        return (obj.enacted is not None) and (obj.enacted >= obj.updated)

    def get_queryset(self, request):
        return VTRTenant.select_by_user(request.user)

admin.site.register(VTRService, VTRServiceAdmin)
admin.site.register(VTRTenant, VTRTenantAdmin)

