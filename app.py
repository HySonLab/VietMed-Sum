#Libraries needed for this program
# Whisper
#Gradio
#speech recognition
#googletrans

import whisper
import speech_recognition as sr
from googletrans import *
import gradio as gr
from pydub import AudioSegment
from time import sleep
'''
def recognize_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("" + text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None
'''
def recognize_from_file(audio_file):
    model = whisper.load_model("medium") 
    result = model.transcribe(audio_file)
    text = result["text"]
    print("Text from audio file:", text)
    return text

def translate_text(text, target_language=None):
    translator = Translator()

    if not target_language:  
        detected_lang = translator.detect(text).lang
        print(f"Detected language: {detected_lang}")
        target_language = detected_lang  
        print(f"Translating to: {target_language}")

    try:
        translated_text = translator.translate(text, dest=target_language).text
        print("Translation:", translated_text)
        return translated_text
    except Exception as e:  
        print(f"Translation error: {e}")
        return text  

def summarize_text(text):
    from gensim.summarization import summarize
    summary = summarize(text, word_count=100)
    print("Summary:", summary)
    return summary

'''
def speech_to_text(audio_or_text, translate_to, summarize):
    if isinstance(audio_or_text, str):  
        text = audio_or_text
        translated_text = translate_text(text, translate_to) if translate_to else text
        summary = summarize_text(translated_text) if summarize else translated_text
        return translated_text, summary
    else:  
        if audio_or_text.name.endswith(".wav") or audio_or_text.name.endswith(".mp3"):
            text = recognize_from_file(audio_or_text)
        else:
            text = recognize_from_mic()
        translated_text = translate_text(text, translate_to) if translate_to else text
        summary = summarize_text(translated_text) if summarize else translated_text
        return translated_text, summary
'''
def speech_to_text(audio_or_text, translate_to, summarize):
    if isinstance(audio_or_text, str):  
        text = audio_or_text
    else:  
        if audio_or_text.name.endswith(".wav") or audio_or_text.name.endswith(".mp3"):
            text = recognize_from_file(audio_or_text)
        else:
            text = recognize_from_mic_realtime()
    
    translated_text = translate_text(text, translate_to) if translate_to else text
    summary = summarize_text(translated_text) if summarize else translated_text
    return text, translated_text, summary

def recognize_from_mic_realtime():
  recognizer = sr.Recognizer()
  chunk = 1024  
  format = pyaudio.paInt16 
  channels = 1  
  rate = 44100  

  p = pyaudio.PyAudio()

  stream = p.open(format=format, channels=channels, rate=rate, input=True, output=False, frames_per_buffer=chunk)

  print("Listening...")

  text = ''
  while True:
    data = stream.read(chunk)
    try:
      recognized_text = recognizer.recognize_google(data)
      text += recognized_text
      print(text)  # Display real-time transcript (optional)
    except sr.UnknownValueError:
      print("Could not understand audio")
    except sr.RequestError as e:
      print("Could not request results from Google Speech Recognition service; {0}".format(e))
      break

  stream.stop_stream()
  stream.close()
  p.terminate()

  return text

interface = gr.Interface(
    fn=speech_to_text,
    inputs=[
        gr.Audio(type="filepath"),
        gr.Checkbox(label="Summarize")
    ],
    outputs=[gr.Textbox(label="Text"), gr.Textbox(label="Summary")],
    title="Speech to Text",
    description="Convert speech from microphone or audio file and summarize."
)
interface.launch()
