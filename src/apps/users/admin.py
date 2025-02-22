from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.users.models import User
from django import forms
from django.utils.translation import gettext_lazy as _


class CustomUserChangeForm(forms.ModelForm):
    new_password = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput,
        required=False,
        help_text=_("Введите новый пароль, если хотите его изменить."),
    )

    class Meta:
        model = User
        fields = ('username', 'new_password')

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password")
        if new_password:
            user.set_password(new_password)  # Хешируем новый пароль
        if commit:
            user.save()
        return user


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    list_display = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'new_password')}),
        # ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    def save_model(self, request, obj, form, change):
        """Если введён новый пароль, хешируем его перед сохранением."""
        if form.cleaned_data.get("new_password"):
            obj.set_password(form.cleaned_data["new_password"])
        obj.save()
