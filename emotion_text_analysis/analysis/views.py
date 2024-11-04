from django.shortcuts import render
from django.http import JsonResponse
from pytube import YouTube
import os
import yt_dlp

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
# def process_video(request):
#     if request.method == 'POST':
#         url = request.POST.get('url')
#         try:
#             yt = YouTube(url)
#             audio_stream = yt.streams.filter(only_audio=True).first()
#             if audio_stream:
#                 audio_stream.download(output_path='/Desktop', filename='video_audio.mp4')
#                 return JsonResponse({'status': 'success', 'message': 'Audio extracted successfully!'})
#             else:
#                 return JsonResponse({'status': 'error', 'message': 'Audio stream not found.'})
#         except Exception as e:
#             print(f"Error: {e}")  # Print the specific error for debugging
#             return JsonResponse({'status': 'error', 'message': f'Error: {str(e)}'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})