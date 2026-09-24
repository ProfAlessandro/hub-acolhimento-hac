import gradio as gr
import speech_recognition as sr
from deep_translator import MyMemoryTranslator
from gtts import gTTS
import os

print("🚀 Inicializando Sistema de Reconhecimento de Voz Ultraleve...")
reconhecedor = sr.Recognizer()

def app_tradutor_hibrido(texto_digitado, audio_gravado_direto):
    # REGRA DE PRIORIDADE: Se o usuário gravou áudio, o sistema transcreve usando a API estável
    if audio_gravado_direto is not None:
        print("🎙️ Processando áudio capturado diretamente pelo microfone...")
        try:
            with sr.AudioFile(audio_gravado_direto) as fonte:
                dados_audio = reconhecedor.record(fonte)
                # Transcreve o áudio em português de forma extremamente leve na nuvem
                texto_final_pt = reconhecedor.recognize_google(dados_audio, language="pt-BR")
        except Exception as e:
            print(f"Erro na transcrição: {e}")
            texto_final_pt = "Não foi possível compreender o áudio. Tente falar novamente de forma clara."
    else:
        texto_final_pt = texto_digitado

    if not texto_final_pt or not texto_final_pt.strip():
        return "Por favor, digite um texto ou grave seu áudio.", "Aguardando entrada...", None

    # Tradução instantânea em tempo real via MyMemory
    texto_espanhol = MyMemoryTranslator(source='pt-BR', target='es-ES').translate(texto_final_pt)
    
    # Síntese de voz em espanhol
    IA_voz = gTTS(text=texto_espanhol, lang='es', slow=False)
    nome_arquivo = "traducao_direta.mp3"
    IA_voz.save(nome_arquivo)
    
    return texto_final_pt, texto_espanhol, nome_arquivo

def limpar_dados_sistema():
    print("🧹 Limpando dados da tela para o próximo usuário...")
    return "", None, "", "", None

estilo_customizado = """
#componente_audio button {
    background-color: #ef4444 !important; /* Cor vermelha viva para gravação */
    color: white !important;
    border: none !important;
    font-weight: bold !important;
}
#componente_audio button:hover {
    background-color: #dc2626 !important;
}
#rodape_creditos {
    text-align: center;
    margin-top: 30px;
    padding-top: 15px;
    border-top: 1px solid #e5e7eb;
}
"""

with gr.Blocks(theme=gr.themes.Soft(), css=estilo_customizado) as app_universal:
    gr.Markdown("# Hub de Acolhimento e Comunicação  - HAC")
    gr.Markdown("### ⚠️ ATENÇÃO: Permita o uso do microfone no seu navegador quando o alerta aparecer!")
    
    with gr.Row():
        with gr.Column():
            entrada_texto = gr.Textbox(label="Opção A: Digite em português:", placeholder="Escreva aqui se preferir digitar...", lines=3)
            
            entrada_audio = gr.Audio(
                label="Opção B: Audio (Clique no microfone abaixo):", 
                sources=["microphone"], 
                type="filepath",
                elem_id="componente_audio"
            )
            
            with gr.Row():
                botao_processar = gr.Button("Traduzir", variant="primary")
                botao_limpar = gr.Button("Limpar Dados", variant="secondary")
            
        with gr.Column():
            saida_pt = gr.Textbox(label="📝 Texto Identificado (Português):", interactive=False)
            saida_es = gr.Textbox(label="🔄 Tradução Automática (Espanhol):", interactive=False)
            saida_audio = gr.Audio(label="🔊 Pronúncia da IA (Espanhol Nativo):", type="filepath")
            
    gr.Markdown(
        "🛠️ **Desenvolvido por: Professor Alessandro Ramos e Gemini** | _Projeto de Inclusão Tecnológica e Social com Inteligência Artificial e Python_",
        elem_id="rodape_creditos"
    )

    botao_processar.click(
        fn=app_tradutor_hibrido, 
        inputs=[entrada_texto, entrada_audio], 
        outputs=[saida_pt, saida_es, saida_audio]
    )
    
    botao_limpar.click(
        fn=limpar_dados_sistema,
        inputs=[],
        outputs=[entrada_texto, entrada_audio, saida_pt, saida_es, saida_audio]
    )

# Configuração obrigatória para servidores em nuvem permanente
app_universal.launch(server_name="0.0.0.0", server_port=7860, inline=False)
