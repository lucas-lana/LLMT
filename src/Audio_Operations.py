from pydub import AudioSegment
from io import BytesIO
import wave

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

def convert_to_vosk(input_audio: BytesIO, format: str) -> BytesIO:
    """
    Converte um áudio para um formato compatível com o Vosk (16 kHz, mono, 16 bits).
    
    :param input_audio: Objeto BytesIO contendo o áudio de entrada.
    :param format: Formato do áudio de entrada (e.g., "mp3", "wav", "flac").
    :return: Objeto BytesIO contendo o áudio convertido para o formato compatível com o Vosk.
    """
    # Converte o áudio para WAV
    wav_audio = convert_to_wav(input_audio, format)
    
    # Converte o áudio para 16 bits
    audio_16bit = convert_to_16bit(wav_audio, "wav")
    
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
    with wave.open(audio_file, "rb") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)
    return duration