import io
import openai

import streamlit as st
import requests
import PIL
from PIL import Image
st.sidebar.header("Enter you Api key below")
key=st.sidebar.text_input('OpenAI API Key' ,type='password')
openai.api_key = key
#st.write(key)
header=st.container()
input_text=st.container()

with header:
    st.header(" TExt to Image Gnerater Application")

def generate_image(text):
    # Generate the image using OpenAI's DALL-E model
    response = openai.Image.create(
        prompt=text,
        n=1,
        size = "512x512"
        )

    # Get the image URL from the response
    image_url = response.data[0]['url']

    # Download the image and convert it to a PIL image
    image_content = requests.get(image_url).content
    image = Image.open(io.BytesIO(image_content))

    #image.show()
    return image
    
with input_text:
    
 prompt = st.text_input("Enter your prompt to generate the image: ")
 img=generate_image(prompt)
 st.image(img)
 
