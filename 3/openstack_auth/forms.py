import logging

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_variables

from django.forms import ValidationError  # noqa
from django import http
#from django.utils.translation import ugettext_lazy as _  # noqa
#from django.views.decorators.debug import sensitive_variables  # noqa


from horizon import exceptions
from horizon import forms as hforms
from horizon import messages
from horizon.utils import validators

from openstack_dashboard import api

from .exceptions import KeystoneAuthException


LOG = logging.getLogger(__name__)


class Login(AuthenticationForm):
    """ Form used for logging in a user.

    Handles authentication with Keystone by providing the domain name, username
    and password. A scoped token is fetched after successful authentication.

    A domain name is required if authenticating with Keystone V3 running
    multi-domain configuration.

    If the user authenticated has a default project set, the token will be
    automatically scoped to their default project.

    If the user authenticated has no default project set, the authentication
    backend will try to scope to the projects returned from the user's assigned
    projects. The first successful project scoped will be returned.

    Inherits from the base ``django.contrib.auth.forms.AuthenticationForm``
    class for added security features.
    """
    region = forms.ChoiceField(label=_("Region"), required=False)
    username = forms.CharField(label=_("User Name"))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(render_value=False))
    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['username', 'password', 'region']
        if getattr(settings,
                   'OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT',
                    False):
            self.fields['domain'] = forms.CharField(label=_("Domain"),
                                                    required=True)
            self.fields.keyOrder = ['domain', 'username', 'password', 'region']
        self.fields['region'].choices = self.get_region_choices()
        if len(self.fields['region'].choices) == 1:
            self.fields['region'].initial = self.fields['region'].choices[0][0]
            self.fields['region'].widget = forms.widgets.HiddenInput()

    @staticmethod
    def get_region_choices():
        default_region = (settings.OPENSTACK_KEYSTONE_URL, "Default Region")
        return getattr(settings, 'AVAILABLE_REGIONS', [default_region])

    @sensitive_variables()
    def clean(self):
        default_domain = getattr(settings,
                                 'OPENSTACK_KEYSTONE_DEFAULT_DOMAIN',
                                 'Default')
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        region = self.cleaned_data.get('region')
        domain = self.cleaned_data.get('domain', default_domain)

        if not (username and password):
            # Don't authenticate, just let the other validators handle it.
            return self.cleaned_data

        try:
            self.user_cache = authenticate(request=self.request,
                                           username=username,
                                           password=password,
                                           user_domain_name=domain,
                                           auth_url=region)
            msg = 'Login successful for user "%(username)s".' % \
                {'username': username}
            LOG.info(msg)
        except KeystoneAuthException as exc:
            msg = 'Login failed for user "%(username)s".' % \
                {'username': username}
            LOG.warning(msg)
            self.request.session.flush()
            raise forms.ValidationError(exc)
        self.check_for_test_cookie()
        return self.cleaned_data




#add the function ---> user registration (form)
class BaseUserForm(hforms.SelfHandlingForm):
    def __init__(self, request, *args, **kwargs):
        super(BaseUserForm, self).__init__(request, *args, **kwargs)

        # Populate project choices
        project_choices = [('', _("Select a project"))]

        # If the user is already set (update action), list only projects which
        # the user has access to.
        user_id = kwargs['initial'].get('id', None)
        domain_id = kwargs['initial'].get('domain_id', None)
        projects, has_more = api.keystone.tenant_list(request,
                                                      domain=domain_id,
                                                      user=user_id)
        for project in projects:
            if project.enabled:
                project_choices.append((project.id, project.name))
        self.fields['project'].choices = project_choices

    def clean(self):
        '''Check to make sure password fields match.'''
        data = super(hforms.Form, self).clean()
        if 'password' in data:
            if data['password'] != data.get('confirm_password', None):
                raise ValidationError(_('Passwords do not match.'))
        return data



class CreateUserForm(BaseUserForm):
    # Hide the domain_id and domain_name by default
    domain_id = hforms.CharField(label=_("Domain ID"),
                                required=False,
                                widget=hforms.HiddenInput())
    domain_name = hforms.CharField(label=_("Domain Name"),
                                  required=False,
                                  widget=hforms.HiddenInput())
    name = hforms.CharField(label=_("User Name"))
    email = hforms.EmailField(
        label=_("Email"),
        required=False)
    password = hforms.RegexField(
        label=_("Password"),
        widget=hforms.PasswordInput(render_value=False),
        regex=validators.password_validator(),
        error_messages={'invalid': validators.password_validator_msg()})
    confirm_password = hforms.CharField(
        label=_("Confirm Password"),
        required=False,
        widget=hforms.PasswordInput(render_value=False))

 #registration : creat project named user's name while creat user , form hide this item
    project = hforms.ChoiceField(label=_("Primary Project"))
 #registration : role is default 'member', form hide this item
    role_id = hforms.ChoiceField(label=_("Role"))

    def __init__(self, *args, **kwargs):
#        roles = kwargs.pop('roles')
#        super(CreateUserForm, self).__init__(*args, **kwargs)
#        role_choices = [(role.id, role.name) for role in roles]
#        self.fields['role_id'].choices = role_choices

        # For keystone V3, display the two fields in read-only
        if api.keystone.VERSIONS.active >= 3:
            readonlyInput = hforms.TextInput(attrs={'readonly': 'readonly'})
            self.fields["domain_id"].widget = readonlyInput
            self.fields["domain_name"].widget = readonlyInput

    # We have to protect the entire "data" dict because it contains the
    # password and confirm_password strings.
    @sensitive_variables('data')
    def handle(self, request, data):
        domain = api.keystone.get_default_domain(self.request)
	
	#creat project named user's name

	cproject = api.keystone.tenant_create(request,
                                                     name=data['name'],
                                                     description='',
                                                     enabled=True,
                                                     domain=domain.id)	

        try:
            LOG.info('Creating user with name "%s"' % data['name'])
#creat user , write the data into database
            new_user = api.keystone.user_create(request,
                                                name=data['name'],
                                                email=data['email'],
                                                password=data['password'],
                                                project=cproject.id,
                                                enabled=True,
                                                domain=domain.id)
#display in the web
            messages.success(request,
                             _('User "%s" was successfully created  registered.')
                             % data['name'])
#if user is specified a role , then Adds a role for a user on a tenant.
            if data['role_id']:
                try:
                    api.keystone.add_tenant_user_role(request,
                                                      cproject.id,
                                                      new_user.id,
                                                      data['role_id'])
                except Exception:
                    exceptions.handle(request,
                                      _('Unable to add user '
                                        'to primary project.'))
            return new_user
        except Exception:
            exceptions.handle(request, _('Unable to create user.'))

