from dj_rest_auth.forms import AllAuthPasswordResetForm

from django.contrib.auth.tokens import default_token_generator
from allauth.account.utils import user_username

class CustomAllAuthPasswordResetForm(AllAuthPasswordResetForm):
    def save(self, request, **kwargs):
        email = self.cleaned_data['email']
        token_generator = kwargs.get('token_generator', default_token_generator)

        for user in self.users:
            temp_key = token_generator.make_token(user)
            username = user_username(user)
        
        return self.cleaned_data['email']
