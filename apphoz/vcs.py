from allauth.socialaccount.models import SocialAccount, SocialToken
from github import Github


class Vcs:
    sa = None
    st = None
    g = None

    def __init__(self, user):
        try:
            sa = SocialAccount.objects.get(user=user)
            st = SocialToken.objects.get(account=sa)
        except Exception as e:
            return None

        self.g = Github(st.token)

    @property
    def get_repos(self):
        return self.g.get_user().get_repos()
