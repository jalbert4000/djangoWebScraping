from django import forms
	
class DeeplinkForm(forms.Form):
    #idcategoria = forms.CharField()
    idcategoria = forms.CharField(label='',required=False, widget=forms.TextInput
                                  (attrs=
                                        {'class': "form-control form-control-lg",
                                        'placeholder': "Ingresar el ID o lista de IDs"}))