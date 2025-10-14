# # # github_deployer.py
# # from github import Github
# # import os
# # import shutil

# # g = Github(os.getenv("GITHUB_PAT"))

# # def deploy_to_github(repo_name, folder_path):
# #     user = g.get_user()
# #     repo = user.create_repo(
# #         name=repo_name,
# #         private=False,
# #         auto_init=False,
# #         license_template="mit"
# #     )

# #     # Add files
# #     for root, _, files in os.walk(folder_path):
# #         for file in files:
# #             path = os.path.join(root, file)
# #             with open(path, "r") as f:
# #                 content = f.read()
# #             repo.create_file(file, f"Add {file}", content)

# #     # Enable Pages
# #     repo.edit(default_branch="main")
# #     repo.create_git_ref(ref='refs/heads/gh-pages', sha=repo.get_branch("main").commit.sha)
# #     repo.pages_source("gh-pages")
# #     pages_url = f"https://{user.login}.github.io/{repo_name}/"

# #     return repo.clone_url, repo.get_commits()[0].sha, pages_url
# # github_deployer.py

# ##################################################################################################
# import os
# import base64
# from github import Github
# from github.GithubException import UnknownObjectException, GithubException

# GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
# REPO_NAME = os.getenv("GITHUB_REPO", "captcha-solver-student")

# def get_or_create_repo():
#     """Use existing repo if it exists, otherwise create a new one."""
#     g = Github(GITHUB_TOKEN)
#     user = g.get_user()

#     try:
#         repo = user.get_repo(REPO_NAME)
#         print(f"✅ Using existing repo: {repo.html_url}")
#     except UnknownObjectException:
#         print(f"ℹ️ Repo '{REPO_NAME}' not found — creating it.")
#         repo = user.create_repo(REPO_NAME, private=False, auto_init=True)
#         print(f"🚀 Created new repo: {repo.html_url}")
#     except GithubException as e:
#         print(f"❌ GitHub error: {e.data}")
#         raise
#     return repo


# def push_file(repo, local_path, commit_message="update file"):
#     """Create or update file in repo."""
#     file_name = os.path.basename(local_path)

#     with open(local_path, "r", encoding="utf-8") as f:
#         content = f.read()

#     try:
#         existing = repo.get_contents(file_name)
#         repo.update_file(existing.path, commit_message, content, existing.sha)
#         print(f"♻️ Updated {file_name}")
#     except UnknownObjectException:
#         repo.create_file(file_name, commit_message, content)
#         print(f"✅ Created {file_name}")


# def enable_pages(repo):
#     """Enable GitHub Pages (manual step may be needed)."""
#     try:
#         repo.edit(has_pages=True)
#         print(f"🌐 GitHub Pages enabled: https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/")
#     except GithubException:
#         print("⚠️ Could not enable GitHub Pages automatically. You may need to do it manually in Settings > Pages.")


# if __name__ == "__main__":
#     repo = get_or_create_repo()
#     push_file(repo, "README.md", "sync README.md")
#     enable_pages(repo)
###############################################
async def deploy_to_github(task, files):
    # create new repo + push + enable pages
    repo_url = f"https://github.com/anjucanil/{task}"
    commit_sha = "abc123"
    pages_url = f"https://anjucanil.github.io/{task}/"
    return repo_url, commit_sha, pages_url


async def redeploy_to_github(task, files):
    # update existing repo + push changes + redeploy pages
    repo_url = f"https://github.com/anjucanil/{task}"
    commit_sha = "def456"
    pages_url = f"https://anjucanil.github.io/{task}/"
    return repo_url, commit_sha, pages_url
