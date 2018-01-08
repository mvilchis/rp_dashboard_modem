from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

############### My libraries ########################
from .models import NormalUser
from .models import ManagerUser

################ Custom admin form ##################
class UserCreationForm(forms.ModelForm):
     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
     password2 = forms.CharField(label='Repetir password', widget=forms.PasswordInput)
     class Meta:
         model = NormalUser
         fields = ('email',
                     'username',
                     'org',
                     'is_active',
                     'is_admin',

                     )
     def save(self, commit=True):
         user = super(UserCreationForm, self).save(commit=False)
         user.set_password(self.cleaned_data["password1"])
         if commit:
             user.save()
         return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = NormalUser
        fields = ('email',
                     'username',
                     'org',
                     'is_active',
                     'is_admin',
                 )
    def clean_password(self):
         return self.initial["password"]

class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email','username')
    list_filter = ('username','email')
    ordering = ('username',)
    fieldsets = (
         (None, {'fields': ('email', 'password','username','org')}),
         ('Permisos', {'fields': ('is_admin', 'is_active',)}),
     )

    add_fieldsets = ( (None, {'classes': ('wide',),
                               'fields': ('email',
                                          'username',
                                          'org',
                                          'password1',
                                          'password2',
                                          'is_active',
                                          'is_admin')
                               }),)
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

admin.site.register(NormalUser, MyUserAdmin)
admin.site.register(ManagerUser)
