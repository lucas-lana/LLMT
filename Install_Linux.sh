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

# Verifica se o Python 3.14 está instalado
if ! command -v python3.14 &> /dev/null; then
    echo "Python 3.14 não está instalado. Instalando..."
    # Adiciona o repositório deadsnakes para Ubuntu/Debian
    sudo apt-get update || erro "Falha ao atualizar os repositórios."
    sudo apt-get install -y software-properties-common || erro "Falha ao instalar 'software-properties-common'."
    sudo add-apt-repository -y ppa:deadsnakes/ppa || erro "Falha ao adicionar o repositório 'deadsnakes/ppa'."
    sudo apt-get update || erro "Falha ao atualizar os repositórios após adicionar o PPA."
    # Instala o Python 3.14
    sudo apt-get install -y python3.14 python3.14-distutils || erro "Falha ao instalar Python 3.14."
else
    echo "Python 3.14 já está instalado."
fi

# Verifica se o pip está instalado
if ! python3.14 -m pip --version &> /dev/null; then
    echo "Instalando pip..."
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.14 || erro "Falha ao instalar pip."
fi

# Atualiza o pip
echo "Atualizando pip..."
python3.14 -m pip install --upgrade pip || erro "Falha ao atualizar pip."

# Instala dependências do sistema para PyAudio e Vosk
echo "Instalando dependências do sistema para PyAudio e Vosk..."
sudo apt-get update || erro "Falha ao atualizar os repositórios."
sudo apt-get install -y portaudio19-dev libopenblas-dev libatlas3-base libatlas-base-dev || erro "Falha ao instalar dependências do sistema."

# Verifica se o arquivo requirements.txt existe
if [ -f "requirements.txt" ]; then
    echo "Instalando dependências do requirements.txt..."
    python3.14 -m pip install -r requirements.txt || erro "Falha ao instalar dependências do requirements.txt."
else
    echo "Arquivo requirements.txt não encontrado."
    exit 1
fi

# Limpeza final
echo "Realizando limpeza final..."
sudo apt-get clean || erro "Falha ao limpar o cache do APT."
sudo apt-get autoremove -y || erro "Falha ao remover pacotes desnecessários."

echo "Processo concluído com sucesso!"
