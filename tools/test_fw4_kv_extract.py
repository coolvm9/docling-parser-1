from docling.document_converter import DocumentConverter
import os

# Path to the FW4 form PDF
fw4_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/forms/fw4.pdf'))

converter = DocumentConverter()
result = converter.convert(fw4_path)

doc = result.document

# Print all available attributes and methods of the doc object
print("Available attributes and methods in doc:")
print(dir(doc))

# Try printing the document as a dictionary if possible
if hasattr(doc, 'dict'):
    print("\nDocument as dict:")
    print(doc.dict())

# Try printing the document as JSON if possible
if hasattr(doc, 'json'):
    print("\nDocument as JSON:")
    print(doc.json())

# Try printing the document's __dict__
print("\nDocument __dict__:")
print(doc.__dict__)
