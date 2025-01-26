from django import forms
from .models import User



class UserRegistrationForm(forms.ModelForm):
    password=forms.CharField(max_length=20, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='پسورد')
    password2=forms.CharField(max_length=20, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='تکرار پسورد')

    class Meta:
        model= User
        fields=['username','email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),
                'email': forms.TextInput(attrs={
                    'class': 'form-control',
            }),
        }
        labels = {
            'username': 'نام کاربری',
            'email': 'ایمیل',

        }
    
    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('پسورد ها با هم مطابقت ندارند')
        return cd['password2']
    
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('این ایمیل قبلا ثبت شده است!')
        return email


