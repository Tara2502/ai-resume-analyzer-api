import pymupdf


def extract_text_from_pdf(file_path: str) -> str:
  try:  
    pdf = pymupdf.open(file_path)

    full_text = ""

    for page in pdf:
        full_text += page.get_text()

    pdf.close()

    return full_text
  
  except pymupdf.FileDataError:
     raise ValueError("Unable to read the pdf file.")
  