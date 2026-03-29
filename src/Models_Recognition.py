import urllib.request
import zipfile
import wave
import json
import os

from vosk import Model, KaldiRecognizer
import speech_recognition as sr
from io import BytesIO


MODELS = {
    "small": {
        "url": "https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip",
        "path": "Modelos/Vosk/vosk-model-small-pt-0.3",
        "folder_name": "vosk-model-small-pt-0.3"
    },
    "large": {
        "url": "https://alphacephei.com/vosk/models/vosk-model-pt-fb-v0.1.1-20220516_2113.zip",
        "path": "Modelos/Vosk/vosk-model-pt-fb-v0.1.1-20220516_2113",
        "folder_name": "vosk-model-pt-fb-v0.1.1-20220516_2113"
    }
}

def ensure_models_downloaded():
    base_path = "Modelos/Vosk"
    os.makedirs(base_path, exist_ok=True)
    
    for name, info in MODELS.items():
        if not os.path.exists(info["path"]):
            print(f"--- Baixando modelo {name.upper()} ({info['url'].split('/')[-1]})... ---")
            zip_tmp = f"{name}_model.zip"
            
            # Download com feedback visual simples
            urllib.request.urlretrieve(info["url"], zip_tmp)
            
            print(f"Extraindo {name}...")
            with zipfile.ZipFile(zip_tmp, 'r') as zip_ref:
                zip_ref.extractall(base_path)
            
            os.remove(zip_tmp)
            print(f"--- Modelo {name} pronto! ---")
        else:
            print(f"Modelo {name} já existe localmente.")


def vosk_rec_min(audio_file: BytesIO) -> str:
    MODEL_PATH = "Modelos/Vosk/vosk-model-small-pt-0.3"

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
    text = ""

    try:
        with sr.AudioFile(audio) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data, language="pt-BR")

    except sr.UnknownValueError:
        text = "Erro: Áudio não compreendido"
    except sr.RequestError as e:
        if "internet connection" in str(e).lower() or "network" in str(e).lower():
            text = "Erro: Conexão com a Internet perdida durante o reconhecimento"
        else:
            text = f"Erro ao acessar o serviço: {e}"

    return text

if __name__ == "__main__":
    # Teste rápido
    with open("teste.wav", "rb") as f:
        audio_bytes = f.read()
    
    audio_io = BytesIO(audio_bytes)
    resultado = vosk_rec(audio_io)
    resultado2 = vosk_rec_min(audio_io)
    print("Vosk Resultado:", resultado)
    print("Vosk Min Resultado:", resultado2)
    
    audio_io.seek(0)
    resultado_sr = speech_rec(audio_io)
    print("SpeechRecognition Resultado:", resultado_sr)