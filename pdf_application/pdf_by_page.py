from PyPDF2 import PdfReader, PdfWriter


def extract_page_from_pdf(input_pdf_path, output_pdf_path, page_number):
    """
    Extracts a specific page from a PDF file and saves it as a new PDF file.
    
    :param input_pdf_path: Path to the input PDF file.
    :param output_pdf_path: Path to save the output PDF file.
    :param page_number: The page number to extract (0-indexed).
    """
    # Load the input PDF
    try:
        input_pdf = PdfReader(input_pdf_path)
    except FileNotFoundError:
        print(f"Error: Input PDF not found at {input_pdf_path}")
        exit()

    # Create a writer object
    writer = PdfWriter()

    # Add the specified page from the input PDF to the output PDF
    try:
        writer.add_page(input_pdf.pages[page_number-1])  # Add the specified page (0-indexed)
    except IndexError:
        print(f"Error: Page number {page_number} is out of range for the input PDF.")
        exit()

    # Write the output PDF
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)
    print(f"Page {page_number + 1} extracted successfully to {output_pdf_path}")