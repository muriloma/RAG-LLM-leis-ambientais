import sys
import json
import csv
import os

from perguntar_modelo import choosen_model, output_file
from normalizar_respostas import normalized_output_file

#ALTERAR ARQUIVOS NAS LINHAS 6 e 9



normalized = input("Foi necessário normalizar as respostas? (s/n): ").strip().lower()

while normalized not in ['s', 'n']:
    print("Resposta inválida. Por favor, digite 's' para sim ou 'n' para não.")
    normalized = input("Foi necessário normalizar as respostas? (s/n): ").strip().lower()

if normalized == 's':
    with open(normalized_output_file, 'r', encoding='utf-8') as f:
        model_responses_file = json.load(f)

if normalized == 'n':
    with open(output_file, 'r', encoding='utf-8') as f:
        model_responses_file = json.load(f)

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


output_csv_file = f'./data/output/comparisons_{choosen_model}.csv'  # Arquivo CSV de saída

# Executar a função para comparar e gerar o CSV
compare_and_save_to_csv(model_responses_file, correct_answers_file, output_csv_file)

# Calcular a porcentagem de acertos a partir do arquivo CSV gerado
accuracy_percentage, total_questions, correct_answers = calculate_accuracy_from_csv(output_csv_file)

# Exibir o resultado
print(f"Total de questões: {total_questions}")
print(f"Total de acertos: {correct_answers}")
print(f"Porcentagem de acertos: {accuracy_percentage:.2f}%")
