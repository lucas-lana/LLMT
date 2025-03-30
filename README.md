# Mídia To Text - LLMT  

**Autor:** Lucas Fonseca Sabino Lana  
**Contato:** lucas.sabino.lana@gmail.com  

Esta ferramenta oferece transcrição gratuita de áudio e vídeo utilizando múltiplos modelos de IA. Para começar, acesse o Google Colab pelo link fornecido. A interface apresenta uma caixa de comandos onde todo o processo ocorre. Clique na seta no canto superior esquerdo para iniciar a configuração automática do ambiente, que leva de 3 a 5 minutos.  

Após a instalação, aparecerão dois links - clique no segundo (terminando com gradio.live) para acessar a interface principal. A aplicação permanece ativa por até 85 horas contínuas. Na tela principal, você pode carregar arquivos arrastando ou selecionando na área indicada. São aceitos formatos como MP3, WAV, OGG (áudio) e MP4, MKV, AVI (vídeo). Arquivos WAV são automaticamente convertidos para melhor qualidade.  

No canto inferior esquerdo, um indicador mostra o tempo estimado de processamento. Durante a espera, é possível remover arquivos ou alterar modelos. Ao clicar em "Gerar Transcrição", o sistema inicia o processamento nos servidores do Google. Quando concluído, um arquivo .rar é gerado contendo as transcrições em formato TXT, nomeados como nome_do_arquivo_transcrição.txt.  

Internamente, a ferramenta utiliza três modelos de transcrição: Vosk Simple (rápido mas menos preciso), Vosk Complete (mais completo, marca palavras desconhecidas) e Google Speech Recognition (ótimo para inglês). Áudios longos são divididos em segmentos de ~3 minutos para melhor eficiência.  

O resultado final inclui três versões do texto transcrito (uma por modelo utilizado). Você pode copiar esses textos para usar com outras ferramentas de IA como ChatGPT. A ferramenta é totalmente gratuita e não altera os arquivos originais, apenas gera novas transcrições.  

Para acessar: [Link da Ferramenta](https://colab.research.google.com/drive/1o2aB6_ouxhTkYo2qLN_tj0dFKJnmDQ_r?usp=sharing)  

Dúvidas? Contate: lucas.sabino.lana@gmail.com
