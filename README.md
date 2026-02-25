# LLMT - Mídia To Text (Lucas Lana Multimidia Transcriber)

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/lucas-lana/llmt)
[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/downloads/release/python-3140/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Uma ferramenta gratuita  para transcrição de áudio e vídeo em português utilizando múltiplos modelos de IA.

**Autor:** Lucas Fonseca Sabino Lana  
**Contato:** [lucas.sabino.lana@gmail.com](mailto:lucas.sabino.lana@gmail.com)

---

## 📑 Índice

- [🎯 Descrição](#-descrição)
- [🚀 Início Rápido](#-início-rápido)
- [📋 Requisitos](#-requisitos)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [🔧 Configuração](#-configuração)
- [💻 Usando a Interface](#-usando-a-interface)
- [🐳 Docker](#-docker)
- [🤖 Modelos de Transcrição](#-modelos-de-transcrição)
- [📦 Instalação Manual](#-instalação-manual)
- [🔍 Resolução de Problemas](#-resolução-de-problemas)
- [📝 Dependências Chave](#-dependências-chave)
- [🤝 Contribuindo](#-contribuindo)
- [📄 Licença](#-licença)
- [❓ Dúvidas e Suporte](#-dúvidas-e-suporte)

---

## 🎯 Descrição

LLMT (Mídia To Text) é uma ferramenta inovadora que oferece **transcrição gratuita de áudio e vídeo** utilizando múltiplos modelos de IA. O projeto fornece uma interface web interativa (Gradio) que funciona em **Hugging Face Spaces** ou em instalação local, permitindo que qualquer pessoa transcreva conteúdo multimídia sem custos.

### Funcionalidades Principais
- **Reconhecimento de Voz**: Transcrição de áudio em português usando modelos Vosk
- **Processamento de Vídeo**: Extração e transcrição de áudio de arquivos de vídeo
- **Múltiplos Modelos**: Escolha entre Vosk Simple, Vosk Complete e Google Speech Recognition
- **Segmentação Automática**: Áudios longos são divididos em segmentos otimizados (~3 minutos)
- **Processamento de Áudio**: Manipulação e transformação de arquivos de áudio
- **Operações de Texto**: Processamento e análise de texto
- **Gerenciamento de Arquivos**: Operações com arquivos de entrada e saída

### Como Funciona
A ferramenta foi projetada para ser intuitiva e acessível:

1. **Acesse a Interface**: Clique no link do Hugging Face Spaces ou execute localmente
2. **Carregue seu Arquivo**: Arraste ou selecione um arquivo de áudio/vídeo
3. **Escolha o Modelo(s)**: Selecione qual modelo de transcrição usar (use os três modelos para uma maior qualidade de transcrição)
4. **Aguarde o Processamento**: O tempo estimado é exibido antes de iniciar (quanto mais modelos selecionados, mais demora o processamento)
5. **Baixe os Resultados**: Receba transcrições em arquivo .zip (ou .rar) com formato TXT

### Formatos Aceitos

**Áudio:**
- MP3 - Formato comprimido mais comum
- WAV - Qualidade de áudio sem compressão (convertido automaticamente)
- OGG - Formato de áudio com compressão livre
- FLAC - Áudio lossless
- AIFF - Formato de áudio interativo

**Vídeo:**
- MP4 - Formato de vídeo mais popular
- MKV - Formato de contenedor flexível
- AVI - Formato de vídeo clássico
- MOV - Formato de vídeo Apple
- WebM - Formato de vídeo web

> **Nota:** Arquivos WAV são automaticamente otimizados para melhor qualidade de transcrição.

## 🚀 Início Rápido

### 🤗 Opção 1: Hugging Face Spaces (Recomendado - Sem Instalação)

A forma mais fácil e rápida de usar o LLMT é através do Hugging Face Spaces. Não requer instalação e roda diretamente no seu navegador:

1. **Acesse o Link**: [LLMT no Hugging Face Spaces](https://huggingface.co/spaces/lucas-lana/llmt)
2. **Desperte o Espaço (se necessário)**: Como a hospedagem gratuita pausa aplicações inativas, o espaço pode estar "dormindo" (status *Sleeping* ou *Paused*). Se isso acontecer, basta clicar no botão na tela para iniciá-lo e aguardar alguns instantes até que a aplicação carregue.
3. **Pronto para usar**: A interface estará carregada e pronta para suas transcrições.

**Vantagens:**
- ✅ Zero configuração ou necessidade de rodar scripts
- ✅ Acesso de qualquer lugar com internet
- ✅ Totalmente gratuito e hospedado na nuvem

### 🐳 Opção 2: Docker (Recomendado - Instalação Local)

```bash
# Construir a imagem
docker build -t llmt:latest .

# Executar o container
docker run -p 7860:7860 llmt:latest
```

A aplicação estará disponível em http://localhost:7860
### 💻 Opção 3: Instalação Local (Linux)

> **⚠️ Atenção:**
>  - Este projeto foi otimizado e configurado para rodar estritamente no Python 3.14. Versões anteriores podem apresentar falhas de compatibilidade com as dependências.
>  - O gerenciador de pacotes deste arquivo de instalação é o `apt-get` 

#### O script de instalação configura tudo automaticamente:
      sudo bash Install_Linux.sh

#### Executar a aplicação:
      python src/Gradio_Interface.py

## 📋 Requisitos

### Sistema
- **Python**: 3.14+
- **Sistema Operacional**: Linux (Ubuntu/Debian recomendado)
- **RAM**: Mínimo 2GB (recomendado 4GB+)

### Dependências Principais
- **Gradio** 6.3.0 - Interface web interativa
- **Vosk** 0.3.45 - Motor de reconhecimento de voz
- **PyDub** - Processamento de áudio
- **FFmpeg** - Conversão de formato de áudio
- **NumPy** - Computação numérica

Para a lista completa de dependências, veja [requirements.txt](requirements.txt).

## 📁 Estrutura do Projeto

```text
LLMT/
├── src/
│   ├── Gradio_Interface.py      # Interface web principal
│   ├── Models_Recognition.py    # Modelos de reconhecimento de voz
│   ├── Audio_Operations.py      # Processamento de áudio
│   ├── Text_Operations.py       # Processamento de texto
│   └── File_Operations.py       # Gerenciamento de arquivos
├── Modelos/
│   └── Vosk/                    # Modelos de fala em português
│       ├── vosk-model-small-pt-0.3/
│       └── vosk-model-pt-fb-v0.1.1-20220516_2113/
├── dockerfile                   # Configuração Docker
├── Install_Linux.sh            # Script de instalação automática
├── requirements.txt            # Dependências Python
└── README.md                   # Este arquivo
```
## 🔧 Configuração

### Variáveis de Ambiente

Ao usar Docker, as seguintes variáveis estão pré-configuradas:

```text
PYTHONPATH=/app/src
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
```

### Modelos Vosk

O projeto utiliza dois modelos de reconhecimento de voz em português:

    vosk-model-small-pt-0.3 - Modelo leve (recomendado para recursos limitados)

    vosk-model-pt-fb-v0.1.1 - Modelo completo (melhor precisão)

Os modelos são baixados automaticamente pelo script de instalação.

## 💻 Usando a Interface

### Guia Passo a Passo

#### 1. **Carregue seu Arquivo**
   - Arraste um arquivo de áudio ou vídeo para a área indicada.
   - Ou clique para selecionar manualmente.
   - Formatos suportados: MP3, WAV, OGG, MP4, MKV, AVI.

#### 2. **Verifique o Tempo Estimado**
   - No canto inferior esquerdo, você verá o tempo estimado de processamento.
   - Pode remover arquivos ou alterar o modelo durante a espera.

#### 3. **Escolha o Modelo de Transcrição**
   - **Vosk Simple**: Rápido mas menos preciso.
   - **Vosk Complete**: Mais completo, marca palavras desconhecidas.
   - **Google Speech Recognition**: Ótimo para inglês.

#### 4. **Defina o prompt**
   - Se não passar nenhum prompt, existe um prompt padrão que é usado para criar uma transcrição final juntando todas as transcrições : ` A partir apenas das transcrições geradas pelos modelos, combine as transcrições a fim de gerar um texto fusão sendo o mais coerente e fiel as informações dos textos:`
   - Caso ache o prompt padrão não atende as suas necessidades / vontades, é possível passar um prompt personalizado.
   - Clique na caixa "Prompt personalizado", abaixo de "Prompt (Opicional)" e digite o seu prompt
   - A primeira linha do arquivo de transcrição será o seu prompt personalizado

#### 5. **Inicie o Processamento**
   - Clique em "Gerar Transcrição".
   - O sistema processa nos servidores do Hugging Face (ou localmente).
   - Áudios longos são divididos em segmentos otimizados (~3 minutos).

#### 6. **Baixe os Resultados**
   - Um arquivo `.zip` (ou `.rar`) é gerado contendo as todas as transcrições e também é possível retornado um arquivo de transcrição `.txt` para cada arquivo a ser transcrito.
   - Formato: `nome_do_arquivo_transcrição.txt`.
   - Dentro do arquivo `.txt` terá todas as do texto (uma por modelo selecionado).

#### 7. **Transcrição Final**
   - Com os arquivos de transcrições em mãos, acesse uma IA (ChatGPT, Gemini, Meta, Claude ...) e carrege o arquivo de transcrição, o resultado será a transcrição final (A primeira linha do arquivo já é um prompt que pede para a IA fazer isso).

### Saída do Processamento

O resultado final inclui:
- ✅ N versões transcritas (uma transcrição por modelo utilizado).
- ✅ Arquivos em formato TXT legível.
- ✅ Tempo total de processamento.
- ✅ Estatísticas do áudio processado.


## 🐳 Docker
```bash
docker build -t llmt:latest .
# Com porta padrão
docker run -p 7860:7860 llmt:latest

# Com volume persistente
docker run -p 7860:7860 -v /caminho/local:/app/output llmt:latest
```
## 🤖 Modelos de Transcrição

LLMT integra três modelos poderosos para máxima flexibilidade:

### 1. **Vosk Simple**
- **Velocidade**: ⚡ Muito rápida
- **Precisão**: 🎯 Moderada
- **Idiomas**: Português, Inglês, Russo e outros
- **Melhor para**: Resumos rápidos, transcrições informais
- **Tamanho**: Modelo leve (~50MB)

### 2. **Vosk Complete**
- **Velocidade**: 🔋 Média
- **Precisão**: 🎯🎯 Alta
- **Idiomas**: Português, Inglês e outros
- **Melhor para**: Documentos profissionais, precisão crítica
- **Recursos**: Marca palavras desconhecidas com [UNK]
- **Tamanho**: Modelo completo (~2.5GB)

### 3. **Google Speech Recognition**
- **Velocidade**: 🔋 Média
- **Precisão**: 🎯🎯🎯 Muito Alta
- **Idiomas**: Mais de 100 idiomas
- **Melhor para**: Inglês, áudio de alta qualidade
- **Observação**: Requer conexão com internet
- **Limite**: Até 60 segundos por requisição

### Comparação Rápida

| Característica | Vosk Simple | Vosk Complete | Google Speech |
|---|---|---|---|
| Velocidade | Muito Rápida | Média | Média |
| Precisão | Moderada | Alta | Muito Alta |
| Português | ✅ Bom | ✅ Excelente | ✅ Bom |
| Offline | ✅ Sim | ✅ Sim | ❌ Não |
| Custo | Gratuito | Gratuito | Gratuito

## 📦 Instalação Manual

Se preferir instalação manual em vez do script automático:

```bash
# 1. Instalar Python 3.14
sudo apt-get install python3.14 python3.14-distutils

# 2. Instalar dependências do sistema
sudo apt-get install portaudio19-dev libopenblas-dev libatlas-base-dev ffmpeg

# 3. Instalar dependências Python
python3.14 -m pip install -r requirements.txt

# 4. Baixar modelos Vosk manualmente (opcional)
# Os modelos devem estar em Modelos/Vosk/
```
## 🔍 Resolução de Problemas

### Problema: ModuleNotFoundError
```text
Solução: Certifique-se que PYTHONPATH está definido para o diretório src/
```
### Problema: Porta 7860 já em uso
```
# Use uma porta diferente
docker run -p 8000:7860 llmt:latest
# ou
GRADIO_SERVER_PORT=8000 python src/Gradio_Interface.py
```
### Problema: Erro ao processar áudio
```      
#Certifique-se que FFmpeg está instalado:
sudo apt-get install ffmpeg
```

## 📝 Dependências Chave

| Pacote | Versão | Propósito |
|--------|--------|----------|
| gradio | 6.3.0 | Interface web |
| vosk | 0.3.45 | Reconhecimento de voz |
| pydub | 0.25.1 | Processamento de áudio |
| numpy | 2.4.1 | Computação numérica |
| ffmpy | 1.0.0 | Interface FFmpeg |

## 🤝 Contribuindo

Contribuições são extremamente bem-vindas! Se você tem ideias para melhorar a ferramenta, otimizar o código ou adicionar novos recursos, sinta-se à vontade para participar.

### Como contribuir:

1. Faça um **Fork** do repositório
2. Crie uma branch para sua feature ou correção (`git checkout -b feature/MinhaFeatureIncrivel`)
3. Faça o commit de suas mudanças com mensagens claras (`git commit -m 'Feat: Adiciona suporte a novo idioma'`)
4. Faça o push para a branch (`git push origin feature/MinhaFeatureIncrivel`)
5. Abra um **Pull Request** detalhando as alterações propostas

### Diretrizes Adicionais:
- **Testes:** Se possível, teste suas modificações localmente garantindo que a transcrição e a conversão de áudio/vídeo continuam funcionando perfeitamente.
- **Issues:** Antes de iniciar uma grande alteração, abra uma *Issue* no repositório para discutirmos a abordagem.
- *Nota:* No futuro, caso necessáiro posso adicionar um arquivo `CONTRIBUTING.md` dedicado com regras mais rígidas de estilo de código.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo de licença para mais detalhes.

## ❓ Dúvidas e Suporte

Tem alguma dúvida, deseja entrar em contato ou encontrou um problema?

**Entre em contato conosco:**
- 📧 **E-mail:** [lucas.sabino.lana@gmail.com](mailto:lucas.sabino.lana@gmail.com)
- 💬 **Suporte**: Abra uma issue no repositório
- 🐛 **Reporte Bugs**: Use a seção de issues

### Perguntas Frequentes

**P: A ferramenta é realmente gratuita?**
R: Sim! LLMT é 100% gratuita. Não há custos ocultos ou limites de uso.

**P: Meus arquivos são armazenados?**
R: Não. Os arquivos são processados temporariamente e descartados após o processamento. Nenhum arquivo é armazenado permanentemente.

**P: Posso usar offline?**
R: Sim (ao rodar a aplicação localmente (claro), exceto pelo modelo Google Speech Recognition que requer conexão com a internet.

**P: Qual é o tamanho máximo de arquivo?**
R: Depende da sua conexão. Arquivos de várias horas funcionam bem.

**P: O áudio original é alterado?**
R: Não! A ferramenta apenas gera novas transcrições e não modifica seus arquivos originais.

## 🙏 Agradecimentos

- [Vosk](https://github.com/alphacephei/vosk-api) - Motor de reconhecimento de voz offline
- [Gradio](https://gradio.app/) - Framework para interfaces web intuitivas
- [PyDub](https://github.com/jiaaro/pydub) - Processamento e manipulação de áudio
- [Google Speech Recognition](https://cloud.google.com/speech-to-text) - API de reconhecimento de voz
- [Hugging Face Spaces](https://huggingface.co/spaces) - Plataforma de hospedagem de aplicações de IA

---

## 📌 Informações Importantes

- ✅ **Totalmente Gratuito**: Sem custos ou limites de uso
- 🔒 **Privacidade**: Nenhum arquivo é armazenado permanentemente
- 📝 **Sem Alterações**: Seus arquivos originais nunca são modificados
- 🚀 **Rápido e Eficiente**: Processamento otimizado com múltiplos modelos
- 🌍 **Acessível**: Funciona em qualquer navegador com internet

---

## Próximos Passos:
- Implementar uma integração da saída (as transcrições) com uma LLM, possivelmente usando o n8n

**Desenvolvido por Lucas Fonseca Sabino Lana**

**Última atualização**: Fevereiro 2026




