from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import MyUserChangeForm, MyUserCreationForm
from .models import MyUser
# Register your models here.


class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = MyUser
    list_display = ["username", "email", "age", "is_staff"]


# Регистрируем нашу модель для админ-интерфейса, который настроили выше
admin.site.register(MyUser, MyUserAdmin)
