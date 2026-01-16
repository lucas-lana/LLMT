import gradio as gr
import File_Operations as fo
import os

# --- Funções Auxiliares (Mantidas iguais) ---
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
        
    _, files_tratados, lista_avisos = fo.trata_arquivo(files)
    
    if lista_avisos:
        texto_aviso = "\n".join(lista_avisos)
        return None, files_tratados, gr.update(value=texto_aviso, visible=True)
    
    return None, files_tratados, gr.update(value="", visible=False)

def update_status_text(files_folder, files_list, model_1, model_2, model_3):
    files = combinar_arquivos(files_folder, files_list)
    if not files: return "⚠️ Nenhum arquivo carregado."
    if not any([model_1, model_2, model_3]): return "⚠️ Nenhum modelo selecionado."
    
    tempo_processo, files_tratados, _ = fo.trata_arquivo(files)
    
    multipicador = 0
    multipicador_video = 0
    for arquivo in files_tratados:
        if "video" in str(arquivo): multipicador_video = 0.21
            
    if model_1: multipicador += 0.32
    if model_2: multipicador += 0.17
    if model_3: multipicador += 0.40
    
    multipicador += multipicador_video
    tempo_total = tempo_processo * multipicador
    qtd = len(files_tratados)
    
    if tempo_total < 60: return f"⏳ Tempo estimado: {tempo_total:.2f} s | Arquivos: {qtd}"
    elif tempo_total < 3600: return f"⏳ Tempo estimado: {tempo_total/60:.2f} min | Arquivos: {qtd}"
    else: return f"⏳ Tempo estimado: {tempo_total/3600:.2f} h | Arquivos: {qtd}"

# --- FUNÇÃO PRINCIPAL ALTERADA ---
def process_inputs(model_1, model_2, model_3, prompt, files_folder, files_list):
    files = combinar_arquivos(files_folder, files_list)
    
    models = 0
    if model_1: models += 1
    if model_2: models += 2
    if model_3: models += 4
    
    if models == 0 or files is None:
        yield None, "⚠️ Erro: Arquivos ou modelos faltando."
        return

    # Preparação
    _, files, _ = fo.trata_arquivo(files)
    if not prompt: prompt = ""
    
    arquivos_prontos = []
    total_arquivos = len(files)
    
    # LOOP COM ATUALIZAÇÃO DE STATUS
    for i, caminho_audio in enumerate(files):
        nome_atual = os.path.basename(caminho_audio)
        
        # 1. Avisa que começou este arquivo (Mantém a lista anterior visível)
        msg_status = f"🔄 Processando {i+1}/{total_arquivos}: '{nome_atual}'... Por favor aguarde."
        yield arquivos_prontos, msg_status
        
        # 2. Realiza a transcrição
        caminho_txt = fo.transcrever_individual(caminho_audio, models, prompt)
        
        if caminho_txt and os.path.exists(caminho_txt):
            arquivos_prontos.append(caminho_txt)
            
            # 3. Avisa que terminou este arquivo e atualiza a lista de downloads
            msg_status = f"✅ '{nome_atual}' concluído! ({i+1}/{total_arquivos})"
            yield arquivos_prontos, msg_status

    # Mensagem final quando sair do loop
    yield arquivos_prontos, "🚀 Todas as transcrições foram concluídas!"

# --- INTERFACE ---
if __name__ == "__main__":
    with gr.Blocks(css="""
        body { font-family: 'Segoe UI', sans-serif; background-color: #f4f4f9; }
        .gr-button { background: linear-gradient(135deg, #6a11cb, #2575fc); color: white; border: none; padding: 11px; border-radius: 8px; transition: 0.3s; }
        .gr-button:hover { transform: scale(1.02); }
        .status-box { background: #2c3e50; border: 1px solid #1a252f; border-radius: 12px; padding: 12px; color: #ecf0f1; font-weight: bold; }
        .warning-box textarea { background-color: #ffe6e6 !important; color: #cc0000 !important; border: 1px solid #ffcccc !important; font-weight: bold; }
        .header { font-size: 28px; font-weight: bold; color: #6a11cb; text-align: center; margin-bottom: 20px; }
        .spacer-black { height: 3px; background-color:rgb(58, 58, 60); }
    """) as demo:
        gr.Markdown('<div class="header"> Transcrição Automática de Mídias</div>')        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 🛠️ Configurações:")
                model_1 = gr.Checkbox(label="Simple Vosk", value=True)
                model_2 = gr.Checkbox(label="Complete Vosk", value=True)
                model_3 = gr.Checkbox(label="Speech Recognition", value=True)
                prompt = gr.Textbox(label="📝 Prompt (opcional)", placeholder="Prompt personalizado...")
                
                gr.HTML('<div class="spacer-black"></div>')
                warning_box = gr.Textbox(label="⚠️ Avisos do Sistema", interactive=False, visible=False, elem_classes="warning-box")
                
                gr.Markdown("### 📊 Status:")
                # Esta caixa agora será atualizada em tempo real durante o processo
                status = gr.Textbox(label="Progresso", value="Aguardando início...", interactive=False, elem_classes="status-box")
                
                transcript_button = gr.Button(value="🚀 Gerar transcrição", elem_classes="gr-button")
            
            with gr.Column(scale=2):
                gr.Markdown("### 📂 Carregue seus arquivos:")
                with gr.Tabs():
                    with gr.TabItem("📁 Upload de Pasta"):
                        files_folder = gr.File(label="Selecione uma pasta", file_count="directory")
                    with gr.TabItem("📄 Arquivos Soltos"):
                        files_list = gr.File(label="Arquivos prontos", file_count="multiple")
                                
                gr.Markdown("### 📥 Arquivos Gerados (Tempo Real):")
                output = gr.File(label="Baixar Transcrições", file_count="multiple")
        
        # --- Eventos ---
        files_folder.upload(fn=tratar_e_limpar, inputs=[files_folder, files_list], outputs=[files_folder, files_list, warning_box])
        files_list.upload(fn=tratar_e_limpar, inputs=[files_folder, files_list], outputs=[files_folder, files_list, warning_box])
        
        inputs_status = [files_folder, files_list, model_1, model_2, model_3]
        files_list.change(fn=update_status_text, inputs=inputs_status, outputs=[status])
        files_folder.change(fn=update_status_text, inputs=inputs_status, outputs=[status])
        model_1.change(fn=update_status_text, inputs=inputs_status, outputs=[status])
        model_2.change(fn=update_status_text, inputs=inputs_status, outputs=[status])
        model_3.change(fn=update_status_text, inputs=inputs_status, outputs=[status])
        
        # AQUI MUDOU: outputs recebe [output, status] para atualizar ambos ao mesmo tempo
        transcript_button.click(
            fn=process_inputs,
            inputs=[model_1, model_2, model_3, prompt, files_folder, files_list],
            outputs=[output, status]
        )
    
    demo.launch(share=True)