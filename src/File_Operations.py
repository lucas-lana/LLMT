import io
import os
import zipfile
import tempfile
import Audio_Operations as ao

def trata_arquivo(lista_arquivos):
    lista_formatos = ["mp3", "ogg", "flac", "wav"]
    lista_formatos_videos = ["mp4", "avi", "mov", "mkv"]
    
    nova_lista_arquivos = []
    lista_avisos = []
    
    tempo_processamento = 0
    tempo_processamento_total = 0

    if not lista_arquivos:
        return 0, [], []

    for caminho_completo in lista_arquivos:
        # Verificação Nível 1: Se não existe agora, pula silenciosamente
        if not os.path.exists(caminho_completo):
            continue

        arquivo = os.path.basename(caminho_completo)
        
        try:
            formato = ao.reconhece_formato(arquivo)
        except:
            formato = arquivo.split('.')[-1].lower() if '.' in arquivo else ""
        
        # 1. ARQUIVOS NÃO SUPORTADOS
        if formato not in lista_formatos and formato not in lista_formatos_videos:
            msg = f"⚠️ O arquivo '{arquivo}' não é suportado (formato: {formato})."
            # Printa no console para debug, mas guarda a mensagem limpa
            print(f"{msg}")
            lista_avisos.append(msg)
            try:
                if os.path.exists(caminho_completo):
                    os.remove(caminho_completo)
            except:
                pass
            continue
            
        # 2. CONVERSÃO DE VÍDEOS
        if formato in lista_formatos_videos:
            # Verificação Nível 2: Garante que o arquivo ainda está lá antes de converter
            if not os.path.exists(caminho_completo):
                continue
                
            try:
                audio = ao.convert_video_to_audio(caminho_completo)
                if isinstance(audio, io.BytesIO): audio_bytes = audio.getvalue()
                else: audio_bytes = audio
                
                if os.path.exists(caminho_completo):
                    os.remove(caminho_completo)
                
                novo_nome = os.path.splitext(caminho_completo)[0] + "_video.wav"
                
                with open(novo_nome, "wb") as novo_arquivo:
                    novo_arquivo.write(audio_bytes)
                
                nova_lista_arquivos.append(novo_nome)
            except Exception as e:
                # Se o erro for "arquivo não encontrado", é bug de concorrência. Ignora.
                if "No such file" in str(e):
                    continue
                    
                print(f"Erro técnico ao converter vídeo '{arquivo}': {e}")
                msg = f"❌ Erro ao converter o vídeo '{arquivo}'" # Mensagem limpa
                lista_avisos.append(msg)
            continue
        
        # 3. PROCESSAMENTO DE ÁUDIOS
        try:
            tempo_processamento = ao.get_duration_audio(caminho_completo)
        except:
            tempo_processamento = 0
            
        print(f"Duração {arquivo}: {tempo_processamento}")
        
        if formato != "wav":
            # Verificação Nível 2: Garante que o arquivo ainda está lá
            if not os.path.exists(caminho_completo):
                continue

            try:
                audio = ao.convert_to_wav(caminho_completo, formato)
                if isinstance(audio, io.BytesIO): audio_bytes = audio.getvalue()
                else: audio_bytes = audio
                
                if os.path.exists(caminho_completo):
                    os.remove(caminho_completo)
                
                novo_nome = os.path.splitext(caminho_completo)[0] + ".wav"
                
                with open(novo_nome, "wb") as novo_arquivo:
                    novo_arquivo.write(audio_bytes)
                
                nova_lista_arquivos.append(novo_nome)
            except Exception as e:
                # Ignora erros de arquivo sumindo (corrida)
                if "No such file" in str(e):
                    continue

                print(f"Erro técnico ao converter áudio '{arquivo}': {e}")
                msg = f"❌ Erro ao converter o áudio '{arquivo}'" # Mensagem limpa
                lista_avisos.append(msg)
        else:
            nova_lista_arquivos.append(caminho_completo)
        
        tempo_processamento_total += tempo_processamento

    return tempo_processamento_total, nova_lista_arquivos, lista_avisos

def transcrever_individual(caminho_arquivo, escolha_modelos, prompt):
    """
    Processa um único arquivo de áudio e retorna o caminho do arquivo de texto gerado.
    """
    arquivo = os.path.basename(caminho_arquivo)
    print(f"Iniciando transcrição de: {arquivo}")
    
    # Define o nome do arquivo de saída
    nome_arquivo_texto = os.path.splitext(arquivo)[0] + "_Transcrição.txt"
    
    try:
        # Chama a transcrição (Audio_Operations)
        texto = ao.transcrever_audio(caminho_arquivo, arquivo, str(escolha_modelos), prompt)
        
        # Cria o arquivo temporário .txt
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w', encoding='utf-8') as tmp_file:
            tmp_file.write(texto)
            # Renomeia o arquivo temporário para ter o nome bonito que queremos exibir
            caminho_final = os.path.join(tempfile.gettempdir(), nome_arquivo_texto)
            
        # Move/Renomeia para o caminho final legível
        if os.path.exists(caminho_final):
            os.remove(caminho_final)
        os.rename(tmp_file.name, caminho_final)
        
        return caminho_final

    except Exception as e:
        print(f"Erro ao transcrever individualmente {arquivo}: {e}")
        return None

def compactar_em_zip(arquivos_temporarios, nome_arquivo_zip):
    with zipfile.ZipFile(nome_arquivo_zip, 'w') as zipf:
        for nome_arquivo, caminho in arquivos_temporarios:
            zipf.write(caminho, arcname=nome_arquivo)
    return nome_arquivo_zip