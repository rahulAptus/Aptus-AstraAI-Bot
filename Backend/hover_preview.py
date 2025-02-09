from fastapi import FastAPI, HTTPException
import requests
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import os
load_dotenv(override=True)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust based on frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/get-link-preview")
def get_link_preview(url: str):
    api_url = 'https://api.linkpreview.net'
    LINK_PREVIEW_API_KEY = "33ad4733a63698696d907377277358e7"
    target = url
    try:
        response = requests.get(
            api_url,
            headers={'X-Linkpreview-Api-Key':  LINK_PREVIEW_API_KEY},
            params={'q': target},
        )
        data = response.json()
        print (data)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
