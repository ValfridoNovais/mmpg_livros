import os
import pdfplumber
import pyttsx3
import re

def process_text_refined(text):
    # Substituir múltiplas quebras de linha por uma única quebra de parágrafo
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Mantém quebra para novos parágrafos
    # Remover quebras de linha dentro de parágrafos contínuos
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)  # Substitui quebra de linha única por espaço
    # Remover espaços extras resultantes do processamento
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def pdf_to_audio_clean_paragraphs_refined(pdf_path):
    try:
        base_dir = os.path.dirname(pdf_path)
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

        # Criar a pasta "audio"
        audio_dir = os.path.join(base_dir, "audio")
        os.makedirs(audio_dir, exist_ok=True)

        # Caminho do arquivo de áudio
        audio_file = os.path.join(audio_dir, f"{pdf_name}.mp3")

        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Extrair texto e limpar cabeçalhos/rodapés
                extracted_text = page.crop((0, 50, page.width, page.height - 50)).extract_text()
                if extracted_text:
                    text += extracted_text + "\n"

        if not text.strip():
            print("Nenhum texto encontrado no PDF.")
            return

        # Processar o texto para corrigir quebras de linha
        cleaned_text = process_text_refined(text)

        # Configurar o mecanismo de TTS
        engine = pyttsx3.init()
        engine.setProperty('rate', 300)  # Ajustar velocidade de leitura
        voices = engine.getProperty('voices')

        # Alterar a voz (certifique-se de que o índice existe)
        if len(voices) > 14:
            engine.setProperty('voice', voices[13].id)  # Escolha a voz desejada
        else:
            engine.setProperty('voice', voices[0].id)  # Voz padrão

        # Salvar áudio
        engine.save_to_file(cleaned_text, audio_file)
        engine.runAndWait()
        print(f"Áudio gerado e salvo em: {audio_file}")

    except Exception as e:
        print(f"Erro ao processar o PDF: {e}")

# Caminho do PDF
pdf_path = r"C:\Repositorios_GitHube\MeusProjetos\mmpg_livros\pdf\Porcentagem.pdf"

# Chamar a função
pdf_to_audio_clean_paragraphs_refined(pdf_path)
