from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class UserCreateForm(UserCreationForm):
    class Meta():
        model=get_user_model()
        fields=('username','first_name','last_name','email','password1','password2')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label='Student Id'
        # self.fields['first_name'].label='Name'
        self.fields['email'].label='Email Address'
