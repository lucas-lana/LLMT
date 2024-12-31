import wave
import json

import speech_recognition as sr
from vosk import Model, KaldiRecognizer

import Audio_Operations as ao

def vosk_rec_min(caminho:str) -> str:
    MODEL_PATH =  "/home/Lucas/Documentos/Modelos/Vosk/vosk-model-small-pt-0.3"
    audio_file = ao.convert_to_vosk(caminho, "wav")

    # Carregar o modelo
    model = Model(MODEL_PATH)
    
    text = ""
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


def vosk_rec(caminho:str) -> str:
    # Baixe o modelo para português em https://alphacephei.com/vosk/models
    MODEL_PATH =  "/home/Lucas/Documentos/Modelos/Vosk/vosk-model-pt-fb-v0.1.1-20220516_2113"
    audio_file = ao.convert_to_vosk(caminho, "wav")

    # Carregar o modelo
    model = Model(MODEL_PATH)

    text = ""
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


def speech_rec(caminho: str) -> str:

    recognizer = sr.Recognizer()
    
    caminho = ao.convert_to_wav(caminho, ao.reconhece_formato(caminho))

    # Carregar o áudio
    with sr.AudioFile(caminho) as source:
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