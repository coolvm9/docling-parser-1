from docling.document_converter import DocumentConverter
from pathlib import Path
import pandas as pd
import os

# Path to the sample PDF used in the Docling table export example
pdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/pdf/2206.01062.pdf'))

converter = DocumentConverter()
result = converter.convert(pdf_path)

doc = result.document

# Export and print all tables as markdown
for table_ix, table in enumerate(doc.tables):
    table_df: pd.DataFrame = table.export_to_dataframe()
    print(f"## Table {table_ix+1}")
    print(table_df.to_markdown())
    # Optionally, save as CSV
    csv_path = os.path.join(os.path.dirname(__file__), f'table_{table_ix+1}.csv')
    table_df.to_csv(csv_path)
    print(f"Saved table {table_ix+1} as {csv_path}")
