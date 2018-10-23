from github import Github
from .github_payload import *


class Vcs:
    g = None

    def __init__(self):
        g = Github(payload.access_token)
