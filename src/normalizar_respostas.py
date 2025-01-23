import ollama
import json
import os

from perguntar_modelo import choosen_model, output_file

# Carregar as questões em formato JSON
with open(output_file, 'r', encoding='utf-8') as f:
    respostas = json.load(f)


def normalize_answers(number, answer):
    prompt = f"Dada a seguinte resposta abaixo, retorne apenas a letra da alternativa escolhida e nenhum caractere a mais:\n\nQuestão: {number}\nResposta: {answer}\n\nResposta:"

    response = ollama.chat(model=choosen_model, messages=[{"role": "user", "content": prompt}])
    return response['message']['content'].strip()

# Lista para armazenar as respostas
answers = []

# Perguntar ao modelo para cada questão

for resp in respostas:
    number = resp['number']
    answer = resp['answer']
    print(f"Normalizando a resposta da questão {number}")
    print(f"Resposta: {answer}")
    normalized_answer = normalize_answers(number, answer)
    answers.append({
        "number": number,
        "answer": normalized_answer
    })


# Exibir as respostas
for answer in answers:
    print(f"Questão {answer['number']}: {answer['answer']}")

normalized_output_dir = f'./data/output/respostas_{choosen_model}'
normalized_output_file = f'{normalized_output_dir}/respostas_normalizadas_{choosen_model}.json'

# Cria o diretório de saída se ele não existir
os.makedirs(normalized_output_dir, exist_ok=True)

with open(normalized_output_file, 'w', encoding='utf-8') as f:
    json.dump(answers, f, ensure_ascii=False, indent=4)

print(f"As respostas foram salvas em {normalized_output_file}.")