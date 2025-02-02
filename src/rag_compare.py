# rag_compare.py
import json
import csv
from colorama import Fore, init
from tabulate import tabulate

# Inicializa o colorama
init(autoreset=True)

# Arquivos de entrada
model_responses_file_1 = './data/output/respostas_qwen14b/respostas_rag_qwen14b.json'
model_responses_file_2 = './data/output/respostas_qwen14b/respostas_qwen14b.json'

# Arquivo do gabarito
gabarito_file = './data/input/gabarito.json'

# Função para comparar as respostas e gerar o CSV
def compare_and_save_to_csv(model_responses_file_1, model_responses_file_2, correct_answers_file, output_csv_file):
    # Criar um dicionário de respostas corretas para facilitar a comparação
    correct_dict = {item['number']: item['answer'][0].lower() for item in correct_answers_file}

    # Criar uma lista para armazenar os resultados da comparação
    results = []

    # Comparar as respostas do modelo 1 e modelo 2 com as respostas corretas
    for response_1, response_2 in zip(model_responses_file_1, model_responses_file_2):
        question_number_1 = response_1['number']
        model_answer_1 = response_1['answer'].lower()  # Resposta do modelo 1
        model_answer_2 = response_2['answer'].lower()  # Resposta do modelo 2
        correct_answer = correct_dict.get(question_number_1)  # Resposta correta (se existir)

        # Comparar as respostas
        is_correct_1 = (model_answer_1 == correct_answer)
        is_correct_2 = (model_answer_2 == correct_answer)
        results.append([question_number_1, model_answer_1, model_answer_2, correct_answer, is_correct_1, is_correct_2])

    # Escrever os resultados no arquivo CSV
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Questão', 'Resposta Modelo 1', 'Resposta Modelo 2', 'Resposta Correta', 'Resultado Modelo 1', 'Resultado Modelo 2'])  # Cabeçalho
        csv_writer.writerows(results)  # Escrever as linhas com os resultados

    print(Fore.GREEN + f"Arquivo CSV gerado: {output_csv_file}")

def calculate_accuracy_from_csv(csv_file):
    total_questions = 0
    correct_answers_1 = 0
    correct_answers_2 = 0

    # Ler o arquivo CSV e contar os acertos
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Pular o cabeçalho
        for row in csv_reader:
            total_questions += 1
            if row[4].strip().lower() == 'true':  # Verificar se o Modelo 1 acertou
                correct_answers_1 += 1
            if row[5].strip().lower() == 'true':  # Verificar se o Modelo 2 acertou
                correct_answers_2 += 1

    # Calcular a porcentagem de acertos
    accuracy_percentage_1 = (correct_answers_1 / total_questions) * 100 if total_questions > 0 else 0
    accuracy_percentage_2 = (correct_answers_2 / total_questions) * 100 if total_questions > 0 else 0
    return accuracy_percentage_1, accuracy_percentage_2, total_questions, correct_answers_1, correct_answers_2

# Ler os arquivos de respostas dos modelos
with open(model_responses_file_1, 'r', encoding='utf-8') as f:
    model_responses_file_1 = json.load(f)

with open(model_responses_file_2, 'r', encoding='utf-8') as f:
    model_responses_file_2 = json.load(f)

# Ler o arquivo do gabarito
with open(gabarito_file, 'r', encoding='utf-8') as f:
    correct_answers_file = json.load(f)

output_csv_file = './data/output/rag_comparison.csv'  # Arquivo CSV de saída

# Executar a função para comparar e gerar o CSV
print(Fore.YELLOW + "Iniciando a comparação das respostas...")
compare_and_save_to_csv(model_responses_file_1, model_responses_file_2, correct_answers_file, output_csv_file)

# Calcular a porcentagem de acertos a partir do arquivo CSV gerado
accuracy_percentage_1, accuracy_percentage_2, total_questions, correct_answers_1, correct_answers_2 = calculate_accuracy_from_csv(output_csv_file)

# Exibir o resultado visualmente
table_data = [
    ['Modelo', 'Acertos', 'Porcentagem de Acertos'],
    [f'{Fore.CYAN}SEM RAG', f'{Fore.GREEN}{correct_answers_1}', f'{Fore.GREEN}{accuracy_percentage_1:.2f}%'],
    [f'{Fore.CYAN}COM RAG', f'{Fore.GREEN}{correct_answers_2}', f'{Fore.GREEN}{accuracy_percentage_2:.2f}%'],
]

table = tabulate(table_data, headers='firstrow', tablefmt='fancy_grid')

print(Fore.LIGHTMAGENTA_EX + "\nResultado da Comparação:")
print(table)

# Exibir resultados finais de forma destacada
print(Fore.LIGHTYELLOW_EX + "\nResumo Final:")
if accuracy_percentage_1 > accuracy_percentage_2:
    print(Fore.GREEN + f"Modelo 1 foi o mais preciso com {accuracy_percentage_1:.2f}% de acertos.")
elif accuracy_percentage_2 > accuracy_percentage_1:
    print(Fore.GREEN + f"Modelo 2 foi o mais preciso com {accuracy_percentage_2:.2f}% de acertos.")
else:
    print(Fore.YELLOW + "Ambos os modelos tiveram a mesma porcentagem de acertos.")
