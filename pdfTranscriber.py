import PyPDF2
import base64
import requests
from pdf2image import convert_from_path

pdffileobj=open('AA_Deep_Learning_final (3).pdf','rb')

pdfreader=PyPDF2.PdfReader(pdffileobj)

x = len(pdfreader.pages)

text_array = []
for i in range(x):
    pageobj=pdfreader.pages[i]

    text=pageobj.extract_text()
    print(text)
    text_array.append(text)
import io

def encode_pdf_page(pdf_path, page_number):
  with open(pdf_path, 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    if page_number < 0 or page_number >= len(pdf_reader.pages):
      print("Invalid page number")
      return

    # Get the specified page
    page = pdf_reader.pages[page_number]

    # Create a BytesIO object to store the content of the page
    page_content = io.BytesIO()
    page_writer = PyPDF2.PdfWriter()
    page_writer.add_page(page)
    page_writer.write(page_content)

    # Encode the content using base64
    bs64 = base64.b64encode(page_content.getvalue())
    print(bs64.decode('utf-8'))
    return bs64

def encode_pdf_page_to_image(pdf_path, page_number):
  # Convert the PDF page to an image
  images = convert_from_path(pdf_path, first_page=page_number + 1, last_page=page_number + 2)

  # If the page was converted successfully, there should be one image in the list
  if images:
    # Save the image to a BytesIO object
    image_content = io.BytesIO()
    images[0].save(image_content, format='JPEG')

    # Encode the content using base64
    bs64 = base64.b64encode(image_content.getvalue())
    return bs64

page_to_test = encode_pdf_page_to_image(pdf_path, page_number)

# Specify the path to your PDF file and the page number (0-based index)
pdf_path = 'AA_Deep_Learning_final (3).pdf'
page_number = 2  # Change this to the desired page number

page_to_test = encode_pdf_page(pdf_path, page_number)

import openai
client = OpenAI()
import dotenv

config = dotenv.dotenv_values(".env")
openai.api_key = config['OPENAI_API_KEY']

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {openai.api_key}"
}

payload = {
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What’s in this image?"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{page_to_test}"
          }
        }
      ]
    }
  ],
  "max_tokens": 300
}

import requests
response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
print(response.json())
