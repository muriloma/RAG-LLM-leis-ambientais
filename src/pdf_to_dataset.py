import os
import pdfplumber
import nltk
from pathlib import Path
from datetime import datetime
from colorama import Fore, init

init(autoreset=True)

nltk.download('punkt')
nltk.download('punkt_tab')

def validate_pdf(file_path):
    print(f"[{datetime.now()}] {Fore.YELLOW}Validando arquivo PDF: {file_path}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{Fore.RED}O arquivo {file_path} não existe.")
    if not file_path.lower().endswith('.pdf'):
        raise ValueError(f"{Fore.RED}O arquivo {file_path} não é um PDF válido.")
    try:
        with pdfplumber.open(file_path) as pdf:
            return True
    except Exception as e:
        raise ValueError(f"{Fore.RED}Falha ao abrir o arquivo PDF: {e}")

def extract_text_from_pdf(pdf_path):
    print(f"[{datetime.now()}] {Fore.YELLOW}Extraindo texto do PDF: {pdf_path}")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        raise ValueError(f"{Fore.RED}Falha ao extrair texto do PDF: {e}")

def preprocess_text(text):
    print(f"[{datetime.now()}] {Fore.YELLOW}Processando texto (dividindo em sentenças).")
    sentences = nltk.sent_tokenize(text)
    return sentences

def save_dataset(sentences, output_file="dataset.txt"):
    print(f"[{datetime.now()}] {Fore.YELLOW}Salvando dataset no arquivo {output_file}.")
    with open(output_file, "w", encoding="utf-8") as f:
        for sentence in sentences:
            f.write(sentence + "\n")
    return output_file

def pdf_to_dataset(pdf_path):
    print(f"[{datetime.now()}] {Fore.GREEN}Iniciando o processo de conversão de PDF para dataset.")
    
    if not validate_pdf(pdf_path):
        return None
    
    text = extract_text_from_pdf(pdf_path)
    
    sentences = preprocess_text(text)
    
    dataset_path = save_dataset(sentences)
    
    print(f"[{datetime.now()}] {Fore.GREEN}Processo de conversão concluído.")
    return dataset_path


if __name__ == "__main__":
    pdf_file_path = "./data/dataset/dataset_leis.pdf"
    
    dataset_path = pdf_to_dataset(pdf_file_path)
    print(f"[{datetime.now()}] {Fore.CYAN}Dataset gerado e salvo em: {dataset_path}")
