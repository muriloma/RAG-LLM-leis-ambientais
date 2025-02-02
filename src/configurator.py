# configurator.py
import colorama
from colorama import Fore

colorama.init(autoreset=True)

def get_user_input():
    print(Fore.CYAN + "Quantas perguntas serão testadas?")
    print(Fore.GREEN + "1. 10 perguntas")
    print(Fore.GREEN + "2. 30 perguntas")
    print(Fore.GREEN + "3. Todas as perguntas")
    num_questions = input(Fore.YELLOW + "Escolha uma opção (1/2/3): ")

    print(Fore.CYAN + "\nEscolha o modelo:")
    print(Fore.GREEN + "1. qwen:14b")
    print(Fore.GREEN + "2. llama:3.1")
    print(Fore.GREEN + "3. deepseek")
    model_choice = input(Fore.YELLOW + "Escolha uma opção (1/2/3): ")
    model = {
        '1': 'qwen:14b',
        '2': 'llama:3.1',
        '3': 'deepseek'
    }.get(model_choice, 'qwen:14b')

    print(Fore.CYAN + "\nDeseja usar RAG? (1 para sim, 2 para não)")
    use_rag_choice = input(Fore.YELLOW + "Escolha uma opção: ").strip()
    use_rag = use_rag_choice == '1'

    dataset_name = None
    if use_rag:
        print(Fore.CYAN + "Deseja usar o dataset padrão? (1 para sim, 2 para não)")
        use_default_dataset = input(Fore.YELLOW + "Escolha uma opção: ").strip()
        use_default_dataset = use_default_dataset == '1'
        if not use_default_dataset:
            dataset_name = input(Fore.YELLOW + "Digite o nome do dataset do Hugging Face: ").strip()

    print(Fore.MAGENTA + "\n------------------------------------------------------------")

    return {
        "num_questions": num_questions,
        "use_rag": use_rag,
        "dataset_name": dataset_name,
        "model": model,
        "compare_responses": False
    }