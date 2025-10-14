# # llm_generator.py
# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# AIPIPE_TOKEN = os.getenv("AIPIPE_TOKEN")  # or whatever name you use in .env
# if not AIPIPE_TOKEN:
#     raise RuntimeError("AIPIPE_TOKEN not set in .env")

# AI_PIPE_CHAT_URL = "https://aipipe.org/openrouter/v1/chat/completions"

# def generate_codebase(request):
#     prompt = f"""
# Brief: {request.brief}
# Checks: {request.checks}
# """
#     header = {
#         "Authorization": f"Bearer {AIPIPE_TOKEN}",
#         "Content-Type": "application/json"
#     }
#     body = {
#         "model": "gpt-3.5-turbo",
#         "messages": [
#             {"role": "system", "content": "You are a code generation assistant."},
#             {"role": "user", "content": prompt}
#         ]
#     }

#     resp = requests.post(AI_PIPE_CHAT_URL, json=body, headers=header)
#     if resp.status_code != 200:
#         raise RuntimeError(f"AI Pipe error: {resp.status_code} {resp.text}")

#     data = resp.json()
#     # The response format should have something like data["choices"][0]["message"]["content"]
#     generated = data["choices"][0]["message"]["content"]

#     # Now write the code files
#     repo_dir = f"repos/{request.task}"
#     os.makedirs(repo_dir, exist_ok=True)
#     with open(f"{repo_dir}/index.html", "w") as f:
#         f.write(generated)

#     return repo_dir
async def build_app(request_data):
    """
    Use the brief + attachments to create initial app files.
    Returns a dict {filename: content}.
    """
    brief = request_data["brief"]
    # call your LLM here
    return {"index.html": "<h1>Hello Round 1!</h1>"}


async def update_app(request_data):
    """
    Modify existing repo code based on new brief.
    """
    brief = request_data["brief"]
    # call your LLM again with the repo context
    return {"index.html": "<h1>Updated for Round 2!</h1>"}
