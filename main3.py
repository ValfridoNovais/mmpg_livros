import os
import pdfplumber
import pyttsx3
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def process_text_refined(text):
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Mantém quebra para novos parágrafos
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)  # Substitui quebra de linha única por espaço
    text = re.sub(r'\s{2,}', ' ', text)  # Remove espaços extras
    return text.strip()

def pdf_to_audio_with_ui(pdf_path, selected_voice_index, rate):
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
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"

        if not text.strip():
            messagebox.showwarning("Aviso", "Nenhum texto encontrado no PDF.")
            return

        # Processar o texto para corrigir quebras de linha
        cleaned_text = process_text_refined(text)

        # Configurar o mecanismo de TTS
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)  # Ajustar velocidade de leitura
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[selected_voice_index].id)

        # Salvar áudio
        engine.save_to_file(cleaned_text, audio_file)
        engine.runAndWait()
        messagebox.showinfo("Sucesso", f"Áudio gerado e salvo em: {audio_file}")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar o PDF: {e}")

def select_pdf_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Arquivos PDF", "*.pdf")],
        title="Selecione um arquivo PDF"
    )
    if file_path:
        pdf_path_var.set(file_path)

def generate_audio():
    pdf_path = pdf_path_var.get()
    if not pdf_path or not os.path.isfile(pdf_path):
        messagebox.showwarning("Aviso", "Por favor, selecione um arquivo PDF válido.")
        return

    rate = int(rate_entry.get())
    selected_voice_index = voice_listbox.curselection()
    if not selected_voice_index:
        messagebox.showwarning("Aviso", "Por favor, selecione uma voz.")
        return

    selected_voice_index = selected_voice_index[0]
    pdf_to_audio_with_ui(pdf_path, selected_voice_index, rate)

# Criar interface gráfica
root = tk.Tk()
root.title("Conversor de PDF para Áudio")

# Caminho do PDF
pdf_path_var = tk.StringVar()
tk.Label(root, text="Arquivo PDF:").pack(pady=5)
tk.Entry(root, textvariable=pdf_path_var, width=50).pack(pady=5)
tk.Button(root, text="Selecionar PDF", command=select_pdf_file).pack(pady=5)

# Velocidade de Leitura
tk.Label(root, text="Velocidade de Leitura (padrão: 200):").pack(pady=5)
rate_entry = tk.Entry(root, width=10)
rate_entry.insert(0, "200")
rate_entry.pack(pady=5)

# Seleção de Voz
tk.Label(root, text="Selecione a Voz:").pack(pady=5)
voice_listbox = tk.Listbox(root, selectmode=tk.SINGLE, height=5)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for index, voice in enumerate(voices):
    voice_listbox.insert(tk.END, f"{index}: {voice.name}")
voice_listbox.pack(pady=5)

# Botão para gerar áudio
tk.Button(root, text="Gerar Áudio", command=generate_audio).pack(pady=20)

# Rodar interface
root.mainloop()
