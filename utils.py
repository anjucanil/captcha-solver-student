# # utils.py
# import requests
# import base64
# import os

# def verify_secret(email, secret):
#     # Replace with your actual secret lookup
#     expected = os.getenv("STUDENT_SECRET")
#     return secret == expected

# def save_attachments(attachments, task_id):
#     os.makedirs(f"repos/{task_id}/assets", exist_ok=True)
#     for att in attachments:
#         data = att["url"].split(",")[1]
#         decoded = base64.b64decode(data)
#         with open(f"repos/{task_id}/assets/{att['name']}", "wb") as f:
#             f.write(decoded)

# def notify_evaluator(url, payload):
#     try:
#         response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
#         return response.status_code == 200
#     except Exception as e:
#         return False
import os, aiohttp, asyncio
from dotenv import load_dotenv
load_dotenv()

STUDENT_SECRET = os.getenv("STUDENT_SECRET")

def verify_secret(secret: str) -> bool:
    return secret == STUDENT_SECRET


async def post_evaluation(url: str, payload: dict, retries: int = 5):
    delay = 1
    async with aiohttp.ClientSession() as session:
        for i in range(retries):
            try:
                async with session.post(url, json=payload) as resp:
                    if resp.status == 200:
                        print("✅ Evaluation notified successfully.")
                        return True
                    else:
                        print(f"Attempt {i+1}: got {resp.status}")
            except Exception as e:
                print(f"Attempt {i+1} failed: {e}")
            await asyncio.sleep(delay)
            delay *= 2
    print("❌ Failed to notify evaluation API after retries.")
    return False
