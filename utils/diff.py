import requests
import json


def diff_url(pr_number: int):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    # TODO: Should be user input
    pr_url = f"https://api.github.com/repos/aiplanethub/genai-stack/pulls/{pr_number}"
    response = requests.get(pr_url, headers=headers)
    res = json.loads(response.text)

    return res["diff_url"]
