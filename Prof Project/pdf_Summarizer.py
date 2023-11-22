import PyPDF2
import base64
import requests
from pdf2image import convert_from_path
import os
import fitz
import io
import base64
from PIL import Image
import requests
import openai
import dotenv

def pdf_page_to_base64(pdf_path, page_number):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number - 1)  # zero-based indexing
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    base64_image = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

    return base64_image

pdf_path = '../Sources/Data/Prof/AA_Deep_Learning_final (3).pdf'

slides = fitz.open(pdf_path)
# Specify the path to your PDF file and the page number (0-based index)

for i in range(49, len(slides)):
    print("Page Number: ", i)
    page_number = i # Change this to the desired page number

    page_to_input = pdf_page_to_base64(pdf_path, page_number)


    config = dotenv.dotenv_values("../.env")
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
              "text": "This is a slide of a lecture, please give detailled explanation on the information provided in it. "
                      "Do not include information about the style / design of the slide as well as the logos of the university or the professor. Focus on the information that is relevant to the topic of the lecture."
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{page_to_input}"
              }
            }
          ]
        }
      ],
        "max_tokens": 2000,
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    response_text = response.json()['choices'][0]['message']['content']
    with open('../Sources/Data/Prof/Slides/Slide_'+str(i)+'.txt', 'w', encoding='utf-8') as f:
        f.write(response_text)
        print("Slide saved as Slide_"+str(i)+".txt")

