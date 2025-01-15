import ollama
import json

# Carregar as questões em formato JSON
with open('c:/dev/estudos/LLM/RAG/respostas/respostas_compilado.json', 'r', encoding='utf-8') as f:
    respostas = json.load(f)



def normalize_answers(number, answer):
    prompt = f"Dada a seguinte resposta abaixo, retorne apenas a letra da alternativa escolhida e nenhum caractere a mais:\n\nQuestão: {number}\nResposta: {answer}\n\nResposta:"

    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
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

output_file = 'respostas_normalizadas.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(answers, f, ensure_ascii=False, indent=4)

print(f"As respostas foram salvas em {output_file}.")