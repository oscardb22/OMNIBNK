from crispy_forms.layout import Submit, Button, Layout, Field, HTML
from django import forms
from crispy_forms.helper import FormHelper
from .models import Users, Movie


class UsersForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Password')
    con_pass = forms.CharField(widget=forms.PasswordInput, required=True, label='Conf. Password')

    def clean(self):
        password = self.cleaned_data.get("password")
        con_pass = self.cleaned_data.get("con_pass")
        username = self.cleaned_data.get("username")

        if Users.objects.filter(username=username).exists():
            self.add_error('username', "This username exist")

        if con_pass != password:
            self.add_error('password', "Passwords dosn't match")

    class Meta:
        model = Users
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(UsersForm, self).__init__(*args, **kwargs)
        lay = Layout(
            'username', 'password', 'con_pass'
        )
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_group_wrapper_class = 'row clearfix'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-10 col-md-10 col-sm-8 form-control-label'
        self.helper.field_class = 'col-lg-10 col-md-10 col-sm-8'
        self.helper.add_input(Submit('submit', 'Enviar'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-default'))
        self.helper.layout = lay


class MovieForm(forms.ModelForm):
    def clean(self):
        title = self.cleaned_data.get("title")
        if Movie.objects.filter(title=title).exists():
            self.add_error('title', "This movie title exist")

    class Meta:
        model = Movie
        fields = ['title', 'recommended', 'picture']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(MovieForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_group_wrapper_class = 'row clearfix'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-10 col-md-10 col-sm-8 form-control-label'
        self.helper.field_class = 'col-lg-10 col-md-10 col-sm-8'
        self.helper.add_input(Submit('submit', 'Enviar'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-default'))
