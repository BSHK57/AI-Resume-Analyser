import pdfplumber
import docx2txt
import os

def extract_text(path):
    text = ''
    _, file_extension = os.path.splitext(path)

    if file_extension.lower() == '.pdf':
        try:
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text: # Ensure text was extracted
                        text += page_text + "\n" # Add newline for readability
        except Exception as e:
            print(f"Error processing PDF file {path}: {e}")
            # Optionally, re-raise the exception or return a specific error message
            # raise e
            return f"Error: Could not extract text from PDF {os.path.basename(path)}."

    elif file_extension.lower() == '.docx':
        try:
            text = docx2txt.process(path)
        except Exception as e:
            print(f"Error processing DOCX file {path}: {e}")
            # Optionally, re-raise the exception or return a specific error message
            # raise e
            return f"Error: Could not extract text from DOCX {os.path.basename(path)}."
    else:
        print(f"Unsupported file type: {path}")
        return f"Error: Unsupported file type {os.path.basename(path)}. Please use PDF or DOCX."

    return text
