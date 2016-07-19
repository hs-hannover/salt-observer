from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext, ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field, HTML, Fieldset
from crispy_forms.bootstrap import StrictButton, PrependedText


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.error_messages.update({
            'invalid_login': _(
                'Please enter a corrent %(username)s and password. '
                'Note that these credentials must be a valid api user!'
            )
        })

        self.fields['username'].widget.attrs.update({'autofocus': 'True'})
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = ''
        self.helper.field_class = 'col-lg-12'

        self.helper.layout = Layout(
            PrependedText('username', '<i class="fa fa-user fa-fw"></i>', placeholder='Username'),
            PrependedText('password', '<i class="fa fa-unlock-alt fa-fw"></i>', placeholder='Password'),
            Div(
                Div(
                    StrictButton('Login', type='submit', css_class='btn-default'),
                    css_class='col-lg-12',
                ),
                css_class='form-group'
            )
        )

    username = forms.CharField(label='', max_length=255)
    password = forms.CharField(label='', widget=forms.PasswordInput)
