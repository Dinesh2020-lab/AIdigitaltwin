from fastapi import FastAPI
from pydantic import BaseModel
from google import genai

app = FastAPI()

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
            "suggestion": result.get("suggestion", "No suggestion available")
        }

    except Exception as e:
        return {"error": str(e)}



    

    