import PyPDF2
import base64
import requests
from pdf2image import convert_from_path
import os
import fitz
import io
import base64
from PIL import Image


def pdf_page_to_base64(pdf_path, page_number):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number - 1)  # zero-based indexing
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    base64_image = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

    return base64_image


# Specify the path to your PDF file and the page number (0-based index)
pdf_path = 'Data/Prof/AA_Deep_Learning_final (3).pdf'
page_number = 2  # Change this to the desired page number

page_to_test = pdf_page_to_base64(pdf_path, page_number)

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
          "text": "Generate a detailed description of the visual content in this slide, focusing on elements that are relevant to the topic of the lecture. Additionally, provide insights or questions that my professor might discuss based on this slide."
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
    "max_tokens": 2000,
}

import requests
response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
print(response.json()['choices'][0]['message']['content'])
