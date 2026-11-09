# CHANGES

## refactor(sprint1): separar notebooks por planilha e usar os comandos do PDF de Distribuição Normal

### Contexto

O notebook `SPRINT1/Notebook_1_Analise_Antes_Intervencao.ipynb` misturava as duas planilhas (Questões 1 a 8) e deixava a Questão 1, a Questão 7.1 e os valores de referência como "provisórios / preencher manualmente". Além disso, os cálculos da distribuição normal eram feitos à mão com `math`, diferente dos comandos do material `SPRINT1/refs/Python - Distribuição Normal-1-1.pdf`. A análise foi dividida por planilha, todos os textos passaram a seguir a situação-problema do grupo e o código passou a usar exatamente os comandos do PDF.

Situação-problema:

> A empresa de e-commerce adicionou uma etapa extra de validação antifraude nos pagamentos via Pix. Isso deixa o processamento mais lento, e o grupo investiga se o tempo ainda é aceitável.

Valores de referência adotados (decisão do grupo, com base no comportamento da Planilha 1):

- **Faixa ideal:** 2 a 3 segundos (onde se concentra a maior parte das transações antes da intervenção; percepção de pagamento instantâneo).
- **Limite tolerável:** até 6 segundos (dobro do teto da faixa ideal).

### Comandos iguais ao PDF "Python - Distribuição Normal" (nos dois notebooks)

| Etapa do PDF | Comando usado |
|---|---|
| 1. Importar as bibliotecas | `import pandas as pd`, `import numpy as np`, `import math`, `import seaborn as sns`, `import matplotlib.pyplot as plt`, `import statsmodels.api as sm`, `from scipy.stats import norm`, `import pylab` |
| 2. Variáveis | `arquivo = "..."`, `coluna = "Tempo_processamento_seg"` |
| 3. Armazenamento | `df=pd.read_excel(arquivo)` e `df` |
| 4.1 Histograma | `sns.histplot(data=df[coluna],kde=True)` e `plt.show()` |
| 4.2 Boxplot | `sns.boxplot(data=df[coluna])` e `plt.show()` |
| 5. Média, mediana e desvio-padrão (padrão do Projeto 1) | `media = round(df[coluna].mean(), 2)`, `mediana = round(df[coluna].median(), 2)`, `dpad = round(df[coluna].std(), 2)` |
| 6.1 Limites | `limite_inf1dp=round(media-dpad,2)` … `limite_sup3dp=round(media+3*dpad,2)` |
| 6.1 Quantidades | `quantidade_1dp=sum(i>=limite_inf1dp and i<= limite_sup1dp for i in df[coluna].sort_values())` (e 2dp, 3dp) |
| 6.1 Porcentagens | `porcentagem1 = round((quantidade_1dp/len(df[coluna]))*100,2)` (e 2, 3) |
| 6.2 Quartis (padrão do Projeto 1) | `Q1 = df[coluna].quantile(q=0.25)`, `Q2 = ...(q=0.50)`, `Q3 = ...(q=0.75)` |
| 6.3 Gráfico Q-Q | `sm.qqplot(df[coluna], line = 'r')` e `pylab.show()` |
| 7. Probabilidade (Q5) | `norm.cdf(3,loc=media,scale=dpad).round(4)-norm.cdf(2,loc=media,scale=dpad).round(4)` |
| Quantis (Q6) | `norm.ppf(0.20,loc=media,scale=dpad).round(2)` e `norm.ppf(0.70,loc=media,scale=dpad).round(2)` |

- Removidos os cálculos feitos à mão: as funções `cdf_normal_padrao` (com `math.erf`) e `quantil_normal_padrao` (bissecção), o Q-Q montado manualmente e a curva normal desenhada com `math.exp` sobre o histograma.
- Mantidos, por exigência da rubrica, `plt.title`, `plt.xlabel` e `plt.ylabel` entre o comando do gráfico e o `plt.show()`, identificando variável, unidade e título.
- Como no PDF, média e desvio-padrão entram arredondados em 2 casas em `loc` e `scale`. Por isso a probabilidade da Q5 passou de 78,81% para **78,85%**; os quantis da Q6 continuam 2,17 s e 2,72 s.
- A regra empírica agora aparece como 68%-95%-99% no código e no texto, como nas orientações da Sprint (antes o print dizia 99,7% e o texto 99%).

### Notebook 1 — `SPRINT1/Notebook_1_Analise_Antes_Intervencao.ipynb` (reescrito)

- Contém **somente** a Planilha 1 (300 observações), na variável `df`, e as Questões 1 a 6.
- Removidos: a Planilha 2 e todas as seções das Questões 7.1 a 8.
- **Questão 1:** texto completo, com os cinco itens da rubrica rotulados (contexto, problema, possível causa, importância da variável e valores de referência com justificativa).
- **Questão 2:** histograma e boxplot com título, variável e unidade (segundos).
- **Questão 3:** média 2,51 s, mediana 2,51 s e desvio-padrão 0,40 s.
- **Questão 4:** itens 6.1, 6.2 e 6.3 do PDF, cada um com uma conclusão, mais uma "Conclusão geral" que justifica o uso da distribuição normal.
- **Questão 5:** P(2 ≤ x ≤ 3) = 78,85%, com justificativa do intervalo (faixa ideal) e contextualização.
- **Questão 6:** 2,17 s (máximo dos 20% menores) e 2,72 s (mínimo dos 30% maiores), contextualizados.
- Célula final "Síntese da Planilha 1", que liga os resultados ao Notebook 2.

### Notebook 2 — `SPRINT1/Notebook_2_Analise_depois_da_Intervencao.ipynb` (novo)

- Mesmos imports e o mesmo padrão `arquivo` / `coluna` / `df=pd.read_excel(arquivo)`, agora com a Planilha 2 (100 observações).
- **Questão 7.1:** Situação (reforço contra fraudes com risco de lentidão), Ação (etapa extra de validação antifraude) e Objetivo (manter o tempo em até 6 s), com pergunta de decisão.
- **Questão 7.2:** histograma (`sns.histplot(data=df[coluna],kde=True)`) e boxplot com título e unidade, mais uma interpretação.
- **Questão 7.3:** média 5,10 s, mediana 5,12 s e desvio-padrão 0,81 s, mais uma interpretação comparando com a Planilha 1.
- **Questão 7.4:** intervalo de 0 a 6 s; a contagem usa o mesmo padrão `sum(i>=... and i<= ...)` do PDF: 85 de 100 (e 0 de 100 na faixa ideal).
- **Questão 8:** pergunta e dois critérios:
  - Critério 1: até 3 s (ideal): 89% → 0%.
  - Critério 2: até 6 s (tolerável): 100% → 85%.
  - Tabela comparativa, boxplot lado a lado com as linhas de 3 s e 6 s e diferença entre as médias (+2,59 s), com aviso único de que a comparação não comprova causalidade.
  - A Planilha 1 é lida em `df_antes` apenas nesta seção.

Os dois notebooks foram executados de ponta a ponta e salvos com as saídas, e os valores impressos foram conferidos com os textos de interpretação.

### Testes (`tests/`)

- `tests/test_notebook_structure.py`: reescrito para o Notebook 1. Exige os imports do PDF e os comandos literais do PDF (leitura, histograma, boxplot, limites, quantidades, porcentagens, `sm.qqplot`, `norm.cdf`, `norm.ppf`) e os do Projeto 1 (média, mediana, desvio-padrão, quartis). Também confere que não há funções feitas à mão (`def`, `math.erf`, `math.exp`), que só a Planilha 1 é usada, a Questão 1 completa, as interpretações com os valores (78,85% etc.), o README, as dependências em `requirements.txt` e a execução de ponta a ponta.
- `tests/test_notebook_2_structure.py` (novo): estrutura das Questões 7.1 a 8, imports do PDF, `df=pd.read_excel(arquivo)` com a Planilha 2, Planilha 1 lida só na Questão 8, comandos dos gráficos, média e desvio-padrão, contagem do intervalo, critérios, aviso de causalidade, interpretações e execução de ponta a ponta.
- `tests/test_backend_comments.py`: checagem dinâmica nos dois notebooks; cada comando de nível superior precisa de um comentário logo acima.
- Resultado: `python -m unittest tests.test_notebook_structure tests.test_notebook_2_structure tests.test_backend_comments` → 37 testes, todos OK.

### Documentação, dependências e regras

- `README.md`: seção "Executar os notebooks" com a situação-problema, as referências, a ordem dos notebooks e o comando dos testes.
- `requirements.txt`: adicionados `numpy`, `scipy` e `statsmodels` (exigidos pelo PDF) e `nbformat` e `nbclient` (testes de execução). `scipy` e `statsmodels` foram instalados no `.venv`.
- `AGENTS.md` (arquivo local, ignorado pelo git): registrada a exceção aprovada para usar as bibliotecas do PDF nos notebooks da SPRINT1.
