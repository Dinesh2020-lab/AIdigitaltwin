from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all (for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="../frontend", html=True), name="frontend")


@app.get("/")
def serve_home():
    return FileResponse("../frontend/index.html")

client = genai.Client(api_key="")


class PatientData(BaseModel):
    pressure: int
    flow: int
    time: int


@app.post("/analyze")
def analyze(data: PatientData):
    try:
        prompt = f"""
You are an expert medical AI monitoring a dialysis machine in real-time.

Patient Parameters:
- Pressure: {data.pressure} mmHg
- Blood Flow: {data.flow} ml/min
- Dialysis Time: {data.time} minutes

Rules:
- High Risk: Pressure > 170 OR Flow < 200 OR abnormal combination
- Medium Risk: Slight deviation from normal ranges
- Low Risk: All parameters within safe range

Respond ONLY in this strict JSON format:
{{
  "risk": "LOW / MEDIUM / HIGH",
  "issue": "short issue description",
  "suggestion": "clear medical recommendation"
}}
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        text = response.text.strip()

        #  Convert AI text → JSON safely
        import json

        try:
            result = json.loads(text)
        except:
            # fallback if Gemini adds extra text
            text = text[text.find("{"):text.rfind("}")+1]
            result = json.loads(text)

        return {
    "risk": result.get("risk", "UNKNOWN"),
    "suggestion": result.get("suggestion", "No suggestion available"),
    "source": "AI"
}

    except Exception as e:

        if data.pressure > 170 or data.flow < 200:
         return {
            "risk": "HIGH",
            "suggestion": "Critical condition. Adjust machine immediately.",
            "source": "FALLBACK"
        }

        elif data.pressure > 140:
         return {
            "risk": "MEDIUM",
            "suggestion": "Patient needs monitoring.",
            "source": "FALLBACK"
        }

    else:
        return {
            "risk": "LOW",
            "suggestion": "All parameters are normal.",
            "source": "FALLBACK"
        }

