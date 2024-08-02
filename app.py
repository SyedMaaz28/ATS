import base64
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
import os
from PIL import Image
import pdf2image
import io

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to page
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page=images[0]

        # Convert the image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # Convert to base64
            }
        ]
        return pdf_parts

    else:
        raise FileNotFoundError("No file uploaded")


# streamlit app

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Choose your resume PDF", type="pdf")

if uploaded_file is not None:
    st.write("PDF uploaded successfully")

submit1 = st.button("Tell me about the resume")
# submit2 = st.button("How can I improve the resume")
# submit3 = st.button("Score the resume")
submit4 = st.button("Percentage match")

input_prompt1="""
You are an experienced HR with Tech Experience in any one of the field of Data Science or Full Stack Web Development or
Big Data Engineer or DEVOPS or Data Engineer or Business Analyst, your task is to review the
resume provided against the job description for these profiles and give a feedback. Make sure to consider the 
and you need to help me rank the resume based on the job description.
Please share your professional evaluation on whether the candidates profiles aligh with job description
and highlight the strenghts and weaknesses of the application with relation to specified Job description.
"""

input_prompt2="""
You are skilled ATS (Application Tracking System) scanner with a deep understanding of any one of the field of Data Science or Full Stack Web Development or
Big Data Engineer or DEVOPS or Data Engineer or Business Analyst and deep ATS functionality,your task is to evaluate the resume against the job description 
and give me the percentage of match if the resume matches to Job Description
First the output should come as percentage match in new line and then keyword missing in new line in bullet points and last the reason behind the percentage match 
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file")

# elif submit2:
#     if uploaded_file is not None:
#         pdf_content = input_pdf_setup(uploaded_file)
#         response = get_gemini_response(input_prompt2, pdf_content, input_text)
#         st.subheader("The response is")
#         st.write(response)
#     else:
#         st.write("Please upload a PDF file")

# elif submit3:
#     if uploaded_file is not None:
#         pdf_content = input_pdf_setup(uploaded_file)
#         response = get_gemini_response(input_prompt3, pdf_content, input_text)
#         st.subheader("The response is")
#         st.write(response)
#     else:
#         st.write("Please upload a PDF file")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file")

else:
    st.write("Please enter the job description and upload a PDF file")

