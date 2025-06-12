import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
# Fetch the API key from environment variables
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

    # For Gemini, the prompt structure might be slightly different for optimal results.
    # This is a starting point and might need refinement.
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
"""

    try:
        if not GEMINI_API_KEY: # Redundant check, but good for safety before API call
             return "Error: Gemini API key not configured. Cannot generate summary."

        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)

        # Check if the response has the expected parts and text
        if response.parts:
            # Assuming the relevant text is in the first part, adjust if necessary
            # based on Gemini API response structure.
            summary_text = response.text # Using .text directly if available and appropriate
        else:
            # Fallback or error if structure is not as expected
            # Try to access text via parts if .text is not directly available or suitable
            # This part might need adjustment based on actual Gemini API response object
            summary_text = ""
            for part in response.candidates[0].content.parts: # Example access pattern
                summary_text += part.text
            if not summary_text:
                print(f"Gemini API response might be empty or in unexpected format: {response.prompt_feedback}")
                return "Error: Could not extract summary from Gemini response. The response might be empty or in an unexpected format."


        return summary_text.strip()

    except Exception as e:
        print(f"An unexpected error occurred while generating summary with Gemini: {e}")
        # Check for specific Gemini API errors if the library provides them
        # For example, if hasattr(e, 'message'): return f"Error generating summary from Gemini: {e.message}"
        return f"Error: An unexpected error occurred while trying to generate the summary with Gemini: {str(e)}"

# Example usage (for testing purposes)
if __name__ == '__main__':
    if GEMINI_API_KEY:
        print("Attempting to generate a test summary with Gemini...")
        sample_jd = "We are looking for a software engineer with experience in Python, Flask, and REST APIs. The ideal candidate should have strong problem-solving skills and be a good team player."
        sample_resume = "Highly skilled Python developer with 5 years of experience in Flask and building RESTful APIs. Proven ability to solve complex problems and collaborate effectively with teams. Led a project that increased efficiency by 15%."

        # Configure genai here as well if running standalone for testing
        # genai.configure(api_key=GEMINI_API_KEY)

        summary = generate_summary(sample_resume, sample_jd)
        print("\nTest Gemini Summary:")
        print(summary)
    else:
        print("Skipping test Gemini summary generation as GEMINI_API_KEY is not set.")
