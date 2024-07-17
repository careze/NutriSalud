from django import forms
from Apps.Crud.models import User, Categoria  

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all())

    class Meta:
        model = User  
        fields = ['email', 'nombre', 'apellido', 'edad', 'telefono', 'password', 'categoria']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
