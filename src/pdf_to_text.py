import pdfplumber
import re

# def clean_text(text):
#     # Remove multiple spaces and newlines
#     cleaned_text = re.sub(r'\s+', ' ', text).strip()
#     # Additional cleaning logic can be added here
#     return cleaned_text

def extract_text_from_pdf(file_path):
    extracted_text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            extracted_text += page.extract_text()
    return extracted_text

# Provide the path to your PDF file
pdf_path = "src/documentation/darzalex_cmi.pdf"
text = extract_text_from_pdf(pdf_path)
# cleaned_text = clean_text(extracted_text)

# Save the extracted text to a file
with open("src/documentation/extracted_text.txt", "w", encoding="utf-8") as text_file:
    text_file.write(text)

print("Text extracted and saved to 'src/documentation/extracted_text.txt'")