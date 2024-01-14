import requests

def get_reponame__by_blueprint_id(api_endpoint, blueprint_id):
    api_url = f"{api_endpoint}/blueprints/{blueprint_id}"

    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            repo_found = False

            if 'plan' in data:
                # Iterate through the 'plans' to find the first dict with 'repoId' as that also has the repo name
                for plan_item in data['plan']:
                    for plugin in plan_item:
                        if 'options' in plugin:
                            options = plugin['options']
                            if 'repoId' in options:
                                # Save the name of the repository
                                repo_name = options['name']
                                repo_found = True
                                # Print repo name for extra info
                                print(f"Repo name: {repo_name}")
                                break

                    if repo_found:
                        return repo_name

        else:
            print(f"Error: Unable to fetch blueprints. Status Code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def create_github_issue(repo_owner, repo_name, access_token, issue_title):
    github_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
    headers = {
        'Authorization': f"Bearer {access_token}",
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'title': issue_title
    }

    try:
        response = requests.post(github_url, headers=headers, json=data)

        if response.status_code == 201:
            print(f"GitHub issue '{issue_title}' created successfully.")
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    
    api_endpoint = "http://54.236.25.78:4000/api"
    blueprint_id = 3

    # Fetch the first plugin repository name from the blueprint
    gitlab_repository_name = get_reponame__by_blueprint_id(api_endpoint, blueprint_id)

    # Create an issue if the above query is successfull
    if gitlab_repository_name:
        # Replace access token with your personal access token
        # NOTE: Should only be used this way for testing purposes
        repo_owner = "sh-eer"
        github_repo_name = "scripting-task"
        access_token = "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"
        issue_title = gitlab_repository_name

        # Create GitHub issue
        result = create_github_issue(repo_owner, github_repo_name, access_token, issue_title)

        # Print a confirmation link of the issue
        if result:
            print(f"Issue URL: {result['html_url']}")
