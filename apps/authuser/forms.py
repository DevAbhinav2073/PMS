from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from apps.course.models import Stream
from apps.student.models import StudentProxyModel
import string
import random

from apps.system.email_sending_utils import send_account_creation_email

User = get_user_model()


def pw_gen(size=8, chars=string.ascii_letters + string.digits + string.punctuation):
    return ''.join(random.choice(chars) for _ in range(size))


class NewStudentCreateForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    roll_number = forms.CharField(required=True)
    stream = forms.ModelChoiceField(queryset=Stream.objects.all())

    def is_valid(self):
        if not self.data._mutable:
            self.data._mutable = True
        password = pw_gen()
        self.data['password1'] = password
        self.data['password2'] = password
        is_valid = super().is_valid()
        if is_valid:
            send_account_creation_email(self.data, password)
        return is_valid

    class Meta:
        model = StudentProxyModel
        fields = ('first_name', 'last_name', 'username', 'roll_number', 'stream')


class StudentChangeForm(UserChangeForm):
    class Meta:
        model = StudentProxyModel
        fields = ()
