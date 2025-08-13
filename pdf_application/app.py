import logger
import os
import exception
import ocrmypdf # type: ignore
from image_handling_pdf_co import uploadFile, makeSearchablePDF
from image_classification import classify_image
from pdf2image import convert_from_path
from pdf_by_page import extract_page_from_pdf

logger = logger.get_logger(__name__)
logger.info("Starting the PDF Application...")


def process_pdf(input_pdf: str, output_pdf: str) -> None:
    """
    Processes the input PDF file and saves the output PDF file.
    """
    try:
        logger.info("Starting OCRMYPDF processing...")
        if not os.path.exists(input_pdf):
            raise exception.AppException(f"Input PDF file does not exist: {input_pdf}")

        logger.info(f"Processing PDF: {input_pdf}")
        ocrmypdf.ocr(input_pdf, output_pdf, deskew=True, force_ocr=True)
        logger.info(f"Processed PDF saved as: {output_pdf}")

    except ocrmypdf.exceptions.OCRmyPDFError as e:
        raise exception.AppException("OCR processing failed.", original_exception=e)
    except Exception as e:
        raise exception.AppException("An unexpected error occurred.", original_exception=e)


def image_processing(input_pdf: str, output_pdf: str) -> None:
    """
    Processes the input PDF file and saves the output PDF file with image handling.
    """
    try:
        if not os.path.exists(input_pdf):
            raise exception.AppException(f"Input PDF file does not exist: {input_pdf}")

        logger.info(f"Processing images in PDF: {input_pdf}")
        uploadedFileUrl = uploadFile(input_pdf)
        if (uploadedFileUrl != None):
            makeSearchablePDF(uploadedFileUrl, output_pdf)
        logger.info(f"Processed images saved as: {output_pdf}")
    except Exception as e:
        raise exception.AppException("An unexpected error occurred.", original_exception=e)
    
if __name__ == "__main__":
    input_pdf = r"C:\Nandeesh\freelance_project\document\Q067_5-6-08_ARI_rotated_100.pdf"
    # fetch the file name from the path
    output_pdf_ocrmypdf = fr"ocrmypdf\{os.path.basename(input_pdf)[:-5]}_ocrmypdf.pdf"   # Replace with your desired output PDF file path

    # Process the PDF using OCRmyPDF
    process_pdf(input_pdf, output_pdf_ocrmypdf)

    # pdf to image conversion
    # Convert scanned PDF to images
    # images = convert_from_path(r"C:\Nandeesh\krishnaik_ml_course\Q067_5-6-08_ARI_diagram.pdf", dpi=150,\
    #                         poppler_path=r"C:\Users\nande\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
    #                         )
    # for i, image in enumerate(images):
    #     image.save(f"images/page_{i+1}.jpg", "JPEG")


    # Process the PDF using image classification
    pages = classify_image("image_dir_path")

    # Save the classified pages to a new PDF
    for i in pages:
        output_pdf = f"pdf_co_workspace\initial_pdfs\page_{i}.pdf"
        # Extract the page from the OCRmyPDF output
        extract_page_from_pdf(input_pdf_path=output_pdf_ocrmypdf, output_pdf_path=output_pdf, page_number=i)

    # Process the PDF using image handling
    for i in os.listdir("pdf_co_workspace\initial_pdfs"):
        input_pdf = os.path.join("pdf_co_workspace\initial_pdfs", i)
        output_pdf = os.path.join("pdf_co_workspace\final_pdfs", f"processed_{i}")
        # Process the PDF using image handling
        logger.info(f"Processing images in PDF: {input_pdf}")
        image_processing(input_pdf, output_pdf)
    logger.info("PDF_co processing completed.")


