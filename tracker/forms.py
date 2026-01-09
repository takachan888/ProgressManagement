from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Task


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["progress", "memo_today", "memo_next"]  # ✅ statusを消す
        widgets = {
            "progress": forms.NumberInput(attrs={
                "type": "range",
                "min": 0,
                "max": 100,
                "step": 1,
                "class": "form-range",
            }),
            "memo_today": forms.TextInput(attrs={"class": "form-control"}),
            "memo_next": forms.TextInput(attrs={"class": "form-control"}),
        }


class LeaderTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "owner", "role", "due_date", "points", "progress", "memo_today", "memo_next"]  # ✅ statusを消す
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "owner": forms.Select(attrs={"class": "form-select"}),
            "role": forms.TextInput(attrs={"class": "form-control"}),
            "due_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "points": forms.NumberInput(attrs={"min": 1, "class": "form-control"}),
            "progress": forms.NumberInput(attrs={
                "type": "range",
                "min": 0,
                "max": 100,
                "step": 1,
                "class": "form-range",
            }),
            "memo_today": forms.TextInput(attrs={"class": "form-control"}),
            "memo_next": forms.TextInput(attrs={"class": "form-control"}),
        }


class LeaderUserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label="パスワード", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="パスワード（確認）", widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["username", "email", "is_active"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            raise ValidationError("パスワードが一致しません。")
        if p1:
            validate_password(p1)
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user


class LeaderUserEditForm(forms.ModelForm):
    new_password1 = forms.CharField(
        label="新しいパスワード（任意）",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False
    )
    new_password2 = forms.CharField(
        label="新しいパスワード（確認）",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False
    )

    class Meta:
        model = User
        fields = ["email", "is_active"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("new_password1")
        p2 = cleaned.get("new_password2")
        if p1 or p2:
            if p1 != p2:
                raise ValidationError("新しいパスワードが一致しません。")
            validate_password(p1)
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        p1 = self.cleaned_data.get("new_password1")
        if p1:
            user.set_password(p1)
        if commit:
            user.save()
        return user
