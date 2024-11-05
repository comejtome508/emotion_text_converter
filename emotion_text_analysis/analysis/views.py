from django.shortcuts import render
from django.http import JsonResponse
from pytube import YouTube
from transformers import pipeline
import os
import yt_dlp
import whisper

def home(request):
    return render(request, 'home.html')

def process_video(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'video_audio.%(ext)s',  # Save as "video_audio.mp3"
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return JsonResponse({'status': 'success', 'message': 'Audio extracted successfully!'})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status': 'error', 'message': f'Error: {str(e)}'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def transcribe_audio(request):
    # Assuming the audio file is saved as 'media/video_audio.mp3'
    audio_path = "video_audio.mp3"

    # Load the Whisper model
    model = whisper.load_model("base")
    
    # Transcribe the audio file
    result = model.transcribe(audio_path)
    transcript = result['text']
    
    # Emotion analysis
    emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
    emotions = emotion_classifier(transcript)

    # Return results as JSON
    return JsonResponse({
        'transcript': transcript,
        'emotions': emotions
    })