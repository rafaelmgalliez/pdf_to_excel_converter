import pdfplumber
from PIL import Image
import io

def parse_pdf(file):
    debug_images = []
    all_tables = []
    errors = []

    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text_table = page.extract_table()
                if text_table:
                    headers = text_table[0]
                    rows = text_table[1:]
                    all_tables.append((headers, rows))
                else:
                    errors.append("No table found on one of the pages.")

                img = page.to_image(resolution=150).original
                debug_images.append(img)
    except Exception as e:
        errors.append(str(e))

    return all_tables, debug_images, errors
