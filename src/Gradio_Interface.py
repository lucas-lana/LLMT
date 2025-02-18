import gradio as gr
import File_Operations as fo
from IPython.display import Javascript, display

def tutorial_link():
    js_code = """
    window.open("https://www.google.com", "_blank");
    """
    display(Javascript(js_code))

def process_inputs(model_1, model_2, model_3, prompt, files):
    models = 0
    arquivos_temp = {}
    if model_1: models += 1
    if model_2: models += 2
    if model_3: models += 4
    if models == 0 or files is None:
        print(f"Models: {models}, Files: {files}")
        print("Nenhum modelo selecionado ou nenhum arquivo carregado.")
        return None
    else:
        # Usa a nova lista de arquivos retornada por trata_arquivos
        _, files = fo.trata_arquivo(files)
        if not prompt:
            prompt = ""
            
        arquivos_temp = fo.acessa_arquivos(files, models, prompt)
        zip_arquivo = fo.compactar_em_zip(arquivos_temp, "Transcrições.rar")
        for caminho in arquivos_temp.values():
            fo.os.remove(caminho)
    return zip_arquivo

def update_status(files, model_1, model_2, model_3):
    multipicador = 0
    if files is None or not any([model_1, model_2, model_3]):
        if files is None:
            return "⚠️ Nenhum arquivo carregado."
        elif not any([model_1, model_2, model_3]):
            return "⚠️ Nenhum modelo selecionado."
        else:
            return "⚠️ Nenhum arquivo carregado e nenhum modelo selecionado."
    else:
        # Atualiza a lista de arquivos com a nova lista retornada por trata_arquivos
        tempo_processo, files = fo.trata_arquivo(files)
        
        if model_1: multipicador += 0.32
        if model_2: multipicador += 0.17
        if model_3: multipicador += 0.40
        tempo_total = tempo_processo * multipicador
        
        if tempo_total < 60:
            return f"⏳ Tempo estimado: {tempo_total:.2f} segundos | Total de arquivos: {len(files)}"
        elif tempo_total < 3600:
            return f"⏳ Tempo estimado: {tempo_total/60:.2f} minutos ou {tempo_total:.2f} segundos | Total de arquivos: {len(files)}"
        else:
            return f"⏳ Tempo estimado: {tempo_total/3600:.2f} horas ou {tempo_total:.2f} segundos | Total de arquivos: {len(files)}"

def update_files_and_status(files, model_1, model_2, model_3):
    if files:
        # Atualiza a lista de arquivos com a nova lista retornada por trata_arquivos
        _, files = fo.trata_arquivo(files)
        status_msg = update_status(files, model_1, model_2, model_3)
        return files, status_msg
    return files, update_status(files, model_1, model_2, model_3)

if __name__ == "__main__":
    with gr.Blocks(css="""
        /* Estilo geral */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f9;
        }
        .gr-button {
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: white;
            border: none;
            padding: 8px 13px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 5px 1px;
            cursor: pointer;
            border-radius: 8px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .gr-button:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
        }
        .gr-textbox {
            border: 2px solid #ddd;
            border-radius: 12px;
            padding: 10px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        .gr-textbox:focus {
            border-color: #6a11cb;
            box-shadow: 0 0 8px rgba(106, 17, 203, 0.3);
        }
        .gr-checkbox {
            margin: 5px 0;
        }
        .status-box {
            background: linear-gradient(135deg, #1e1e2f, #2c3e50);
            border: 1px solid #1a252f;
            border-radius: 12px;
            padding: 12px;
            font-size: 14px;
            color: #ecf0f1;
            transition: transform 0.3s ease;
        }
        .status-box:hover {
            transform: translateY(-2px);
        }
        .header {
            font-size: 28px;
            font-weight: bold;
            color: #6a11cb;
            text-align: center;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }
        .instructions {
            font-size: 14px;
            color: #555;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        .icon {
            font-size: 20px;
            margin-right: 8px;
        }
        .spacer-black {
            height: 3px;
            background-color:rgb(58, 58, 60);
        }
    """) as demo:
        gr.Markdown('<div class="header"> Transcrição Automática de Mídias</div>')        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 🛠️ Configurações:")
                model_1 = gr.Checkbox(label="Simple Vosk", value=True)
                model_2 = gr.Checkbox(label="Complete Vosk", value=True)
                model_3 = gr.Checkbox(label="Speech Recognition", value=True)
                prompt = gr.Textbox(label="📝 Personalize o prompt padrão (opcional)", placeholder="Digite um prompt personalizado...")
                
                gr.HTML('<div class="spacer-black"></div>')
                gr.Markdown("### 📊 Status:")
                
                status = gr.Textbox(label="Tempo de processamento", value="Aguardando interação...", interactive=False, elem_classes="status-box")
                
                tutorial_button = gr.Button(value="📖 Tutorial de Uso", elem_classes="gr-button")
                transcript_button = gr.Button(value="🚀 Gerar transcrição", elem_classes="gr-button")
            
            with gr.Column(scale=2):
                gr.Markdown("### 📂 Carregue seus arquivos:")
                files = gr.File(label="Carregue uma pasta", file_count="directory")
                                
                gr.Markdown("### 📥 Arquivo Gerado:")
                output = gr.File(label="Baixar transcrições RAR")
        
        transcript_button.click(
            fn=process_inputs,
            inputs=[model_1, model_2, model_3, prompt, files],
            outputs=[output]
        )
        tutorial_button.click(fn=tutorial_link)
        
        files.change(
            fn=update_files_and_status,
            inputs=[files, model_1, model_2, model_3],
            outputs=[files, status]
        )
        model_1.change(
            fn=update_status,
            inputs=[files, model_1, model_2, model_3],
            outputs=[status]
        )
        model_2.change(
            fn=update_status,
            inputs=[files, model_1, model_2, model_3],
            outputs=[status]
        )
        model_3.change(
            fn=update_status,
            inputs=[files, model_1, model_2, model_3],
            outputs=[status]
        )
    
    demo.launch(share=True)