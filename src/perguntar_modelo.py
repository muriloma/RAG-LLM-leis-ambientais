# perguntar_modelo.py

import ollama
import json
import os
import time
from configurator import get_user_input

def ask_llama(question, options, model):
    options_text = "\n".join([f"{key}: {value}" for key, value in options.items()])
    prompt = f"Pergunta: {question}\nEscolha a alternativa correta entre as opções. A reposta deve conter apenas a letra da alternativa escolhida e mais nenhum texto.\nÉ obrigatório escolher uma das alternativas abaixo, mesmo que você não saiba qual é a resposta correta, é obrigatório escolher uma alternativa:\n{options_text}\nResposta:"
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response['message']['content'].strip()

def main(config):
    LANGUAGE_MODEL = config["model"]
    num_questions = int(config["num_questions"]) if config["num_questions"] != "3" else None

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
       
        model_answer = ask_llama(question_text, options, LANGUAGE_MODEL)
        answers.append({
            "number": q["number"],
            "answer": model_answer
        })

    end_time = time.time()

    for answer in answers:
        print(f"Questão {answer['number']}: {answer['answer']}")

    print(f"Tempo de execução: {end_time - start_time} segundos")
    safe_string = LANGUAGE_MODEL.replace(':', '')
    output_dir = f'./data/output/respostas_{safe_string}'
    output_file = f'{output_dir}/respostas_{safe_string}.json'

    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(answers, f, ensure_ascii=False, indent=4)

    print(f"As respostas foram salvas em {output_file}.")
