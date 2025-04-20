from src.pdf_to_md import pdf_to_md_with_plumber
from src.extract.extract_md import process_md_file
from src.upload_points import upload_points
import argparse

parser = argparse.ArgumentParser(description="Upload points to qdrant database with provided janssen cmi pdf file.")
parser.add_argument("--collection", type=str, required=True, help="The collection name")
parser.add_argument("--input", type=str, required=True, help="The input .pdf cmi file path")

args = parser.parse_args()
pdf_path = args.input
collection_name = args.collection
# pdf_path = "src/documentation/janssen/darzalex_cmi.pdf"
# collection_name = "janssen"
md_path = "src/documentation/extracted_md.md"


if __name__ == '__main__':
    pdf_to_md_with_plumber(pdf_path, md_path)
    print("pdf successfully converted to md")
    extracted_chunks = process_md_file(pdf_path, md_path)
    print(extracted_chunks)
    print("md successfully extract to chunks")
    upload_points(collection_name, extracted_chunks)
    print("successfully uploaded all the chunks")