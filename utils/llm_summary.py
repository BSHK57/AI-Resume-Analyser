import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY environment variable not set. Gemini summary will not be generated.")

def generate_summary(resume_text, jd_text, model_name="gemini-1.5-flash-latest"): # Default to gemini-pro
    """Generates a strengths/weaknesses summary using Google's Gemini model."""

    if not GEMINI_API_KEY:
        return "Error: Gemini API key not configured. Cannot generate summary."

    if not resume_text or not jd_text:
        return "Error: Resume text or Job Description text is missing. Cannot generate summary."
    prompt = f"""
You are an expert HR assistant. Your task is to analyze a resume against a job description.
Based on the provided job description and resume, please identify:
1. Three key strengths of the candidate that align well with the job description.
2. Two potential areas where the candidate's resume does not fully meet the job description's requirements or could be improved.

Present your analysis in a clear, concise, bullet-pointed format. Ensure each point starts with a bullet (e.g., * or -).

Job Description:
---
{jd_text}
---

Resume:
---
{resume_text}
---

Analysis (Strengths and Weaknesses):
(by mentioning the headings remove extralines without content)
"""

    try:
        if not GEMINI_API_KEY: # Redundant check, but good for safety before API call
             return "Error: Gemini API key not configured. Cannot generate summary."

        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)

        # Check if the response has the expected parts and text
        if response.parts:
            summary_text = response.text # Using .text directly if available and appropriate
        else:
            summary_text = ""
            for part in response.candidates[0].content.parts: # Example access pattern
                summary_text += part.text
            if not summary_text:
                print(f"Gemini API response might be empty or in unexpected format: {response.prompt_feedback}")
                return "Error: Could not extract summary from Gemini response. The response might be empty or in an unexpected format."


        return summary_text.strip()

    except Exception as e:
        print(f"An unexpected error occurred while generating summary with Gemini: {e}")
        return f"Error: An unexpected error occurred while trying to generate the summary with Gemini: {str(e)}"


def get_score(resume_text, jd_text, model_name="gemini-1.5-flash-latest"): # Default to gemini-pro
    if not GEMINI_API_KEY:
        return "Error: Gemini API key not configured. Cannot generate summary."

    if not resume_text or not jd_text:
        return "Error: Resume text or Job Description text is missing. Cannot generate summary."
    prompt = f"""
You are an expert HR assistant and resume analyst.
Your task is to evaluate how well the given resume aligns with the provided job description.
Instructions:
1. Carefully compare the resume content with the job description.
2. Consider all relevant aspects such as technical skills, experience, education, tools, certifications, and keywords.
3. Based on this analysis, calculate the percentage match between the resume and the job description.
Format: Only return a single numerical value (without any percentage symbol), representing the alignment score as a decimal (e.g., 85.75).
No explanation or extra text is required.
Job Description:
---
{jd_text}
---

Resume:
---
{resume_text}
---
"""

    try:
        if not GEMINI_API_KEY:
             return "Error: Gemini API key not configured. Cannot generate summary."

        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)

        if response.parts:
            summary_text = response.text
        else:
            summary_text = ""
            for part in response.candidates[0].content.parts: # Example access pattern
                summary_text += part.text
            if not summary_text:
                print(f"Gemini API response might be empty or in unexpected format: {response.prompt_feedback}")
                return "Error: Could not extract Score from Gemini response. The response might be empty or in an unexpected format."


        return summary_text.strip()

    except Exception as e:
        print(f"An unexpected error occurred while generating summary with Gemini: {e}")
        return f"Error: An unexpected error occurred while trying to generate the Score with Gemini: {str(e)}"