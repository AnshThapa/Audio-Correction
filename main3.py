import streamlit as st
from moviepy.editor import VideoFileClip, AudioFileClip
import speech_recognition as sr
import requests
import json
from google.cloud import texttospeech
import os

# Set up Google Cloud credentials (path to your Google Cloud JSON key)
# Add your own path
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "E:\ML practice\Audio correction\mythic-inn-422205-n4-347e516642c6.json"

# Set up Azure OpenAI API Key and Endpoint URL
# You can use your own API key and Endpoints
api_key = "22ec84421ec24230a3638d1b51e3a7dc"
endpoint_url = "https://internshala.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"

# Streamlit App
st.title("Video Audio Replacement using AI")

# Step 1: Upload Video File
video_file = st.file_uploader("Upload a Video", type=["mp4"])

# Save the uploaded video (in temporary file)
if video_file is not None:
    temp_video_path = "temp_video.mp4"
    with open(temp_video_path, "wb") as f:
        f.write(video_file.read())

# Extract audio from video
def extract_audio(video_file):
    clip = VideoFileClip(video_file)
    audio_path = "extracted_audio.wav"
    clip.audio.write_audiofile(audio_path)
    return audio_path

# Step 2: Transcribe Audio using Google Speech-to-Text
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        transcription = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        transcription = "Could not understand the audio."
    return transcription

# Step 3: Correct Transcription using Azure OpenAI GPT-4o
def correct_transcription(transcription):
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    
    # Prepare the request payload (prompt)
    data = {
        "messages": [
            {
                "role": "system", 
                "content": "You are a helpful assistant that corrects grammatical mistakes and removes unnecessary fillers like 'um', 'hmm'."
            },
            {
                "role": "user",
                "content": transcription
            }
        ],
        "max_tokens": 1000
    }

    # Make the POST request to the Azure OpenAI API
    response = requests.post(endpoint_url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        corrected_text = result['choices'][0]['message']['content']
        return corrected_text
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
        return None

# Step 4: Convert Corrected Text to Speech (using Google's Text-to-Speech - Journey Voice)
def text_to_speech(corrected_text):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=corrected_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-JourneyNeural"
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

    audio_output = "output_audio.mp3"
    with open(audio_output, "wb") as out:
        out.write(response.audio_content)
    return audio_output

# Step 5: Replace Audio in Video
def replace_audio_in_video(video_file, new_audio_file, output_video):
    video_clip = VideoFileClip(video_file)
    audio_clip = AudioFileClip(new_audio_file)
    final_video = video_clip.set_audio(audio_clip)
    final_video.write_videofile(output_video, codec="libx264", audio_codec="aac")

# Main Logic
if video_file:
    st.write("Processing your video...")

    # Step 1: Extract Audio from Video
    audio_path = extract_audio(temp_video_path)
    st.write("Audio extracted from the video.")

    # Step 2: Transcribe Audio using Google Speech-to-Text
    transcription = transcribe_audio(audio_path)
    st.write("Original Transcription:", transcription)

    # Step 3: Correct Transcription using Azure OpenAI GPT-4o
    corrected_text = correct_transcription(transcription)
    if corrected_text:
        st.write("Corrected Transcription:", corrected_text)

        # Step 4: Convert Corrected Text to Speech
        new_audio_path = text_to_speech(corrected_text)
        st.write("Generated new audio using AI voice.")

        # Step 5: Replace Audio in the Video
        output_video = "final_output.mp4"
        replace_audio_in_video(temp_video_path, new_audio_path, output_video)
        st.write("Audio replaced in the video successfully!")

        # Step 6: Display Final Video with New Audio
        st.video(output_video)
    else:
        st.error("Failed to correct transcription.")
