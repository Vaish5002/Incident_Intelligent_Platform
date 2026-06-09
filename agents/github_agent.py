from github import Github

def get_github_analysis(repo_url):

    try:
        # Example:
        # https://github.com/psf/requests
        parts = repo_url.rstrip("/").split("/")

        owner = parts[-2]
        repo_name = parts[-1]

        g = Github()

        repo = g.get_repo(f"{owner}/{repo_name}")

        commit = repo.get_commits()[0]

        files = commit.files

        changed_files = []

        for file in files:
            changed_files.append(file.filename)

        return {
            "commit_sha": commit.sha,
            "commit_message": commit.commit.message,
            "changed_files": changed_files,
            "commit_time": str(commit.commit.author.date)
        }

    except Exception as e:
        return {
            "error": str(e)
        }