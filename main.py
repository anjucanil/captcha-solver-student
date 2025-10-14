# # main.py
# import os
# from dotenv import load_dotenv

# load_dotenv()

# STUDENT_SECRET = os.getenv("STUDENT_SECRET")
# print("Loaded secret:", STUDENT_SECRET)
# from fastapi import FastAPI, Request, HTTPException
# from pydantic import BaseModel
# import os
# from llm_generator import generate_codebase
# #from deployer_github import deploy_to_github
# from github_deployer import get_or_create_repo, push_file, enable_pages


# from utils import verify_secret, save_attachments, notify_evaluator

# app = FastAPI()

# class TaskRequest(BaseModel):
#     email: str
#     secret: str
#     task: str
#     round: int
#     nonce: str
#     brief: str
#     checks: list
#     evaluation_url: str
#     attachments: list

# @app.post("/receive-task")
# async def receive_task(request: TaskRequest):
#     # 1. Verify secret
#     if not verify_secret(request.email, request.secret):
#         raise HTTPException(status_code=403, detail="Invalid secret.")

#     # 2. Save attachments (e.g., sample.png)
#     save_attachments(request.attachments, request.task)

#     # 3. Generate codebase using LLM
#     repo_dir = generate_codebase(request)

#     # 4. Deploy to GitHub
#     repo_url, commit_sha, pages_url = deploy_to_github(request.task, repo_dir)

#     # 5. Notify evaluator
#     success = notify_evaluator(request.evaluation_url, {
#         "email": request.email,
#         "task": request.task,
#         "round": request.round,
#         "nonce": request.nonce,
#         "repo_url": repo_url,
#         "commit_sha": commit_sha,
#         "pages_url": pages_url
#     })

#     return {"status": "success"} if success else {"status": "partial"}
# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import asyncio
from utils import verify_secret
from llm_generator import build_app, update_app
from github_deployer import deploy_to_github, redeploy_to_github
from utils import post_evaluation

app = FastAPI()

@app.post("/api-endpoint")
async def handle_request(request: Request):
    data = await request.json()

    # 1️⃣ Verify secret
    if not verify_secret(data.get("secret")):
        return JSONResponse(status_code=403, content={"error": "Invalid secret"})

    round_no = data.get("round", 1)
    email = data.get("email")
    task = data.get("task")
    nonce = data.get("nonce")
    evaluation_url = data.get("evaluation_url")

    # 2️⃣ Send immediate acknowledgement
    response = {"status": "ok", "round": round_no}
    asyncio.create_task(process_round(data))   # run asynchronously
    return JSONResponse(status_code=200, content=response)


async def process_round(data: dict):
    """Do heavy work in the background."""
    round_no = data["round"]
    task = data["task"]
    evaluation_url = data["evaluation_url"]

    if round_no == 1:
        # 🏗️ Build phase
        app_files = await build_app(data)  # use your LLM generator
        repo_url, commit_sha, pages_url = await deploy_to_github(task, app_files)
    elif round_no == 2:
        # 🔁 Revise phase
        app_files = await update_app(data)  # modify existing app
        repo_url, commit_sha, pages_url = await redeploy_to_github(task, app_files)
    else:
        print(f"Unknown round {round_no}")
        return

    # 📤 Notify evaluator
    payload = {
        "email": data["email"],
        "task": data["task"],
        "round": round_no,
        "nonce": data["nonce"],
        "repo_url": repo_url,
        "commit_sha": commit_sha,
        "pages_url": pages_url,
    }
    await post_evaluation(evaluation_url, payload)    
    return JSONResponse(status_code=200, content={"status": "ok", "round": round_no})
