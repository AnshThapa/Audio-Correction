# Video Audio Replacement using AI
### By Ansh Thapa (anshthapa007@gmail.com)

This is a Python-based Proof of Concept (PoC) project that replaces the audio of a video with AI-generated speech. The project uses Google's Speech-to-Text API to transcribe the original audio, corrects the transcription using OpenAI's GPT-4 model, and finally replaces the original audio with AI-generated speech using Google Text-to-Speech.


## Features

1. Video Upload: Users can upload a video file in .mp4 format.
2. Audio Transcription: The project's first step extracts the audio from the video and transcribes it using Google's Speech-to-Text.
3. Transcription Correction: The transcription is then passed to OpenAI's GPT-4 to remove grammatical errors, 'umms,' 'hmms,' and other filler words.
4. Text-to-Speech: The corrected transcription is converted into speech using Google's Text-to-Speech API (Journey Neural voice).
5. Audio Replacement: The newly generated audio is synced back with the original video, replacing the old audio.

## Prerequisites

### 1. Google Cloud Setup
Google Cloud API Keys: Ensure you have enabled the Google Cloud Speech-to-Text and Text-to-Speech APIs for your project. You'll need a Google Cloud service account key JSON file.
Enable APIs:
Speech-to-Text: Enable here.
Text-to-Speech: Enable here.
### 2. OpenAI Setup
You need an OpenAI API key with access to GPT-4.
You can get your OpenAI API Key by signing up for OpenAI's API service.
### 3. Python Environment
Make sure you have Python 3.7+ installed.
### 4. Install Required Libraries
Install the necessary Python packages via pip:

pip install streamlit moviepy speechrecognition openai google-cloud-speech google-cloud-texttospeech

copy the above mentioned requirements into your terminal and press enter

## Setup

1. Google Cloud Credentials
2. Create a service account key from the Google Cloud Console.
3. Download the service account key in JSON format.
4. Set the environment variable [GOOGLE_APPLICATION_CREDENTIALS] to the path of the downloaded JSON file.

for windows:

	<sub> set GOOGLE_APPLICATION_CREDENTIALS="path\to\your\google-cloud-key.json" </sub>

## OpenAI API Key

Replace the existing key with your own OpenAI API Key in the code (Recommended):

	<sub> openai.api_key = "your_openai_api_key" </sub>

## Running the Project
1. Start the Streamlit app: Run the following command to launch the Streamlit interface:

<sub> streamlit run app.py 	</sub>

2. Upload a Video: In the web interface, upload a .mp4 video file. The system will extract the audio, transcribe it, correct the transcription, and then replace the original audio with an AI-generated voice.
3. View the Output: After processing, the app will display the final video with the new audio in the browser.

## Known Issues and Limitations
1. Syncing issues may occur if there are significant pauses or mismatches in transcription and speech generation.
2. For larger video files, the processing time may be longer.
3. Ensure your Google Cloud API quota is sufficient and is activated, especially for Speech-to-Text and Text-to-Speech requests.
