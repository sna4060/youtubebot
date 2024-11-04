from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()  # Load all environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="Youtube Summarizer", page_icon="📺")

st.header("My Youtube Summarizer Web Application")

# Function to extract video_id from different YouTube URL formats
def extract_video_id(youtube_link):
    if "youtu.be" in youtube_link:
        return youtube_link.split('/')[-1].split('?')[0]
    elif "youtube.com" in youtube_link:
        return youtube_link.split("v=")[-1].split('&')[0]
    else:
        return None

youtube_link = st.text_input("Enter Youtube Video Link")

if youtube_link:
    video_id = extract_video_id(youtube_link)
    if video_id:
        st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    else:
        st.write("Invalid URL format")

submit = st.button("Summarize")

# Adjusted prompt to ensure Korean translation
prompt = """You are a YouTube video summarizer. Take the transcript text and summarize the
entire video, providing an important summary. Provide the summary in both English and Korean,
with each summary within 250-300 words. \n\n"""

def extract_transcript_details(video_id):
    try:
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=["ko", "en"])
        transcript = " ".join([i['text'] for i in transcript_text])
        return transcript
    except Exception as e:
        st.write("This video does not have available subtitles.")
        return None

if submit:
    try:
        if video_id:
            transcript_text = extract_transcript_details(video_id)
            if transcript_text:
                model = genai.GenerativeModel("gemini-pro")
                summary = model.generate_content(prompt + transcript_text)
                st.write("### English Summary\n")
                st.write(summary.text)
                st.write("### Korean Summary\n")
                st.write(summary.text_korean)
            else:
                st.write("Unable to summarize due to missing transcript.")
        else:
            st.write("Invalid URL format.")
    except Exception as e:
        st.write(f"Unable to summarize: {e}")
