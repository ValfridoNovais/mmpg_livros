import PyPDF2
import pyttsx3

def pdf_to_audio(pdf_path, output_audio_file=None):
    try:
        # Abrir o arquivo PDF
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""

            # Extrair texto de cada página
            for page in reader.pages:
                text += page.extract_text()
        
        # Configurar o mecanismo de TTS
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Ajusta a velocidade da fala
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.alex')  # Altere para a voz disponível no seu sistema

        if output_audio_file:
            # Salvar áudio em arquivo
            engine.save_to_file(text, output_audio_file)
            engine.runAndWait()
            print(f"Áudio salvo como: {output_audio_file}")
        else:
            # Reproduzir áudio diretamente
            engine.say(text)
            engine.runAndWait()
    except Exception as e:
        print(f"Erro ao processar o PDF: {e}")

# Exemplo de uso
pdf_path = "seu_arquivo.pdf"  # Substitua pelo caminho do seu arquivo PDF
output_audio_file = "audio.mp3"  # Substitua pelo nome do arquivo de áudio desejado ou deixe como None
pdf_to_audio(pdf_path, output_audio_file)
