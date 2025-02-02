# main.py

from configurator import get_user_input
from perguntar_modelo import main as perguntas_main
from rag_system import main as rag_main

def main():
    config = get_user_input()

    if config["num_questions"] == "1":
        num_questions = 10
    elif config["num_questions"] == "2":
        num_questions = 30
    else:
        num_questions = None

    config["num_questions"] = num_questions

    if config["use_rag"]:
        rag_main(config)
    else:
        perguntas_main(config)

if __name__ == "__main__":
    main()
