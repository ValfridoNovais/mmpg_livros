# PDF-to-Audio Converter

Este programa converte o texto de um arquivo PDF em um arquivo de áudio MP3, com tratamento para remover quebras de linha desnecessárias e ignorar cabeçalhos e rodapés.

## Recursos
- Extração de texto de PDFs utilizando `pdfplumber`.
- Conversão de texto para áudio utilizando `pyttsx3`.
- Suporte para ajuste de velocidade de leitura e seleção de vozes disponíveis no sistema.
- Criação automática de um diretório `audio` para salvar os arquivos gerados.

## Requisitos
- Python 3.8 ou superior
- Bibliotecas Python listadas em `requirements.txt`.

## Instalação
1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
