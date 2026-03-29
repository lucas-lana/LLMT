import gradio as gr
import os
import sys

# Garante que o Python encontre os módulos na pasta src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import File_Operations as fo
import Models_Recognition as mr 

# --- Funções Auxiliares ---
def combinar_arquivos(lista_pastas, lista_arquivos):
    arquivos_brutos = []
    if lista_pastas:
        arquivos_brutos.extend(lista_pastas)
    if lista_arquivos:
        arquivos_brutos.extend(lista_arquivos)
    
    if not arquivos_brutos:
        return None

    arquivos_validos = [f for f in arquivos_brutos if os.path.exists(f)]
    return arquivos_validos if arquivos_validos else None

def tratar_e_limpar(files_folder, files_list):
    files = combinar_arquivos(files_folder, files_list)
    if not files:
        return None, None, gr.update(value="", visible=False)
        
    # Apenas verifica na UI
    _, files_tratados, lista_avisos = fo.trata_arquivo(files, apenas_verificar=True)
    
    if lista_avisos:
        texto_aviso = "\n".join(lista_avisos)
        return None, files_tratados, gr.update(value=texto_aviso, visible=True)
    
    return None, files_tratados, gr.update(value="", visible=False)

def update_status_text(files_folder, files_list, model_1, model_2, model_3):
    files = combinar_arquivos(files_folder, files_list)
    
    if not files: 
        return gr.update(value="⚠️ Nenhum arquivo carregado.", lines=1)
    if not any([model_1, model_2, model_3]): 
        return gr.update(value="⚠️ Nenhum modelo selecionado.", lines=1)
    
    tempo_processo, files_tratados, _ = fo.trata_arquivo(files, apenas_verificar=True)
    
    multipicador = 0
    multipicador_video = 0
    for arquivo in files_tratados:
        if any(ext in str(arquivo).lower() for ext in ['.mp4', '.avi', '.mov', '.mkv']): 
            multipicador_video = 0.21
            
    if model_1: multipicador += 0.32
    if model_2: multipicador += 0.17
    if model_3: multipicador += 0.40
    
    multipicador += multipicador_video
    tempo_total = tempo_processo * multipicador
    qtd = len(files_tratados)
    
    msg = ""
    if tempo_total < 60: msg = f"⏳ Tempo estimado: {tempo_total:.2f} s | Arquivos: {qtd}"
    elif tempo_total < 3600: msg = f"⏳ Tempo estimado: {tempo_total/60:.2f} min | Arquivos: {qtd}"
    else: msg = f"⏳ Tempo estimado: {tempo_total/3600:.2f} h | Arquivos: {qtd}"

    return gr.update(value=msg, lines=1)

def process_inputs(model_1, model_2, model_3, prompt, files_folder, files_list):
    files = combinar_arquivos(files_folder, files_list)
    
    models = 0
    if model_1: models += 1
    if model_2: models += 2
    if model_3: models += 4
    
    if models == 0 or files is None:
        yield None, gr.update(value="⚠️ Erro: Arquivos ou modelos faltando.", lines=1), gr.update(interactive=True)
        return

    msg_status = "🔄 Preparando arquivos (Convertendo vídeos/áudios)..."
    yield None, gr.update(value=msg_status, lines=2), gr.update(interactive=False)
    
    _, files, _ = fo.trata_arquivo(files, apenas_verificar=False)
    
    if not prompt: prompt = ""
    
    arquivos_prontos = []
    total_arquivos = len(files)
    
    for i, caminho_audio in enumerate(files):
        nome_atual = os.path.basename(caminho_audio)
        msg_status = f"🔄 PROCESSANDO ARQUIVO {i+1} DE {total_arquivos}...\n\n📁 Arquivo atual: '{nome_atual}'"
        
        yield arquivos_prontos, gr.update(value=msg_status, lines=4), gr.update(value="⏳ Gerando transcrições", interactive=False)
        
        caminho_txt = fo.transcrever_individual(caminho_audio, models, prompt)
        
        if caminho_txt and os.path.exists(caminho_txt):
            arquivos_prontos.append(caminho_txt)
            msg_status = f"✅ SUCESSO!\n\nArquivo '{nome_atual}' concluído ({i+1}/{total_arquivos}).\nPassando para o próximo..."
            yield arquivos_prontos, gr.update(value=msg_status, lines=4), gr.update(interactive=False)

    if arquivos_prontos:
        yield arquivos_prontos, gr.update(value="📦 Compactando arquivos em ZIP...", lines=2), gr.update(interactive=False)
        caminho_zip = fo.criar_zip_final(arquivos_prontos)
        if caminho_zip:
            arquivos_prontos.append(caminho_zip)

    yield arquivos_prontos, gr.update(value="🚀 Todas as transcrições foram concluídas e o ZIP foi criado!", lines=2), gr.update(interactive=True)

# --- Configuração Visual (CSS) ---
meu_css = """
    body { font-family: 'Segoe UI', sans-serif; background-color: #f4f4f9; }
    .gr-button { 
        background: linear-gradient(135deg, #6a11cb, #2575fc); 
        color: white; border: none; padding: 20px; border-radius: 8px; transition: 0.3s;
        font-size: 28px !important; font-weight: bold !important; 
    }
    .gr-button:hover { transform: scale(1); }
    .status-box { background: #2c3e50; border: 1px solid #1a252f; border-radius: 12px; padding: 12px; color: #ecf0f1; }
    .status-box textarea { font-size: 24px !important; line-height: 1.4 !important; font-weight: bold; }
    .tabs-grandes button { font-size: 18px !important; padding: 10px 20px !important; font-weight: bold; margin-bottom: 2px !important; }
    .warning-box textarea { background-color: #ffe6e6 !important; color: #cc0000 !important; border: 1px solid #ffcccc !important; font-weight: bold; }
    .check-big label span { font-size: 20px !important; line-height: 1.5 !important; padding-left: 5px !important; }
    .title-big h3 { font-size: 25px !important; font-weight: bold !important; margin-bottom: 10px !important; margin-top: 10px !important; }
    .header { font-size: 42px; font-weight: bold; text-align: center; margin-bottom: 40px; }
    .spacer-black { height: 3px; background-color:rgb(58, 58, 60); }
"""

# --- Execução Principal ---

# 1. Baixa os modelos AGORA (Escopo Global)
# Isso é necessário para que, ao importar este arquivo, os modelos já sejam verificados
print("Verificando modelos do Vosk...")
try:
    mr.ensure_models_downloaded()
except Exception as e:
    print(f"Aviso: Não foi possível verificar modelos na inicialização: {e}")

# 2. Constrói a Interface (Escopo Global)
# A variável 'demo' precisa existir aqui fora para ser importada pelo app.py
with gr.Blocks(css=meu_css) as demo:  
    gr.Markdown('<div class="header"> Transcrição Automática de Mídias </div>')        
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🛠️ Configurações:", elem_classes="title-big")
            
            model_1 = gr.Checkbox(label="Simple Vosk", value=True, elem_classes="check-big")
            model_2 = gr.Checkbox(label="Complete Vosk", value=True, elem_classes="check-big")
            model_3 = gr.Checkbox(label="Speech Recognition", value=True, elem_classes="check-big")

            prompt = gr.Textbox(label="📝 Prompt (opcional)", placeholder="Prompt personalizado...", elem_classes="check-big")
            
            gr.HTML('<div class="spacer-black"></div>')
            warning_box = gr.Textbox(label="⚠️ Avisos do Sistema", interactive=False, visible=False, elem_classes="warning-box")
            
            gr.Markdown("### 📊 Status:", elem_classes="title-big")
            status = gr.Textbox(label="Progresso", value="⏳ Aguardando início...", interactive=False, lines=1, elem_classes="status-box")
            
            transcript_button = gr.Button(value="🚀 Gerar transcrição", elem_classes="gr-button")
        
        with gr.Column(scale=2):
            gr.Markdown()
            with gr.Tabs(elem_classes="tabs-grandes"):
                with gr.TabItem("📄 Upload de Arquivos"):
                    files_list = gr.File(label="Selecione arquivos", file_count="multiple")
                with gr.TabItem("📁 Upload de Pasta"):
                    files_folder = gr.File(label="Selecione uma pasta", file_count="directory")
                            
            gr.Markdown("### 📥 Arquivos Gerados (Tempo Real):", elem_classes="title-big")
            output = gr.File(label="Baixar Transcrições", file_count="multiple")
    
    # Eventos
    files_folder.upload(fn=tratar_e_limpar, inputs=[files_folder, files_list], outputs=[files_folder, files_list, warning_box])
    files_list.upload(fn=tratar_e_limpar, inputs=[files_folder, files_list], outputs=[files_folder, files_list, warning_box])
    
    inputs_status = [files_folder, files_list, model_1, model_2, model_3]
    files_list.change(fn=update_status_text, inputs=inputs_status, outputs=[status])
    files_folder.change(fn=update_status_text, inputs=inputs_status, outputs=[status])
    model_1.change(fn=update_status_text, inputs=inputs_status, outputs=[status])
    model_2.change(fn=update_status_text, inputs=inputs_status, outputs=[status])
    model_3.change(fn=update_status_text, inputs=inputs_status, outputs=[status])
    
    transcript_button.click(
        fn=process_inputs,
        inputs=[model_1, model_2, model_3, prompt, files_folder, files_list],
        outputs=[output, status, transcript_button]
    )

# 3. Bloco para execução direta (Testes locais)
if __name__ == "__main__":
    print("--- Inicializando Aplicação Manualmente ---")
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)