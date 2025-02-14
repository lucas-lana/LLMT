import gradio as gr
import File_Operations as fo

# Função que será chamada quando o usuário interagir com a interface
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
        # Lista todos os arquivos na pasta e realiza operações individuais
        lista_n_suportados, _ = fo.trata_arquivo(files)
        arquivos_temp = fo.acessa_arquivos(files, lista_n_suportados, models, prompt)
        
        zip_arquivo = fo.compactar_em_zip(arquivos_temp, "Transcrições.rar")
        for caminho in arquivos_temp.values():
            fo.os.remove(caminho)
    return zip_arquivo

# Função que atualiza o status
def update_status(files, model_1, model_2, model_3):
    multipicador = 0
    if files is None or not any([model_1, model_2, model_3]):
        if files is None:
            return "Nenhum arquivo carregado."
        elif not any([model_1, model_2, model_3]):
            return "Nenhum modelo selecionado."
        else:
            return "Nenhum arquivo carregado e nenhum modelo selecionado."
    else:
        # Chama a função de processamento para obter o tempo de processamento
        _, tempo_processo = fo.trata_arquivo(files)
        if model_1: multipicador += 0.32
        if model_2: multipicador += 0.17
        if model_3: multipicador += 0.40
        tempo_total = tempo_processo * multipicador
        if tempo_total < 60:
            return f"Tempo de processamento estimado: {tempo_total:.2f} segundos"
        elif tempo_total < 3600:
            return f"Tempo de processamento estimado: {tempo_total/60:.2f} minutos ou {tempo_total:.2f} segundos"
        else:
            return f"Tempo de processamento estimado: {tempo_total/3600:.2f} horas ou {tempo_total/60:.2f} minutos ou {tempo_total:.2f} segundos"


if __name__ == "__main__":
    # Definindo a interface Gradio
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                with gr.Column():
                    gr.Markdown("### Selecione os modelos:")
                    model_1 = gr.Checkbox(label="Simple Vosk", value=True)
                    model_2 = gr.Checkbox(label="Complete Vosk", value=True)
                    model_3 = gr.Checkbox(label="Speech Recognition", value=True)
                with gr.Column():
                    prompt = gr.Textbox(label="Personalize o prompt padrão (opcional)")
                    transcript_button = gr.Button(value="Gerar transcrição")
            with gr.Column():   
                files = gr.File(label="Carregue uma pasta", file_count="directory")
                status = gr.Textbox(label="Status", value="Aguardando interação...", interactive=False)
        
        output = gr.File(label="Baixar transcrições RAR")
        
        
        # Define a função para o botão de transcrição
        transcript_button.click(fn=process_inputs, inputs=[model_1, model_2, model_3, prompt, files], outputs=[output])
        
        # Define a função para atualizar o status automaticamente
        files.change(fn=update_status, inputs=[files, model_1, model_2, model_3], outputs=[status])
        model_1.change(fn=update_status, inputs=[files, model_1, model_2, model_3], outputs=[status])
        model_2.change(fn=update_status, inputs=[files, model_1, model_2, model_3], outputs=[status])
        model_3.change(fn=update_status, inputs=[files, model_1, model_2, model_3], outputs=[status])
    
    # Lançando a interface
    demo.launch(share=False)