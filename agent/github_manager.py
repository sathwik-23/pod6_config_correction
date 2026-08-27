import os

from github import Github
from git import Repo


class GithubManager:

    def __init__(self):

        self.token = os.getenv("GITHUB_TOKEN")
        self.repository_name = os.getenv(
            "GITHUB_REPOSITORY"
        )

    def create_branch(
        self,
        repo_path,
        branch_name
    ):

        print(f"Repo Path: {repo_path}")
        print(f"Creating Branch: {branch_name}")

        repo = Repo(repo_path)

        try:
            repo.git.checkout("main")
        except Exception as e:
            print(
                f"Failed to checkout main: {e}"
            )

        try:
            repo.git.pull("origin", "main")
        except Exception as e:
            print(
                f"Pull skipped: {e}"
            )

        try:
            repo.git.checkout(
                "-b",
                branch_name
            )
            print(
                f"Created branch {branch_name}"
            )

        except Exception:
            repo.git.checkout(branch_name)
            print(
                f"Using existing branch {branch_name}"
            )

        return repo

    def commit_changes(
        self,
        repo,
        message
    ):

        repo.git.add(A=True)

        if repo.is_dirty(untracked_files=True):

            repo.index.commit(message)

            print(
                f"Commit Created: {message}"
            )
        else:

            print(
                "No changes found to commit."
            )

    def push_branch(
        self,
        repo,
        branch
    ):

        origin = repo.remote(
            name="origin"
        )

        print(
            f"Pushing branch: {branch}"
        )

        origin.push(
            refspec=f"{branch}:{branch}"
        )

        print(
            "Push completed."
        )

    def create_pull_request(
        self,
        branch,
        title,
        body
    ):

        github = Github(self.token)

        repository = github.get_repo(
            self.repository_name
        )

        try:

            pr = repository.create_pull(
                title=title,
                body=body,
                head=branch,
                base="main"
            )

            print(
                f"PR Created: {pr.html_url}"
            )

            return pr.html_url

        except Exception as e:

            print(
                f"PR Creation Failed: {e}"
            )

            return None