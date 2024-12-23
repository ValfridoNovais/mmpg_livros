import os
import PyPDF2
import pyttsx3

def pdf_to_audio(pdf_path):
    try:
        # Extrair o nome do arquivo e o diretório do PDF
        base_dir = os.path.dirname(pdf_path)
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

        # Criar a pasta "audio" se ela não existir
        audio_dir = os.path.join(base_dir, "audio")
        os.makedirs(audio_dir, exist_ok=True)

        # Caminho para salvar o arquivo de áudio
        audio_file = os.path.join(audio_dir, f"{pdf_name}.mp3")

        # Abrir o arquivo PDF
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""

            # Extrair texto de cada página
            for page in reader.pages:
                text += page.extract_text()

        if not text.strip():
            print("Nenhum texto encontrado no PDF.")
            return

        # Configurar o mecanismo de TTS
        engine = pyttsx3.init()
        engine.setProperty('rate', 100)  # Ajusta a velocidade da fala
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[2].id)  # Escolhe a voz padrão (ajuste conforme necessário)

        # Salvar áudio em arquivo
        engine.save_to_file(text, audio_file)
        engine.runAndWait()
        print(f"Áudio gerado e salvo em: {audio_file}")

    except Exception as e:
        print(f"Erro ao processar o PDF: {e}")

# Caminho do PDF
pdf_path = r"C:\Repositorios_GitHube\MeusProjetos\mmpg_livros\pdf\Porcentagem.pdf"

# Chamar a função
pdf_to_audio(pdf_path)
