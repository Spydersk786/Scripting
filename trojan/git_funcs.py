from github import Github
import base64

def connect():
    # Connect to the GitHub API using a personal access token
    with open("token.txt", "r") as f:
        token = f.read().strip()
    g = Github(token)
    repo = g.get_repo("Spydersk786/Scripting")
    return repo

def get_file_contents(dirname, module_name, repo):
    # Get the contents of a file from a GitHub repository
    try:
        repo = connect()
        contents = repo.get_contents(dirname + "/" + module_name)
        return base64.b64decode(contents.content).decode("utf-8")
    except Exception as e:
        print(f"Error getting file contents: {e}")
        return None