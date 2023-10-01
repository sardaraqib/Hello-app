import streamlit as st
import pandas as pd
import PyPDF2
import io
import openai
import docx2txt
import pyperclip



import streamlit as st
st.sidebar.header("select from the drop down") 
st.sidebar.write("if you are new select the ** ""how to use" "** from the drop down ")
pages = ["Home", "How to use", "Contact"]
 
page = st.sidebar.selectbox("Menu", pages)


for p in pages:
    st.sidebar.button(p)

if page == "Home":
  st.title(" AI Document Chatbot Testing  Phase")
  key=st.sidebar.text_input("Put You Api key here",type='password')
  openai.api_key=key



#defining a fuction to extract text from the pdf file
  def extract_text_from_pdf(file):
    #creating a BytesIO object from the uploaded file
     pdf_file_obj=io.BytesIO(file.read())
    #creating pdf reading object fromthe BYtesIo object
     pdf_reader= PyPDF2.PdfReader(pdf_file_obj)
    #initalize the empty string to store the extracted text
     text=''
    #looping through each page of the pdg file and extracting the text
     for page_num in range(len(pdf_reader.pages)):
        page=pdf_reader.pages[page_num]
        text=page.extract_text()
    #Returning the text
     return text




#DEfine a fuction to extract data from the docs

  def extract_text_from_docs(file):
    #creating a BytesIo obect from the upload file    #docs ma ary pages aik sath hoty ha 
                                                   #ais lya ham loops ni laga rhy df ma lagany party 
    docs_file_obj=io.BytesIO(file.read())
   # extracting  text from the word file
    text=docx2txt.process(docs_file_obj)
    return text



#define a fuction to extract text from a text file
  def extract_text_from_txt(file):
  #Reading the uploaded file as text
   text=file.read().decode('utf-8')
  #returning the extracted text
   return text




#definign a function to extract the text from the file beelaf of type
  def extract_text_from_file(file):
    #checking the type of uploaded file
   if file.type == 'application/pdf':
      #extracting text from the pdf file
       text=extract_text_from_pdf(file)
   elif file.type=='application/vnd.openxmlformats-officedocument.wordprocessingml.document':
      text=extract_text_from_docs(file)
    #extractinf rom text file
   elif file.type=='text/plain':
      text=extract_text_from_txt(file)
   else :
      st.error("unspported file type")
      text=None
  #returning a text
   return text    


# Get Question from the user
# Deinign a fuction to generate question from text using GPt-3
  def get_question_from_gpt(text):
   #selecting the first 4096 character of the text at the prompt for GPT-3
   prompt=text[:4096]     
   #genearting a qustion using the GPt-3 Api
   response=openai.Completion.create(engine='text-davinci-003',prompt=prompt,temperature=0.5,max_tokens=30)
   #returning the generated question
   return response.choices[0].text.strip()


# Deinign a fuction to generate answer of the question from text using GPt-3
  def get_answer_from_gpt(text,question):
   #selecting the first 4096 character of the text at the prompt for GPT-3 along with question
   prompt=text[:4096]+"\nQuestion: "+ question +"\nAnswer:"     
   #genearting a answer using the GPt-3 Api
   response=openai.Completion.create(engine='text-davinci-003',prompt=prompt,temperature=0.6,max_tokens=2000)
   #returning the generated answer
   return response.choices[0].text.strip()

#define a main fuction 
  def main():
   #setting the title of the app
   st.subheader("Ask a question from the uploaded documents")
   st.write("> After the question wait for 2Osecond then ask other question  its a testing phase does not have that much power ")
   uploaded_file=st.file_uploader('Chose a file',type=['pdf','docx','txt'])
   #checking if a file is uploaded 
   if uploaded_file is not None:
      text=extract_text_from_file(uploaded_file)
    #checking the if text was extracted succesfuly
      if text is not None:
         #generating a question from the extracted text using GPT-3
         question=get_question_from_gpt(text)
         #display the genrated question
         st.write('Question' +question)
         #creating atext input for the user toa sk a question
         user_question=st.text_input("Ask a queston about the document")
         #checking if a  user has asked a question
         if user_question:
             #generating an answer to a user queston
             answer=get_answer_from_gpt(text,user_question)
             #Display the generated answer
             st.write("Answer:"+answer)
             #creating a button to copy the answer text in clipboard
             if st.button("Copy anser text"):
              pyperclip.copy(answer)
              st.success("Successfuly answer is copied")

#calling the main fuction
  if __name__=="__main__":
    main()              
    
elif page == "How to use":
    st.title("Making account on the chatgpt")
    st.write("Every OpenAI account has a security API Key that can be used to integrate third party tools, access OpenAI API's like their client API libraries for ChatGPT for chatbot conversations, DALL-E, OpenAI's AI art generator, which creates images based on detailed text descriptions from a person, and Whisper, a speech-recognition model that can transcribe and translate audio from many languages.")
    st.header("How to Find your Secret API Key in your OpenAI Account")
    st.write("First sign in or sign up for your OpenAI account.  You can find sign up and login link here: https://platform.openai.com/")
    st.image("https://d33v4339jhl8k0.cloudfront.net/docs/assets/589c78fadd8c8e73b3e9710e/images/641e20b450f28e43c4c5caae/file-i68gbKeqyP.jpg")
    st.write("Once logged in, click on your profile name or Icon to open the menu.Then select the 'View API Keys' option as highlighted in the screenshot below.")
    st.image("https://d33v4339jhl8k0.cloudfront.net/docs/assets/589c78fadd8c8e73b3e9710e/images/641e21151b1cd16ee8afa02e/file-yHWdq1PWBZ.png")
    st.write("On the API Keys page, you will see a list of existing Secret Keys.  Just select 'Create new secret key' to generate a new key to use your your client integrations like when you want to sue ChatGPT into your Live Chat chatbots.")
    st.image("https://d33v4339jhl8k0.cloudfront.net/docs/assets/589c78fadd8c8e73b3e9710e/images/641e21559a0fe82b2d575045/file-Btil8dqShs.jpg")
    st.write("Then click the green icon on the popup page to copy your OpenAI secret key to a safe place.")
    st.image("https://d33v4339jhl8k0.cloudfront.net/docs/assets/589c78fadd8c8e73b3e9710e/images/64208dd150f28e43c4c5cb44/file-GUYpN5uLSi.jpg")
    st.write("save the key and go back to the home page  put the key there  and start using it")

   
elif page == "Contact":
    st.title("Queries")
    st.subheader("For any problem contact us on this Email")
    st.subheader("aqib51719@gmail.com")
        
