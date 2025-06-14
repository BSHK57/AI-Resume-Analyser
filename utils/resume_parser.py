import pdfplumber
import docx2txt
from io import BytesIO
import os

def extract_text(file):
    text = ''
    filename = file.filename
    _, file_extension = os.path.splitext(filename)

    if file_extension.lower() == '.pdf':
        try:
            with pdfplumber.open(file.stream) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text: # Ensure text was extracted
                        text += page_text + "\n" # Add newline for readability
        except Exception as e:
            print(f"Error processing PDF file {filename}: {e}")
            return f"Error: Could not extract text from PDF {filename}."

    elif file_extension.lower() == '.docx':
        try:
            temp_stream = BytesIO(file.read())
            text = docx2txt.process(temp_stream)
        except Exception as e:
            print(f"Error processing DOCX file {filename}: {e}")
            return f"Error: Could not extract text from DOCX {filename}."
        finally:
            file.seek(0)  # Reset file pointer after reading
    else:
        print(f"Unsupported file type: {filename}")
        return f"Error: Unsupported file type {filename}. Please use PDF or DOCX."

    return text
