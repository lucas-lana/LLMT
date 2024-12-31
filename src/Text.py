import time
import Transcription as tc
import Audio_Operations as ao

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

def texto(caminho: str, nome_arquivo:str) -> str:
    
    texto = "Testes do arquivo: " + nome_arquivo + "\n"
    texto += f"Duração do aúdio: {ao.get_audio_duration(caminho):.2f}\n" + '-'*50 + "\n\n"
    
    vosk_min_result, vosk_min_time = measure_time(tc.vosk_rec_min, caminho)
    texto += f"Vosk Simple Model: {vosk_min_result} (Tempo: {vosk_min_time:.2f} segundos)\n\n"
    
    vosk_result, vosk_time = measure_time(tc.vosk_rec, caminho)
    texto += f"Vosk Complete Model: {vosk_result} (Tempo: {vosk_time:.2f} segundos)\n\n"
    
    speech_result, speech_time = measure_time(tc.speech_rec, caminho)
    texto += f"Speech Recognition: {speech_result} (Tempo: {speech_time:.2f} segundos)\n\n" + '-'*50
    return texto
    
    ##arquivo = caminho[:caminho.rfind('.')]
    ##create_file(texto, arquivo)