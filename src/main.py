import sys
import File_Operations as fo

if __name__ == "__main__":
    # Verifica se os argumentos necessários foram passados
    if len(sys.argv) < 3:
        print("Uso: python3 script.py <caminho_da_pasta_mae> <caminho_da_pasta_destino>")
        print("O caminho da pasta deve ser entre aspas duplas.")
    
    elif len(sys.argv) == 3 or len(sys.argv) == 4:
        # Captura os argumentos da linha de comando
        pasta_origem = sys.argv[1]
        pasta_destino = sys.argv[2]
        
        
        if len(sys.argv) == 4:
            escolha_modelos = sys.argv[3]
        else:
            escolha_modelos = "0"
        
        # Modo de escolha de modelos
        # 1 - Vosk mínimo
        # 2 - Vosk máximo
        # 3 - Vosk mínimo e máximo
        # 4 - Speech
        # 5 - Vosk mínimo e Speech
        # 6 - Vosk máximo e Speech
        # Else - Todos os modelos
        
        arquivos_n_sup = fo.trata_arquivo(pasta_origem)

        # Chama a função para renomear os arquivos
        fo.acessa_arquivos(pasta_origem, pasta_destino,arquivos_n_sup,escolha_modelos)
        
    else:
        print("Erro: Foram passados argumentos demais.")
        print("Uso: python3 script.py <caminho_da_pasta_mae> <caminho_da_pasta_destino>")
        print("O caminho da pasta deve ser entre aspas duplas.")
        
        