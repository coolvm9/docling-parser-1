from docling.document_converter import DocumentConverter

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import urllib.request
print(urllib.request.urlopen("https://arxiv.org/pdf/2408.09869").status)

source = "https://arxiv.org/pdf/2408.09869"

converter = DocumentConverter()  # Downloads - Detection model, Recognition model
result = converter.convert(source)

print(result.document.export_to_markdown())
