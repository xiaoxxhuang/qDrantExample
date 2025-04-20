import pdfplumber
import pandas as pd
import re
from pdfplumber.utils import extract_text, get_bbox_overlap, obj_to_bbox
import tabulate

def clean_and_format_text(df):
    """
    Cleans and formats the text by:
    - Splitting content into multiple rows if '. \n' or '?\n' is detected.
    - Removing unwanted sequences after splitting.
    """
    formatted_rows = []
    for _, row in df.iterrows():
        split_rows = [[] for _ in range(len(row))]  # Track splits for all columns
        max_splits = 0  # Keep track of the maximum number of splits in a row

        for col_idx, cell in enumerate(row):
            if pd.isna(cell):  # Handle missing cells
                split_rows[col_idx].append(None)
                continue
            # Step 1: Split content based on '. \n' or '?\n'
            cleaned_text = re.sub(r'(\n⦁|⦁| • |\n\u2022|\u2022)', ' ', str(cell))
            split_texts = re.split(r'\.\s*\n|\?\s*\n', cleaned_text)

            # Step 2: Clean each split text
            cleaned_splits = []
            for split_text in split_texts:
                if split_text.strip():  # Skip empty strings
                    format_text = split_text.replace(" \n", " ").replace("\n", " ")  # Further clean
                    cleaned_splits.append(format_text.strip())

            split_rows[col_idx].extend(cleaned_splits)
            max_splits = max(max_splits, len(cleaned_splits))

        # Normalize split rows to ensure all columns have the same number of rows
        for col_idx in range(len(row)):
            while len(split_rows[col_idx]) < max_splits:
                split_rows[col_idx].append(None)

        # Transpose split rows to create complete rows
        for i in range(max_splits):
            formatted_rows.append([split_rows[col_idx][i] for col_idx in range(len(row))])

    return pd.DataFrame(formatted_rows, columns=df.columns)


# Example usage
def pdf_to_md_with_plumber(pdf_path, md_path, footer_threshold=100):
    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        filtered_page = page
        page_height = page.height
        chars = filtered_page.chars
        for table in page.find_tables():
            x0, y0, x1, y1 = table.bbox
            if y1 > page_height - footer_threshold:
                continue

            first_table_char = page.crop(table.bbox).chars[0]
            filtered_page = filtered_page.filter(lambda obj:
                                                 get_bbox_overlap(obj_to_bbox(obj), table.bbox) is None
            )
            chars = filtered_page.chars
            df = pd.DataFrame(table.extract())

            formatted_df = clean_and_format_text(df)

            markdown = formatted_df.to_markdown(index=False)
            chars.append(first_table_char | {"text": markdown})

        page_text = extract_text(chars, layout=True)
        all_text.append(page_text)
    pdf.close()

    with open(md_path, 'w', encoding='utf-8') as md_file:
        md_file.write("\n".join(all_text))
    print(f"Markdown file saved at: {md_path}")