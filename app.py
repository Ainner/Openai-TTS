import gradio as gr
import tempfile
from openai import OpenAI

def tts(text, model, voice):
    try:
        client = OpenAI(
            base_url='https://api.closeai-proxy.xyz/v1',
            api_key='XXX',
        )

        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
        )

    except Exception as error:
        print(str(error))
        raise gr.Error("An error occurred while generating speech. Please check your API key and try again.")

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        temp_file.write(response.content)

    return temp_file.name

def gradio_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# <center> OpenAI Text-To-Speech </center>")
        with gr.Row(variant='panel'):
            model = gr.Dropdown(choices=['tts-1','tts-1-hd'], label='Model', value='tts-1')
            voice = gr.Dropdown(choices=['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'], label='Voice Options', value='alloy')

        text = gr.Textbox(label="Input text", placeholder="Enter your text and then click on the 'Generate' button, or press the Enter key.", lines=4)  # 设置 lines 参数为 4，表示多行输入框
        btn = gr.Button("Generate")
        output_audio = gr.Audio(label="Speech Output")
    
        text.submit(fn=tts, inputs=[text, model, voice], outputs=output_audio, api_name="tts_enter_key", concurrency_limit=None)
        btn.click(fn=tts, inputs=[text, model, voice], outputs=output_audio, api_name="tts_button", concurrency_limit=None)

    demo.launch()

if __name__ == "__main__":
    gradio_interface()
