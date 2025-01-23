import json

# Carregar as questões em formato JSON
with open('./data/input/questoes.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Verificar as primeiras perguntas carregadas
for q in questions[:2]:  # Exibindo as 2 primeiras questões
    print(f"Questão {q['number']}: {q['question']}")
    for option, answer in q['options'].items():
        print(f"{option}: {answer}")
    print()