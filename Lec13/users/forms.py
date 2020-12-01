# Это именно низкоуровневые интерфейсы взаимодействия с моделью
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import MyUser

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser 
        fields = UserCreationForm.Meta.fields + ('age',)

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = MyUser
        fields = UserChangeForm.Meta.fields # допишу что понадобится