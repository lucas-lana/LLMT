import time
import Transcription as tc

def create_file(texto: str, nome_arquivo: str):
    nome_arquivo += ".txt"
    with open(nome_arquivo, "w") as file:
        file.write(texto)

def measure_time(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return result, elapsed_time

def texto(sub_audio: any) -> list:
    
    vosk_min_result, vosk_min_time = measure_time(tc.vosk_rec_min, sub_audio)
    vosk_min_text = f"{vosk_min_result} (Tempo: {vosk_min_time:.2f} segundos)\n\n"
    
    vosk_result, vosk_time = measure_time(tc.vosk_rec, sub_audio)
    vosk_max_text = f"{vosk_result} (Tempo: {vosk_time:.2f} segundos)\n\n"
    
    speech_result, speech_time = measure_time(tc.speech_rec, sub_audio)
    speech_text = f"{speech_result} (Tempo: {speech_time:.2f} segundos)\n\n"
    
    return vosk_min_text, vosk_max_text, speech_text
    
    ##arquivo = caminho[:caminho.rfind('.')]
    ##create_file(texto, arquivo)