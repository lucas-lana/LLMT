from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import Text_Operations as tx
from io import BytesIO
import os

def convert_video_to_audio(video_file: str) -> BytesIO:
    """
    Converte um vídeo para áudio.
    
    :param video_file: Caminho do arquivo de vídeo.
    :return: Objeto BytesIO contendo o áudio extraído do vídeo.
    """
    # Lê o arquivo de vídeo
    video = VideoFileClip(video_file)
    
    # Extrai o áudio
    audio = video.audio
    
    # Salva o áudio temporariamente em um arquivo WAV
    audio.write_audiofile("temp_audio.wav", codec='pcm_s16le')
    
    # Fecha o vídeo para liberar recursos
    video.close()
    
    # Carrega o áudio usando pydub
    audio_segment = AudioSegment.from_wav("temp_audio.wav")
    
    # Cria um buffer para o áudio
    audio_buffer = BytesIO()
    audio_segment.export(audio_buffer, format="wav")
    audio_buffer.seek(0)  # Retorna o cursor para o início do buffer
    
    # Remove o arquivo temporário
    os.remove("temp_audio.wav")
    
    return audio_buffer

def convert_to_wav(input_audio: BytesIO, format: str) -> BytesIO:
    """
    Converte um áudio para o formato WAV.
    
    :param input_audio: Objeto BytesIO contendo o áudio de entrada.
    :param format: Formato do áudio de entrada (e.g., "mp3", "ogg", "flac").
    :return: Objeto BytesIO contendo o áudio convertido para WAV.
    """
    # Lê o áudio de entrada
    audio = AudioSegment.from_file(input_audio, format=format)
    
    # Cria um buffer para o áudio WAV
    wav_audio = BytesIO()
    audio.export(wav_audio, format="wav")
    wav_audio.seek(0)  # Retorna o cursor para o início do buffer
    
    return wav_audio


def convert_to_16bit(input_audio: BytesIO, format: str) -> BytesIO:
    """
    Converte um áudio para 16 bits.

    :param input_audio: Objeto BytesIO contendo o áudio de entrada.
    :param format: Formato do áudio de entrada (e.g., "mp3", "ogg", "flac").
    :return: Objeto BytesIO contendo o áudio convertido para 16 bits.
    """
    # Lê o áudio de entrada
    audio = AudioSegment.from_file(input_audio, format=format)
    
    # Converte para 16 bits
    audio_16bit = audio.set_sample_width(2)  # 16 bits = 2 bytes
    
    # Exporta para um buffer
    output_audio = BytesIO()
    audio_16bit.export(output_audio, format="wav")
    output_audio.seek(0)  # Retorna o cursor para o início do buffer
    
    return output_audio


def convert_audio_channels(input_audio: BytesIO, format: str, target_channels: int) -> BytesIO:
    """
    Converte um áudio para mono ou estéreo.

    :param input_audio: Objeto BytesIO contendo o áudio de entrada.
    :param format: Formato do áudio de entrada (e.g., "mp3", "wav", "flac").
    :param target_channels: Número de canais desejados (1 para mono, 2 para estéreo).
    :return: Objeto BytesIO contendo o áudio com os canais convertidos.
    """
    # Lê o áudio de entrada
    audio = AudioSegment.from_file(input_audio, format=format)
    
    # Converte para o número de canais desejado
    if target_channels == 1:
        converted_audio = audio.set_channels(1)  # Converte para mono
    elif target_channels == 2:
        converted_audio = audio.set_channels(2)  # Converte para estéreo
    else:
        raise ValueError("Número de canais inválido. Use 1 (mono) ou 2 (estéreo).")
    
    # Exporta para um buffer
    output_audio = BytesIO()
    converted_audio.export(output_audio, format="wav")
    output_audio.seek(0)  # Retorna o cursor para o início do buffer
    
    return output_audio


def convert_to_16khz(input_audio: BytesIO, format: str) -> BytesIO:
    """
    Converte um áudio para 16 kHz de taxa de amostragem.

    :param input_audio: Objeto BytesIO contendo o áudio de entrada.
    :param format: Formato do áudio de entrada (e.g., "mp3", "wav", "flac").
    :return: Objeto BytesIO contendo o áudio convertido para 16 kHz.
    """
    # Lê o áudio de entrada
    audio = AudioSegment.from_file(input_audio, format=format)
    
    # Ajusta a taxa de amostragem para 16 kHz
    audio_16khz = audio.set_frame_rate(16000)
    
    # Exporta para um buffer
    output_audio = BytesIO()
    audio_16khz.export(output_audio, format="wav")
    output_audio.seek(0)  # Retorna o cursor para o início do buffer
    
    return output_audio

def convert_to_vosk(input_audio: BytesIO) -> BytesIO:
    """
    Converte um áudio para um formato compatível com o Vosk (16 kHz, mono, 16 bits).
    
    :param input_audio: Objeto BytesIO contendo o áudio de entrada.
    :return: Objeto BytesIO contendo o áudio convertido para o formato compatível com o Vosk.
    """
    
    # Converte o áudio para 16 bits
    audio_16bit = convert_to_16bit(input_audio, "wav")
    
    # Converte o áudio para mono
    mono_audio = convert_audio_channels(audio_16bit, "wav", 1)
    
    # Converte o áudio para 16 kHz
    audio_16khz = convert_to_16khz(mono_audio, "wav")
    
    return audio_16khz

def reconhece_formato(caminho: str) -> str:
    """
    Reconhece o formato do arquivo
    
    :caminho: O caminho do arquivo
    :return: o formato do arquivo
    """
    partes = caminho.split(".")
    return partes[-1]

def get_audio_duration(audio_file: str) -> float:
    with tx.mr.wave.open(audio_file, "rb") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)
    return duration

def get_duration_audio(file_path: str) -> float:
    audio = AudioSegment.from_file(file_path)
    return len(audio) / 1000  # Converte de milissegundos para segundos


def transcrever_audio(caminho_arquivo: str, arquivo: str, escolha_modelos,prompt) -> str:
    vosk_min_text = "Vosk Simple Model: \n"
    vosk_max_text = "Vosk Complete Model: \n"
    speech_text = "Speech Recognition: \n"
    vosk_min_time = 0
    vosk_max_time = 0
    speech_time = 0
    
    # Convertendo o áudio para um formato compatível com o Vosk (BytesIO)
    audio = convert_to_vosk(caminho_arquivo)
    
    # Converte BytesIO para AudioSegment
    audio_segment = AudioSegment.from_file(audio)
    duracao = len(audio_segment)
    
    if "--ND" in prompt:
        lista_partes = tx.texto(audio,escolha_modelos)
        if len(lista_partes) == 4:
            if escolha_modelos == "3":
                vosk_min_text += str(lista_partes[0])
                vosk_max_text += str(lista_partes[1])
                vosk_min_time += float(lista_partes[2]) 
                vosk_max_time += float(lista_partes[3])

            elif escolha_modelos == "5":
                vosk_min_text += str(lista_partes[0])
                speech_text += str(lista_partes[1])
                vosk_min_time += float(lista_partes[2])
                speech_time += float(lista_partes[3])

            else:
                vosk_max_text += str(lista_partes[0])
                speech_text += str(lista_partes[1])
                vosk_max_time += float(lista_partes[2])
                speech_time += float(lista_partes[3])

        elif len(lista_partes) == 2:
            if escolha_modelos == "1":
                vosk_min_text += str(lista_partes[0])
                vosk_min_time += float(lista_partes[1])

            elif escolha_modelos == "2":
                vosk_max_text += str(lista_partes[0])
                vosk_max_time += float(lista_partes[1])

            elif escolha_modelos == "4":
                speech_text += str(lista_partes[0])
                speech_time += float(lista_partes[1])

        else:
            vosk_min_text += str(lista_partes[0])
            vosk_max_text += str(lista_partes[1])
            speech_text += str(lista_partes[2])
            vosk_min_time += float(lista_partes[3]) 
            vosk_max_time += float(lista_partes[4]) 
            speech_time += float(lista_partes[5])
        
        
    else:
        max_duracao = 3 * 60 * 1000  # Máximo de 3 minutos por parte
        qtd_partes = (duracao // max_duracao) + (1 if (duracao % max_duracao) > 0 else 0)

        for parte in range(qtd_partes):
            lista_partes = []

            inicio = parte * max_duracao
            fim = min((parte + 1) * max_duracao, duracao)

            # Obtém a parte do áudio como um AudioSegment
            parte_atual = audio_segment[inicio:fim]

            # Converte a parte atual para BytesIO antes de passar para a função de transcrição
            parte_atual_io = BytesIO()
            parte_atual.export(parte_atual_io, format="wav")
            parte_atual_io.seek(0)

            # Passa a parte para a função de transcrição
            lista_partes = tx.texto(parte_atual_io,escolha_modelos)
            if len(lista_partes) == 4:
                if escolha_modelos == "3":
                    vosk_min_text += str(lista_partes[0])
                    vosk_max_text += str(lista_partes[1])
                    vosk_min_time += float(lista_partes[2]) 
                    vosk_max_time += float(lista_partes[3])

                elif escolha_modelos == "5":
                    vosk_min_text += str(lista_partes[0])
                    speech_text += str(lista_partes[1])
                    vosk_min_time += float(lista_partes[2])
                    speech_time += float(lista_partes[3])

                else:
                    vosk_max_text += str(lista_partes[0])
                    speech_text += str(lista_partes[1])
                    vosk_max_time += float(lista_partes[2])
                    speech_time += float(lista_partes[3])

            elif len(lista_partes) == 2:
                if escolha_modelos == "1":
                    vosk_min_text += str(lista_partes[0])
                    vosk_min_time += float(lista_partes[1])

                elif escolha_modelos == "2":
                    vosk_max_text += str(lista_partes[0])
                    vosk_max_time += float(lista_partes[1])

                elif escolha_modelos == "4":
                    speech_text += str(lista_partes[0])
                    speech_time += float(lista_partes[1])

            else:
                vosk_min_text += str(lista_partes[0])
                vosk_max_text += str(lista_partes[1])
                speech_text += str(lista_partes[2])
                vosk_min_time += float(lista_partes[3]) 
                vosk_max_time += float(lista_partes[4]) 
                speech_time += float(lista_partes[5])

            #print(vosk_min_text)
            #print("\n")
            #print(vosk_max_text)
            #print("\n")
            #print(speech_text)
    
    
    if prompt == "":
        Prompt = "A partir apenas das transcrições geradas pelos modelos, combine as transcrições a fim de gerar um texto fusão sendo o mais coerente e fiel as informações dos textos:" 
    elif prompt == "--ND":
        Prompt = "A partir apenas das transcrições geradas pelos modelos, combine as transcrições a fim de gerar um texto fusão sendo o mais coerente e fiel as informações dos textos:"
    elif "--ND" in prompt:
        Prompt = prompt.replace("--ND","")+":"
    else:
        Prompt = prompt+":"
    
    texto = Prompt+"\n\n\nTestes do arquivo: " + arquivo + "\n" + "Duração: " 
    texto += f"{get_audio_duration(caminho_arquivo):.2f}\n"+ '-'*50 + "\n" 
    
    if escolha_modelos == "1":
        texto += vosk_min_text +f"(Tempo: {vosk_min_time:.2f} segundos)" + "\n"
        
    elif escolha_modelos == "2":
        texto += vosk_max_text +f"(Tempo: {vosk_max_time:.2f} segundos)" + "\n"
        
    elif escolha_modelos == "4":
        texto += speech_text + f"(Tempo: {speech_time:.2f} segundos)" + "\n"
        
    elif escolha_modelos == "3":
        texto += vosk_min_text +f"(Tempo: {vosk_min_time:.2f} segundos)" + "\n\n" + vosk_max_text +f"(Tempo: {vosk_max_time:.2f} segundos)" + "\n"
        
    elif escolha_modelos == "5":
        texto += vosk_min_text +f"(Tempo: {vosk_min_time:.2f} segundos)" + "\n\n" + speech_text + f"(Tempo: {speech_time:.2f} segundos)" + "\n"
        
    elif escolha_modelos == "6":
        texto += vosk_max_text +f"(Tempo: {vosk_max_time:.2f} segundos)" + "\n\n" + speech_text + f"(Tempo: {speech_time:.2f} segundos)" + "\n"
        
    else:
        texto += vosk_min_text +f"(Tempo: {vosk_min_time:.2f} segundos)" + "\n\n" + vosk_max_text +f"(Tempo: {vosk_max_time:.2f} segundos)" + "\n\n" +speech_text + f"(Tempo: {speech_time:.2f} segundos)" + "\n"
    
    
    return texto