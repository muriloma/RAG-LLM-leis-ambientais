# Tutorial: Testando Modelo LLM com Ollama

## Requisitos Prévios
- Python 3.12.8
- Ollama instalado
- Bibliotecas Python:
  ```bash
  pip install ollama
  ```

## Estrutura do Projeto

### Arquivos Necessários
1. `questoes.json`: Arquivo com as perguntas
2. `gabarito.json`: Gabarito das respostas corretas

### Scripts do Projeto

#### 1. `perguntar_modelo.py`
- Objetivo: Carregar perguntas do JSON e obter respostas do modelo
- Passos:
  1. Carregar perguntas do JSON
  2. Definir variável `prompt` para instruções do modelo
  3. Definir variável `response` com o modelo Ollama
  4. Iterar sobre as perguntas
  5. Salvar respostas em lista `answers`
  6. Exportar respostas para JSON

**Prompt Específico**: Responder apenas com a letra da alternativa correta

#### 2. `normalizar_respostas.py`
- Objetivo: Padronizar respostas do modelo
- Processo:
  1. Carregar respostas geradas anteriormente
  2. Usar novo prompt para normalizar formato
  3. Gerar `respostas_normalizadas.json`

#### 3. `comparar_resp.py`
- Objetivo: Comparar respostas do modelo com gabarito
- Etapas:
  1. Carregar respostas do modelo e gabarito
  2. Comparar respostas
  3. Gerar arquivo CSV com:
     - Questão
     - Resposta do Modelo
     - Resposta Correta
     - Resultado (Booleano)
  4. Calcular métricas:
     ```python
     print(f"Total de questões: {total_questions}")
     print(f"Total de acertos: {correct_answers}")
     print(f"Porcentagem de acertos: {accuracy_percentage:.2f}%")
     ```

## Fluxo de Instalação
1. Instalar o Ollama na máquina local:
    - As instruções de download e instalação podem ser encontradas em [Ollama](https://github.com/ollama/ollama/blob/ca2f9843c8c71491d5abf626c73508e5a1685cea/README.md)

2. Instalar a biblioteca python Ollama através do comando no seu terminal:
```bash
  pip install ollama
  ```

3. Baixar pelo menos 1 modelo de LLM do ollama, recomendamos o `qwen2.5` ou o `llama3.2`. Exemplo:
```bash
  ollama pull llama3.2
```

4. Para verificar se o modelo foi baixado utilize o comando
```bash
  ollama list
  ```

## Fluxo de Execução
1. Inciar o servidor ollama no terminal
```bash
  ollama serve
  ```

2. No arquivo `perguntar_modelo.py` definir na linha ``12`` o modelo que foi escolhido, modificando a variável `choosen_model`
```python
  choosen_model = 'nome do modelo escolhido'
```

3. Executar `perguntar_modelo.py` em um novo terminal com o comando
```bash
  python .\src\perguntar_modelo.py  
  ```

4. As respostas serão salvas em um arquivo na pasta `./data/output/respostas_nome_do_modelo/respostas_nome_do_modelo.json`. 
Caso as respostas não estejam no padrão do exemplo abaixo:
```json
  {
    "number": 4,
    "answer": "a"
  },
  {
    "number": 5,
    "answer": "e"
  },
  ```
  Devem executar o arquivo `normalizar_respostas.py` com o comando no terminal:
  ```bash
  python .\src\normalizar_respostas.py 
  ```
  Isso fará com que o arquivo de respostas seja tratado novamente pelo modelo, para obter um arquivo .json padronizado

5. Excutar o arquivo `comparar_resp.py` pelo comando no terminal:
```bash
  python .\src\comparar_resp.py 
  ```
  O script irá perguntar se foi necessário normalizar as respostas, você deve responder com 's' para sim e 'n' para não.
  Em seguida ele executará os comandos e fará a comparação das respostas obtidas pelo modelo e o gabarito das perguntas, mostrando assim o percentual de acerto do teste.
  
## Dicas
- Verifique o formato dos JSONs
- Garanta que os prompts estejam claros
- Monitore as saídas de cada script
