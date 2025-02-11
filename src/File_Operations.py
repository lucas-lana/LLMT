import io
import os
import sys
import requests
import Audio_Operations as ao


def check_internet_connection(url='http://www.google.com/', timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False
    

def trata_arquivo(pasta_mae) :
    lista_formatos = ["mp3", "ogg", "flac","wav"]
    #lista_formatos_videos = ["mp4", "avi", "mov", "mkv"]
    lista_nao_suportados = []
    tempo_processamento = 0
    tempo_processamento_total = 0
    
    if not os.path.isdir(pasta_mae):
        print(f"Erro: A pasta '{pasta_mae}' não foi encontrada.")
        return
    
    for raiz, subpastas, arquivos in os.walk(pasta_mae):
        for arquivo in arquivos:
            caminho_completo = os.path.join(raiz, arquivo)
            formato = ao.reconhece_formato(arquivo)
            
            if formato not in lista_formatos: #and formato not in lista_formatos_videos:
                print(f"Formato do arquivo '{arquivo}' não suportado.")
                lista_nao_suportados.append(arquivo)
                continue
            
            #if formato in lista_formatos_videos:
            #    print(f"Arquivo '{arquivo}' é um vídeo e não será processado.")
            #    ao.extract_audio_from_video(caminho_completo)
            #    lista_nao_suportados.append(arquivo)
            #    continue
            
            tempo_processamento = ao.get_duration_audio(caminho_completo)
            print(f"Tempo de duração do {arquivo}: {tempo_processamento}")
            
            if formato != "wav":
                try:
                    # Converte o arquivo para WAV
                    audio = ao.convert_to_wav(caminho_completo, formato)
                    
                    # Verifica se 'audio' é um objeto BytesIO, caso sim, obtém os bytes
                    if isinstance(audio, io.BytesIO):
                        audio_bytes = audio.getvalue()
                    else:
                        audio_bytes = audio
                    
                    # Remove o arquivo original
                    os.remove(caminho_completo)
                    print(f"Arquivo original '{arquivo}' foi excluído.")
                    
                    # Cria um novo arquivo WAV com o mesmo nome
                    novo_nome = os.path.splitext(caminho_completo)[0] + ".wav"
                    with open(novo_nome, "wb") as novo_arquivo:
                        novo_arquivo.write(audio_bytes)
                    
                    print(f"Novo arquivo WAV '{novo_nome}' foi criado.")
                except Exception as e:
                    print(f"Erro ao processar o arquivo '{arquivo}': {e}")
            
            
            tempo_processamento_total += tempo_processamento
        print(f"Tempo de processamento total: {tempo_processamento_total}")        
                    
    return lista_nao_suportados,tempo_processamento_total
                
        

def acessa_arquivos(pasta_mae,pasta_destino,arquivos_n_sup,escolha_modelos):
    # Verifica se a pasta existe
    if not os.path.isdir(pasta_mae):
        print(f"Erro: A pasta '{pasta_mae}' não foi encontrada.")
        return

    # Percorre a pasta mãe e todas as subpasta e arquivos
    for raiz, subpastas, arquivos in os.walk(pasta_mae):
        for arquivo in arquivos:
            # Procedimento do que fazer com os arquivos
            print(f"Arquivo: {arquivo}")
            
            if arquivo in arquivos_n_sup:
                continue
            
            caminho_arquivo = os.path.join(raiz, arquivo)
            
            if ((escolha_modelos == "0" or escolha_modelos == "7" or escolha_modelos == "4" or escolha_modelos == "5" or escolha_modelos == "6") and check_internet_connection() == False):
                print("Erro: Não é possível utilizar o modelo Speech sem conexão com a internet.")
                print("Trascrevendo o arquivo '" + arquivo +  "' sem o modelo Speech.")
        
                if escolha_modelos == "4":
                    print("Escolhido apenas o modelo Speech.")
                    print("Parando a execução do programa.")
                    sys.exit()

                elif escolha_modelos == "5":
                    print("Executando apenas com o modelo Vosk mínimo")
                    escolha_modelos = "1"

                elif escolha_modelos == "6":
                    print("Executando apenas com o modelo Vosk máximo")
                    escolha_modelos = "2"

                else:
                    print("Executando modelos Vosk.")
                    escolha_modelos = "3"
            
            # Tratar o nome do arquivo
            nome_arquivo_texto = caminho_arquivo[:caminho_arquivo.rfind('.')] + "_Transcrição.txt"
            
            # Trasncreve o áudio
            texto = ao.transcrever_audio(caminho_arquivo, arquivo,escolha_modelos)
                  
            # Crie a pasta de destino se ela não existir
            if not os.path.exists(pasta_destino):
                os.makedirs(pasta_destino)
            
            # Caminho completo para o arquivo de texto na pasta de destino
            caminho_arquivo_texto_destino = os.path.join(pasta_destino, os.path.basename(nome_arquivo_texto))
            
            with open(caminho_arquivo_texto_destino, 'w') as f:
                f.write(texto)
    
