import wave
import json

from vosk import Model, KaldiRecognizer
import speech_recognition as sr
from io import BytesIO

def vosk_rec_min(audio_file: BytesIO) -> str:
    MODEL_PATH =  "Modelos/Vosk/vosk-model-small-pt-0.3"

    # Carregar o modelo
    model = Model(MODEL_PATH)
    
    text = ""
    
    # Rewind the BytesIO object to ensure we're reading from the beginning
    audio_file.seek(0)
    
    # Abrir o arquivo de áudio usando o BytesIO
    with wave.open(audio_file, "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
            raise ValueError("O áudio deve estar em mono, 16-bit e 16 kHz.")

        recognizer = KaldiRecognizer(model, wf.getframerate())

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result_str = recognizer.Result()
                result = json.loads(result_str)
                text += result.get('text', '')

    # Resultado final
    final_result_str = recognizer.FinalResult()
    final_result = json.loads(final_result_str)
    text += final_result.get('text', '')

    return text



def vosk_rec(audio_file: BytesIO) -> str:
    # Baixe o modelo para português em https://alphacephei.com/vosk/models
    MODEL_PATH =  "Modelos/Vosk/vosk-model-pt-fb-v0.1.1-20220516_2113"

    # Carregar o modelo
    model = Model(MODEL_PATH)

    text = ""
    audio_file.seek(0)
    
    # Abrir o arquivo de áudio
    with wave.open(audio_file, "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
            raise ValueError("O áudio deve estar em mono, 16-bit e 16 kHz.")

        recognizer = KaldiRecognizer(model, wf.getframerate())

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result_str = recognizer.Result()
                result = json.loads(result_str)
                text += result.get('text', '')

    # Resultado final
    final_result_str = recognizer.FinalResult()
    final_result = json.loads(final_result_str)
    text += final_result.get('text', '')

    return text


def speech_rec(audio: BytesIO) -> str:

    recognizer = sr.Recognizer()
    audio.seek(0)

    # Carregar o áudio
    with sr.AudioFile(audio) as source:
        audio = recognizer.record(source)

    # Converter áudio em texto
    try:
        text = recognizer.recognize_google(audio,language = "pt-BR")
        print("Texto reconhecido:", text)
    except sr.UnknownValueError:
        print("Não foi possível entender o áudio")
    except sr.RequestError as e:
        print(f"Erro ao acessar o serviço: {e}")
    
    return text