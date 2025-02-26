import io
import os
import zipfile
import tempfile
import Audio_Operations as ao
    

def trata_arquivo(lista_arquivos) :
    lista_formatos = ["mp3", "ogg", "flac","wav"]
    lista_formatos_videos = ["mp4", "avi", "mov", "mkv"]
    nova_lista_arquivos = []
    tempo_processamento = 0
    tempo_processamento_total = 0

    
    for caminho_completo in lista_arquivos:
        arquivo = (caminho_completo.split("/"))[4]
        formato = ao.reconhece_formato(arquivo)
        
        if formato not in lista_formatos and formato not in lista_formatos_videos: #and formato not in lista_formatos_videos:
            print(f"Formato do arquivo '{arquivo}' não suportado.")
            continue
            
        if formato in lista_formatos_videos:
            try :
                # Converte o arquivo para WAV
                audio = ao.convert_video_to_audio(caminho_completo)
                
                # Verifica se 'audio' é um objeto BytesIO, caso sim, obtém os bytes
                if isinstance(audio, io.BytesIO):
                    audio_bytes = audio.getvalue()
                else:
                    audio_bytes = audio
                
                # Remove o arquivo original
                os.remove(caminho_completo)
                print(f"Arquivo original '{arquivo}' foi excluído.")
                
                # Cria um novo arquivo WAV com o mesmo nome
                novo_nome = os.path.splitext(caminho_completo)[0] + "_video.wav"
                with open(novo_nome, "wb") as novo_arquivo:
                    novo_arquivo.write(audio_bytes)
                
                print(f"Novo arquivo WAV '{novo_nome}' foi criado.")
            except Exception as e:
                print(f"Erro ao processar o arquivo '{arquivo}': {e}")
            
            nova_lista_arquivos.append(novo_nome)
            continue
        
        
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
            
            nova_lista_arquivos.append(novo_nome)
        else:
            nova_lista_arquivos.append(caminho_completo)
        
        
        tempo_processamento_total += tempo_processamento
    print(f"Tempo de processamento total: {tempo_processamento_total}")                     
    return tempo_processamento_total,nova_lista_arquivos
                
        

def acessa_arquivos(lista_arquivos,escolha_modelos,prompt):

    arquivos_temporarios = {}
    # Percorre a pasta mãe e todas as subpasta e arquivos
    for caminho_arquivo in lista_arquivos:
        arquivo = (caminho_arquivo.split("/"))[4]
        # Procedimento do que fazer com os arquivos
        print(f"Arquivo: {arquivo}")    
            
        # Tratar o nome do arquivo
        nome_arquivo_texto = arquivo[:arquivo.rfind('.')] + "_Transcrição.txt"
        
        # Trasncreve o áudio
        texto = ao.transcrever_audio(caminho_arquivo,arquivo,str(escolha_modelos),prompt)

        # Salvar o texto em um arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w', encoding='utf-8') as tmp_file:
            tmp_file.write(texto)
            arquivos_temporarios[nome_arquivo_texto] = tmp_file.name
    
    return arquivos_temporarios

def compactar_em_zip(arquivos_temporarios, nome_arquivo_zip):
    # Criar um arquivo ZIP
    with zipfile.ZipFile(nome_arquivo_zip, 'w') as zipf:
        for nome_arquivo, caminho in arquivos_temporarios.items():
            zipf.write(caminho, arcname=nome_arquivo)
    
    return nome_arquivo_zip