import pymupdf


def validate_pdf_signature(file_path: str) -> bool:
    with open(file_path, "rb") as file:
        header = file.read(5)

    return header == b"%PDF-"


def extract_text_from_pdf(file_path: str) -> str:
    try:
        pdf = pymupdf.open(file_path)

        try:
            full_text = ""

            for page in pdf:
                full_text += page.get_text()

            return full_text

        finally:
            pdf.close()

    except pymupdf.FileDataError:
        raise ValueError("Unable to read the PDF file")