import pdfplumber

def extract_text_from_pdf(pdf_path):
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            all_text += page.extract_text()
    return all_text


# import pdfplumber

# def extract_text_from_pdf(pdf_path):
#     """Extracts text from a PDF file."""
#     all_text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             all_text += page.extract_text()
#     return all_text
