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

## Fluxo de Execução
1. Rodar `perguntar_modelo.py`
2. Executar `normalizar_respostas.py`
3. Processar com `comparar_resp.py`

## Dicas
- Verifique o formato dos JSONs
- Garanta que os prompts estejam claros
- Monitore as saídas de cada script
