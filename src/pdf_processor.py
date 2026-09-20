import pymupdf


def extract_text_from_pdf(pdf_file):
    """
    Extract text from an uploaded PDF file.
    """

    pdf_document = pymupdf.open(stream=pdf_file.read(), filetype="pdf")

    extracted_text = ""

    for page in pdf_document:
        page_text = page.get_text()
        extracted_text += page_text + "\n"

    pdf_document.close()

    return extracted_text