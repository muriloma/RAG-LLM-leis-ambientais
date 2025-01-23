import ollama
import json

#ALTERAR ARQUIVOS DAS LINHAS 6 e 43

# Carregar as questões em formato JSON
with open('c:/dev/estudos/LLM/RAG/docs/questoes.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)



# prompt = f"Pergunta: {question}\nEscolha a alternativa correta entre as opções. A reposta deve conter apenas a letra da alternativa. Escolha uma das alternativas abaixo, mesmo que você não saiba qual é a resposta correta, é obrigatório escolher uma alternativa:\n{options_text}\nResposta:"

def ask_llama(question, options):
    # Formatando o prompt para garantir que o modelo escolha uma das opções
    options_text = "\n".join([f"{key}: {value}" for key, value in options.items()])
    prompt = f"Pergunta: {question}\nEscolha a alternativa correta entre as opções. A reposta deve conter apenas a letra da alternativa escolhida e mais nenhum texto.\n É obrigatório escolher uma das alternativas abaixo, mesmo que você não saiba qual é a resposta correta, é obrigatório escolher uma alternativa:\n{options_text}\nResposta:"

    # Chamar o modelo Llama3.2
    response = ollama.chat(model="llama3.3", messages=[{"role": "user", "content": prompt}])
    
    return response['message']['content'].strip()  # Garantir que não haja espaços extras na resposta

# Lista para armazenar as respostas
answers = []

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

# Exibir as respostas
for answer in answers:
    print(f"Questão {answer['number']}: {answer['answer']}")

output_file = 'respostas_llama3.3.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(answers, f, ensure_ascii=False, indent=4)

print(f"As respostas foram salvas em {output_file}.")