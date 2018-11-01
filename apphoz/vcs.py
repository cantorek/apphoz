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
            self.g = Github(st.token)
        except Exception as e:
            self.g = Github('')
            return None


    @property
    def get_repos(self):
        return self.g.get_user().get_repos()

    def get_repo(self, repo_id):
        return self.g.get_repo(repo_id)

    def get_github(self):
        return self.g
