import ollama
import json
import os
import time

#ALTERAR ARQUIVOS DAS LINHAS 6 e 43

# Carregar as questões em formato JSON
with open('./data/input/questoes.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Escolher o modelo a ser utilizado pelo ollama
choosen_model = "qwen2.5"

# prompt = f"Pergunta: {question}\nEscolha a alternativa correta entre as opções. A reposta deve conter apenas a letra da alternativa. Escolha uma das alternativas abaixo, mesmo que você não saiba qual é a resposta correta, é obrigatório escolher uma alternativa:\n{options_text}\nResposta:"

def ask_llama(question, options):
    # Formatando o prompt para garantir que o modelo escolha uma das opções
    options_text = "\n".join([f"{key}: {value}" for key, value in options.items()])
    prompt = f"Pergunta: {question}\nEscolha a alternativa correta entre as opções. A reposta deve conter apenas a letra da alternativa escolhida e mais nenhum texto.\n É obrigatório escolher uma das alternativas abaixo, mesmo que você não saiba qual é a resposta correta, é obrigatório escolher uma alternativa:\n{options_text}\nResposta:"

    # Chamar o modelo escolhido
    response = ollama.chat(model=choosen_model, messages=[{"role": "user", "content": prompt}])
    
    return response['message']['content'].strip()  # Garantir que não haja espaços extras na resposta

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
output_file = f'{output_dir}/respostas_{choosen_model}.json'

# Cria o diretório de saída se ele não existir
os.makedirs(output_dir, exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(answers, f, ensure_ascii=False, indent=4)

print(f"As respostas foram salvas em {output_file}.")