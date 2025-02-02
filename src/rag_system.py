# rag_system.py

import json
import os
import time
import ollama
from datasets import load_dataset
from configurator import get_user_input

EMBEDDING_MODEL = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'

VECTOR_DB = []

def download_and_save_dataset(dataset_name, save_path):
    try:
        dataset = load_dataset(dataset_name)
        os.makedirs(save_path, exist_ok=True)
        with open(f'{save_path}/dataset.txt', 'w', encoding='utf-8') as f:
            for item in dataset['train']:
                if 'text' in item:
                    f.write(item['text'] + '\n')
        print(f"Dataset {dataset_name} baixado com sucesso e salvo em {save_path}/dataset.txt.")
    except Exception as e:
        print(f"Erro ao baixar ou salvar o dataset {dataset_name}: {str(e)}")

def download_model(model_name):
    try:
        ollama.pull(model_name)
        print("Modelo baixado com sucesso.")
    except Exception as e:
        print(f"Erro ao baixar o modelo {model_name}: {str(e)}")

def add_chunk_to_database(chunk):
    embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)['embeddings'][0]
    VECTOR_DB.append((chunk, embedding))

def load_data(data_file):
    with open(data_file, 'r', encoding='utf-8') as file:
        dataset = file.readlines()
    for chunk in dataset:
        add_chunk_to_database(chunk.strip())

def cosine_similarity(a, b):
    dot_product = sum([x * y for x, y in zip(a, b)])
    norm_a = sum([x ** 2 for x in a]) ** 0.5
    norm_b = sum([x ** 2 for x in b]) ** 0.5
    return dot_product / (norm_a * norm_b)

def retrieve(query, top_n=3):
    query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=query)['embeddings'][0]
    similarities = []
    for chunk, embedding in VECTOR_DB:
        similarity = cosine_similarity(query_embedding, embedding)
        similarities.append((chunk, similarity))
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_n]

def ask_llama(question, options, model):
    options_text = "\n".join([f"{key}: {value}" for key, value in options.items()])
    prompt = f"Pergunta: {question}\nEscolha a alternativa correta entre as opções. A reposta deve conter apenas a letra da alternativa escolhida e mais nenhum texto.\nÉ obrigatório escolher uma das alternativas abaixo, mesmo que você não saiba qual é a resposta correta, é obrigatório escolher uma alternativa:\n{options_text}\nResposta:"
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response['message']['content'].strip()

def main(config):
    LANGUAGE_MODEL = config["model"]
    num_questions = int(config["num_questions"]) if config["num_questions"] != "3" else None
    use_rag = config["use_rag"]

    if use_rag == 1:
        dataset_name = config["dataset_name"]
        if not dataset_name:
            dataset_name = './dataset.txt'
            download_and_save_dataset(dataset_name, './data/dataset')
        load_data('./dataset.txt')

    question_file_path = './data/input/questoes.json'
    if not os.path.exists(question_file_path):
        print(f"Arquivo de questões não encontrado: {question_file_path}")
        return

    with open(question_file_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    if num_questions:
        questions = questions[:num_questions]

    answers = []
    start_time = time.time()

    for q in questions:
        question_text = q['question']
        options = q['options']
        number = q['number']
        print(f"\n------------------------------------------------------------")
        print(f"Pergunta {number}: {question_text}")

        if use_rag == 1:
            retrieved_knowledge = retrieve(question_text)
            retrieved_text = '\n'.join([chunk for chunk, _ in retrieved_knowledge])
            instruction_prompt = f"Você é um assistente útil. Use apenas o seguinte contexto para responder à pergunta:\n{retrieved_text}"
            model_answer = ask_llama(question_text, options, LANGUAGE_MODEL)
        else:
            model_answer = ask_llama(question_text, options, LANGUAGE_MODEL)

        answers.append({
            "number": q["number"],
            "answer": model_answer
        })

    end_time = time.time()

    for answer in answers:
        print(f"Questão {answer['number']}: {answer['answer']}")

    print(f"\nTempo de execução: {end_time - start_time} segundos")
    safe_string = LANGUAGE_MODEL.replace(':', '')
    output_dir = f'./data/output/respostas_{safe_string}'
    output_file = f'{output_dir}/respostas_rag_{safe_string}.json'

    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(answers, f, ensure_ascii=False, indent=4)

    print(f"As respostas foram salvas em {output_file}.")
