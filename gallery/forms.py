from django import forms


class PhotoUploadForm(forms.Form):
    # title = forms.CharField(label='Title', max_length=130)
    file = forms.FileField()
