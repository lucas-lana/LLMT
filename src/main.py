import sys
import File_Operations as fo

if __name__ == "__main__":
    # Verifica se os argumentos necessários foram passados
    if len(sys.argv) < 3:
        print("Uso: python3 script.py <caminho_da_pasta_mae> <caminho_da_pasta_destino>")
        print("O caminho da pasta deve ser entre aspas duplas.")
    else:
        # Captura os argumentos da linha de comando
        pasta_origem = sys.argv[1]
        pasta_destino = sys.argv[2]
        
        
        arquivos_n_sup = fo.trata_arquivo(pasta_origem)

        # Chama a função para renomear os arquivos
        fo.acessa_arquivos(pasta_origem, pasta_destino,arquivos_n_sup)