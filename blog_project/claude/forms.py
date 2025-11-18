from django import forms

class JSONUploadForm(forms.Form):
    json_file = forms.FileField(label='JSON 파일 업로드')