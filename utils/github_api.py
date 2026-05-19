import requests


def get_github_profile(username):

    url = f"https://api.github.com/users/{username}"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    return None


def get_user_repos(username):

    url = f"https://api.github.com/users/{username}/repos"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    return []