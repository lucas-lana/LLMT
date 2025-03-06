#!/bin/bash

# Verifica se o script está sendo executado com privilégios de superusuário
if [ "$EUID" -ne 0 ]; then
    echo "Este script requer privilégios de superusuário. Execute com sudo."
    exit 1
fi

# Verifica se o sistema é baseado em Debian/Ubuntu
if [ ! -f /etc/os-release ]; then
    echo "Este script só é compatível com sistemas baseados em Debian/Ubuntu."
    exit 1
fi

# Função para exibir mensagens de erro e sair
erro() {
    echo "ERRO: $1"
    exit 1
}

# Verifica se o Python 3.11 está instalado
if ! command -v python3.11 &> /dev/null; then
    echo "Python 3.11 não está instalado. Instalando..."
    # Adiciona o repositório deadsnakes para Ubuntu/Debian
    sudo apt-get update || erro "Falha ao atualizar os repositórios."
    sudo apt-get install -y software-properties-common || erro "Falha ao instalar 'software-properties-common'."
    sudo add-apt-repository -y ppa:deadsnakes/ppa || erro "Falha ao adicionar o repositório 'deadsnakes/ppa'."
    sudo apt-get update || erro "Falha ao atualizar os repositórios após adicionar o PPA."
    # Instala o Python 3.11
    sudo apt-get install -y python3.11 python3.11-distutils || erro "Falha ao instalar Python 3.11."
else
    echo "Python 3.11 já está instalado."
fi

# Verifica se o pip está instalado
if ! python3.11 -m pip --version &> /dev/null; then
    echo "Instalando pip..."
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11 || erro "Falha ao instalar pip."
fi

# Atualiza o pip
echo "Atualizando pip..."
python3.11 -m pip install --upgrade pip || erro "Falha ao atualizar pip."

# Instala dependências do sistema para PyAudio e Vosk
echo "Instalando dependências do sistema para PyAudio e Vosk..."
sudo apt-get update || erro "Falha ao atualizar os repositórios."
sudo apt-get install -y portaudio19-dev libopenblas-dev libatlas3-base libatlas-base-dev || erro "Falha ao instalar dependências do sistema."

# Verifica se o arquivo requirements.txt existe
if [ -f "requirements.txt" ]; then
    echo "Instalando dependências do requirements.txt..."
    python3.11 -m pip install -r requirements.txt || erro "Falha ao instalar dependências do requirements.txt."
else
    echo "Arquivo requirements.txt não encontrado."
    exit 1
fi

# Verifica e instala as dependências necessárias (wget e unzip)
echo "Verificando e instalando dependências..."
if ! command -v wget &> /dev/null; then
    echo "Instalando wget..."
    sudo apt-get update && sudo apt-get install -y wget || erro "Falha ao instalar wget."
fi
if ! command -v unzip &> /dev/null; then
    echo "Instalando unzip..."
    sudo apt-get update && sudo apt-get install -y unzip || erro "Falha ao instalar unzip."
fi

# URLs dos arquivos ZIP
URL="https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip"
URL2="https://alphacephei.com/vosk/models/vosk-model-pt-fb-v0.1.1-20220516_2113.zip"

# Pasta de destino para o download e extração (relativa ao diretório do script)
PASTA_DESTINO="src/Modelos/Vosk"

# Cria a pasta de destino se ela não existir
mkdir -p "$PASTA_DESTINO" || erro "Falha ao criar a pasta de destino."

# Nomes dos arquivos ZIP
NOME_ARQUIVO=$(basename "$URL")
NOME_ARQUIVO2=$(basename "$URL2")

# Verifica se os modelos já estão instalados
if [ -d "$PASTA_DESTINO/vosk-model-small-pt-0.3" ] && [ -d "$PASTA_DESTINO/vosk-model-pt-fb-v0.1.1-20220516_2113" ]; then
    echo "Modelos Vosk já estão instalados."
else
    # Baixa os arquivos ZIP em paralelo
    echo "Baixando modelos Vosk..."
    wget -O "$PASTA_DESTINO/$NOME_ARQUIVO" "$URL" &
    wget -O "$PASTA_DESTINO/$NOME_ARQUIVO2" "$URL2" &
    wait

    # Verifica se o download foi bem-sucedido
    if [ $? -eq 0 ]; then
        echo "Download concluído com sucesso!"
    else
        erro "Erro ao baixar os arquivos ZIP. Verifique sua conexão com a internet ou as URLs fornecidas."
    fi

    # Extrai os arquivos ZIP
    echo "Extraindo $NOME_ARQUIVO..."
    unzip "$PASTA_DESTINO/$NOME_ARQUIVO" -d "$PASTA_DESTINO" || erro "Erro ao extrair $NOME_ARQUIVO."
    echo "Extraindo $NOME_ARQUIVO2..."
    unzip "$PASTA_DESTINO/$NOME_ARQUIVO2" -d "$PASTA_DESTINO" || erro "Erro ao extrair $NOME_ARQUIVO2."

    # Remove os arquivos ZIP após a extração
    rm "$PASTA_DESTINO/$NOME_ARQUIVO" "$PASTA_DESTINO/$NOME_ARQUIVO2" || erro "Falha ao remover os arquivos ZIP."
fi

# Limpeza final
echo "Realizando limpeza final..."
sudo apt-get clean || erro "Falha ao limpar o cache do APT."
sudo apt-get autoremove -y || erro "Falha ao remover pacotes desnecessários."

echo "Processo concluído com sucesso!"