from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        
        user = super().save_user(request, user, form, False)

        profile_image = data.get("profile_image")
        nickname = data.get("nickname")
        introduce = data.get("introduce")
        auth_answer = data.get("auth_answer")
                
        if profile_image:
            user.profile_image = profile_image

        if nickname:
            user.nickname = nickname
        
        if introduce:
            user.introduce = introduce
        
        if auth_answer:
            user.auth_answer = auth_answer
        
        user.save()
        return user