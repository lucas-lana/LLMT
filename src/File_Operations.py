import io
import os
import sys
import Text as tx

def trata_arquivo(pasta_mae) -> list:
    lista_formatos = ["mp3", "ogg", "flac","wav"]
    lista_nao_suportados = []
    
    if not os.path.isdir(pasta_mae):
        print(f"Erro: A pasta '{pasta_mae}' não foi encontrada.")
        return
    
    for raiz, subpastas, arquivos in os.walk(pasta_mae):
        for arquivo in arquivos:
            caminho_completo = os.path.join(raiz, arquivo)
            formato = tx.ao.reconhece_formato(arquivo)
            
            if formato not in lista_formatos:
                print(f"Formato do arquivo '{arquivo}' não suportado.")
                lista_nao_suportados.append(arquivo)
                continue
            
            if formato != "wav":
                try:
                    # Converte o arquivo para WAV
                    audio = tx.ao.convert_to_wav(caminho_completo, formato)
                    
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
    return lista_nao_suportados

                
        

def acessa_arquivos(pasta_mae,pasta_destino,arquivos_n_sup):
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
            
            # Tratar o nome do arquivo
            nome_arquivo_texto = caminho_arquivo[:caminho_arquivo.rfind('.')] + "_Transcrição.txt"
            
            
            # Subdividir audios maiores de 3 minutos
            # Subdividir audios maiores de 3 minutos
            # Subdividir audios maiores de 3 minutos
            
            # Mexer no arquivo original (Audio)
            texto = str(tx.texto(caminho_arquivo, caminho_arquivo))
            
            
            # Crie a pasta de destino se ela não existir
            if not os.path.exists(pasta_destino):
                os.makedirs(pasta_destino)
            
            # Caminho completo para o arquivo de texto na pasta de destino
            caminho_arquivo_texto_destino = os.path.join(pasta_destino, os.path.basename(nome_arquivo_texto))
            
            with open(caminho_arquivo_texto_destino, 'w') as f:
                f.write(texto)
    
            

if __name__ == "__main__":
    # Verifica se os argumentos necessários foram passados
    if len(sys.argv) < 3:
        print("Uso: python3 script.py <caminho_da_pasta_mae> <caminho_da_pasta_destino>")
        print("O caminho da pasta deve ser entre aspas duplas.")
    else:
        # Captura os argumentos da linha de comando
        pasta_origem = sys.argv[1]
        pasta_destino = sys.argv[2]
        
        
        arquivos_n_sup = trata_arquivo(pasta_origem)

        # Chama a função para renomear os arquivos
        acessa_arquivos(pasta_origem, pasta_destino,arquivos_n_sup)
