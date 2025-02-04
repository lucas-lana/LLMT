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

def texto(sub_audio: any,escolha_modelos) -> list:
        
    if escolha_modelos == "1":
        vosk_min_result, vosk_min_time = measure_time(tc.vosk_rec_min, sub_audio)
        vosk_min_text = f"{separa_linha(vosk_min_result)}\n"
        return vosk_min_text, vosk_min_time
    
    elif escolha_modelos == "2":
        vosk_result, vosk_time = measure_time(tc.vosk_rec, sub_audio)
        vosk_max_text = f"{separa_linha(vosk_result)}\n"
        return vosk_max_text, vosk_time
    
    elif escolha_modelos == "4":
        speech_result, speech_time = measure_time(tc.speech_rec, sub_audio)
        speech_text = f"{separa_linha(speech_result)}\n"
        return speech_text, speech_time
    
    elif escolha_modelos == "3":
        vosk_min_result, vosk_min_time = measure_time(tc.vosk_rec_min, sub_audio)
        vosk_min_text = f"{separa_linha(vosk_min_result)}\n"

        vosk_result, vosk_time = measure_time(tc.vosk_rec, sub_audio)
        vosk_max_text = f"{separa_linha(vosk_result)}\n"
        
        return vosk_min_text, vosk_max_text, vosk_min_time,vosk_time
    
    elif escolha_modelos == "5":
        vosk_min_result, vosk_min_time = measure_time(tc.vosk_rec_min, sub_audio)
        vosk_min_text = f"{separa_linha(vosk_min_result)}\n"

        speech_result, speech_time = measure_time(tc.speech_rec, sub_audio)
        speech_text = f"{separa_linha(speech_result)}\n"
        
        return vosk_min_text, speech_text, vosk_min_time,speech_time
    
    elif escolha_modelos == "6":
        vosk_result, vosk_time = measure_time(tc.vosk_rec, sub_audio)
        vosk_max_text = f"{separa_linha(vosk_result)}\n"

        speech_result, speech_time = measure_time(tc.speech_rec, sub_audio)
        speech_text = f"{separa_linha(speech_result)}\n"
        
        return vosk_max_text, speech_text, vosk_time,speech_time
    
    else :
        vosk_min_result, vosk_min_time = measure_time(tc.vosk_rec_min, sub_audio)
        vosk_min_text = f"{separa_linha(vosk_min_result)}\n"

        vosk_result, vosk_time = measure_time(tc.vosk_rec, sub_audio)
        vosk_max_text = f"{separa_linha(vosk_result)}\n"

        speech_result, speech_time = measure_time(tc.speech_rec, sub_audio)
        speech_text = f"{separa_linha(speech_result)}\n"
    
        return vosk_min_text, vosk_max_text, speech_text,vosk_min_time,vosk_time,speech_time        
        
    ##arquivo = caminho[:caminho.rfind('.')]
    ##create_file(texto, arquivo)

def separa_linha(resultado_modelo: str) -> str:
    texto_resultado = ''
    tamanho_texto = len(resultado_modelo)
    i = 0 

    while i < tamanho_texto:
        j = min(i + 124, tamanho_texto)

        if j < tamanho_texto:
            while j > i and resultado_modelo[j] != ' ':
                j -= 1

        texto_resultado += resultado_modelo[i:j].strip() + "\n"
        i = j + 1

    return texto_resultado.strip()