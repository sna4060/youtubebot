from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
 
load_dotenv()   ## load all environment variables
 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
 
st.set_page_config(page_title="Youtube Summarizer",page_icon="📺")
 
st.header("My Youtube Summarizer Web Application")
 
youtube_link = st.text_input("Enter Youtube Video Link")
 
if youtube_link:
    try:
        video_id = youtube_link.split("=")[1]
        st.image("https://img.youtube.com/vi/{}/0.jpg".format(video_id),use_column_width=True)
    except Exception as e:
        st.write("Invalid Url")
 
submit = st.button("Summarize")
 
prompt = """You are a YouTuve video summarizer, you will be taking the transcript text and summarize the
entire video and provide the import summary. Please provide the summary of the text given here in two
languages, English and Hindi within 250-300 words. Please translate accordingly. """
 
def extract_transcript_details(video_url):
    try:
       video_id = youtube_link.split("=")[1]
       transcript_text =  YouTubeTranscriptApi.get_transcript(video_id,languages=["en","ko"])
       transcript = ""
       for i in transcript_text:
          transcript += " "+i['text']
       return transcript
    except Exception as e:
        raise e
 
if submit:
    try:
        transcript_text = extract_transcript_details(youtube_link)
        if transcript_text:
            st.write(transcript_text)
        else:
            st.write("Unable to summarize")
    except Exception as e:
        st.write("Unable to summarize")
