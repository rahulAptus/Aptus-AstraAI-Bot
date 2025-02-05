
from openai import OpenAI

def moderation(query):
    print("[INFO]: Checking for harmful query")
    try:
        client = OpenAI()
        response = client.moderations.create(input=query)
        return response.results[0].flagged
    except Exception as e:
        print(f"[ERROR]: While performing OpenAI moderation {e}")

    return None