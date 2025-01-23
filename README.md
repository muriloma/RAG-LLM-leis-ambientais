# RELATÓRIO TREINAMENTO DE MODELO

> **Sumário**
>
> 1. [Resumo](#resumo)
> 2. [Introdução](#introdução)
> 3. [Metodologia](#metodologia)
> 4. [Resultados e Discussão](#resultados-e-discussão)
> 5. [Conclusão](#conclusão)
> 6. [Trabalhos Futuros](#trabalhos-futuros)
> 7. [Referências](#referências)

## Desenvolvimento e Teste de um Modelo Local de Linguagem para Questões Jurídicas em Propriedade Ambiental

---

### Resumo

Este trabalho apresenta o processo de treinamento, ajuste e avaliação de um modelo local de linguagem para auxiliar na interpretação de leis relacionadas à propriedade ambiental no Brasil. A pesquisa foi baseada em dados extraídos de legislações públicas disponíveis no site oficial do Governo Federal, seguidas pela criação e refinamento de perguntas para validar o desempenho do modelo.

---

### Introdução

O avanço das tecnologias de linguagem natural (LLMs) tem gerado oportunidades significativas no campo jurídico, oferecendo suporte na interpretação de legislações e no acesso à informação jurídica. Este estudo busca explorar o desenvolvimento de um modelo local voltado para a compreensão de leis de propriedade ambiental, destacando etapas de coleta de dados, criação de perguntas e validação do desempenho do modelo.

---

### Metodologia

#### 1. Coleta de Dados

O trabalho iniciou com a coleta de textos legais diretamente do site oficial do Governo Federal do Brasil. As seguintes legislações foram selecionadas:

| Legislação                 | Descrição                                                                                                                                                                 |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Lei nº 14.904, de 2024** | Trata sobre modificações em regulações ambientais, estabelecendo diretrizes para a gestão de propriedades que impactam áreas de preservação permanente e uso sustentável. |
| **Lei nº 14.850, de 2024** | Dispõe sobre penalidades e responsabilidades administrativas relacionadas ao descumprimento de normas de preservação ambiental.                                           |

#### 2. Geração e Refinamento de Perguntas

- Utilização do ChatGPT-4 para geração automática de perguntas
- Revisão manual pela equipe de pesquisa
- Elaboração de 50 perguntas finais focadas em tópicos jurídicos específicos

#### 3. Treinamento e Teste do Modelo

---

### Resultados e Discussão

#### Desempenho do Modelo

O modelo demonstrou capacidade mediana em:

- ✓ Identificação de direitos ambientais
- ✓ Detalhamento de obrigações legais
- ✓ Interpretação de sanções previstas

#### Desafios Encontrados

- 🚫 Necessidade de ajuste em perguntas automáticas
- 🚫 Limitações na compreensão de termos jurídicos complexos

---

### Conclusão

A pesquisa demonstrou o potencial de modelos locais de linguagem para atuar como ferramentas auxiliares na interpretação de leis específicas. Apesar dos desafios enfrentados, os resultados destacam a importância de um processo de curadoria rigoroso tanto no corpus quanto na geração de perguntas para garantir a precisão das respostas.

---

### Trabalhos Futuros

1. Expansão do corpus jurídico com outras legislações ambientais
2. Implementação de técnicas de pré-treinamento em linguagem jurídica

---

1. [Governo Federal do Brasil. Lei nº 14.904, de 2024.](https://www2.camara.leg.br/legin/fed/lei/2024/lei-14904-27-junho-2024-795864-publicacaooriginal-172234-pl.html#:~:text=Estabelece%20diretrizes%20para%20a%20elabora%C3%A7%C3%A3o,2009%3B%20e%20d%C3%A1%20outras%20provid%C3%AAncias.)
2. [Governo Federal do Brasil. Lei nº 14.850, de 2024.](https://www2.camara.leg.br/legin/fed/lei/2024/lei-14850-2-maio-2024-795555-publicacaooriginal-171660-pl.html#:~:text=Institui%20a%20Pol%C3%ADtica%20Nacional%20de%20Qualidade%20do%20Ar.&text=Art.,do%20ar%20no%20territ%C3%B3rio%20nacional.)
