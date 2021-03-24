from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

class ContentTypeRestrictedFileField(FileField):

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)
        max_upload_size = 524288

        file = data.file
        try:
            content_type = file.content_type
            print ('type: ', file.content_type)
            print('file size: ', file.size)
            if content_type in ['image/png', 'image/jpeg']:

                if file.size > max_upload_size:
                    raise forms.ValidationError(_('Please keep filesize under %s. Your file is  %s') % (filesizeformat(max_upload_size), filesizeformat(file.size)))
            else:
                raise forms.ValidationError(_('Filetype not supported.'))
        except AttributeError:
            pass

        return data
