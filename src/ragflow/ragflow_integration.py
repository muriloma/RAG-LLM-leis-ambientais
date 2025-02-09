import requests
import time
import json
import os
import csv


# endereco do RagFlow
ep = "http://127.0.0.1:"
apikey = "ragflow-NhNzEyNDQyZTBmOTExZWZhZmRjMDI0Mm"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {apikey}"
}

# Carregar as questões em formato JSON
with open('./data/input/questoes.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Escolher o modelo a ser utilizado pelo RagFlow
choosen_model = "llama3.2"



def ask_ragflow(prompt, ep, headers):
    # lista os assistentes de chat 
    url = f"{ep}/api/v1/chats"
    response = requests.get(url, headers=headers)
    chat_id = response.json()['data'][0]['id']
    print(f"chat_id = {chat_id}")


    # Criar uma nova 'conversa' / sessao
    url = f"{ep}/api/v1/chats/{chat_id}/sessions"
    payload = {
        "name": "Pergunta1",
    }
    response = requests.post(url, json=payload, headers=headers)
    session_id = response.json()['data']['id']

    # interage com a 'conversa' / sessao
    url = f"{ep}/api/v1/chats/{chat_id}/completions"
    payload = {
        "question": prompt,
        "stream": False,
        "session_id": session_id
    }
    response = requests.post(url, json=payload, headers=headers)
    resposta  = response.json()['data']['answer'].strip()

    # Apaga a 'conversa' / sessao 
    url = f"{ep}/api/v1/chats/{chat_id}/sessions"
    payload = {
        "ids": [session_id],
    }
    requests.delete(url, json=payload, headers=headers)

    return resposta


# Realizar pergunta ao modelo pelo ragflow
def ask_llama(question, options):
    # Formatando o prompt para garantir que o modelo escolha uma das opções
    options_text = "\n".join([f"{key}: {value}" for key, value in options.items()])
    prompt = f"Pergunta: {question}\nEscolha a alternativa correta entre as opções. A reposta deve conter apenas a letra da alternativa escolhida e mais nenhum texto.\n É obrigatório escolher uma das alternativas abaixo, mesmo que você não saiba qual é a resposta correta, é obrigatório escolher uma alternativa:\n{options_text}\n"

    resposta = ask_ragflow(prompt, ep, headers)    

    while len(resposta) > 1:
        resposta = normalize_answers(resposta)

    return resposta

def normalize_answers(answer):
    prompt = f"Dada a seguinte resposta abaixo, retorne apenas a letra da alternativa escolhida e nenhum caractere a mais:\n\nResposta: {answer}\n"
    resposta = ask_ragflow(prompt, ep, headers)
    return resposta

# Lista para armazenar as respostas
answers = []

start_time = time.time() # Iniciar a contagem do tempo


# Perguntar ao modelo para cada questão
for q in questions:
    question_text = q['question']
    options = q['options']
    print(f"Perguntando ao modelo: {question_text}")

    model_answer = ask_llama(question_text, options)
    answers.append({
        "number": q["number"],
        "answer": model_answer
    })

end_time = time.time() # Finalizar a contagem do tempo


# Exibir as respostas
for answer in answers:
    print(f"Questão {answer['number']}: {answer['answer']}")
    
print(f"Tempo de execução: {end_time - start_time} segundos")

output_dir = f'./data/output/respostas_{choosen_model}'
output_file = f'{output_dir}/respostas_{choosen_model}_Ragflow.json'

# Cria o diretório de saída se ele não existir
os.makedirs(output_dir, exist_ok=True)

# Cria o arquivo de saída com as respostas em formato JSON
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(answers, f, ensure_ascii=False, indent=4)


# Carrega as respostas como JSON
with open(output_file, 'r', encoding='utf-8') as f:
        model_responses_file = json.load(f)

# Carrega o gabarito com JSON
with open('./data/input/gabarito.json', 'r', encoding='utf-8') as f:
    correct_answers_file = json.load(f)


# Função para comparar as respostas e gerar o CSV
def compare_and_save_to_csv(model_responses_file, correct_answers_file, output_csv_file):

    # Criar um dicionário de respostas corretas para facilitar a comparação
    correct_dict = {item['number']: item['answer'][0].lower() for item in correct_answers_file}

    # Criar uma lista para armazenar os resultados da comparação
    results = []

    # Comparar as respostas do modelo com as respostas corretas
    for response in model_responses_file:
        question_number = response['number']
        model_answer = response['answer'].lower()  # Resposta do modelo em letras maiúsculas
        correct_answer = correct_dict.get(question_number)  # Resposta correta (se existir)

        # Comparar as respostas
        is_correct = (model_answer == correct_answer)
        results.append([question_number, model_answer, correct_answer, is_correct])

    # Escrever os resultados no arquivo CSV
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Questão', 'Resposta do Modelo', 'Resposta Correta', 'Resultado'])  # Cabeçalho
        csv_writer.writerows(results)  # Escrever as linhas com os resultados

    print(f"Arquivo CSV gerado: {output_csv_file}")


def calculate_accuracy_from_csv(csv_file):
    total_questions = 0
    correct_answers = 0

    # Ler o arquivo CSV e contar os acertos
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Pular o cabeçalho
        for row in csv_reader:
            total_questions += 1
            if row[3].strip().lower() == 'true':  # Verificar se a resposta é 'True'
                correct_answers += 1

    # Calcular a porcentagem de acertos
    accuracy_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    return accuracy_percentage, total_questions, correct_answers

# Arquivo CSV de saída
output_csv_file = f'./data/output/comparisons_{choosen_model}.csv'  

# Executar a função para comparar e gerar o CSV
compare_and_save_to_csv(model_responses_file, correct_answers_file, output_csv_file)

# Calcular a porcentagem de acertos a partir do arquivo CSV gerado
accuracy_percentage, total_questions, correct_answers = calculate_accuracy_from_csv(output_csv_file)

# Exibir o resultado
print(f"Total de questões: {total_questions}")
print(f"Total de acertos: {correct_answers}")
print(f"Porcentagem de acertos: {accuracy_percentage:.2f}%")
