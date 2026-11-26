# Avaliação da Sprint 1 versus a rubrica — Projeto 2 (Estatística e Análise de Dados)

Data da avaliação: 26/11/2026
Material avaliado: `SPRINT1/Projeto 2 Sprint 1 - Grupo 6.docx` e `.docx.pdf` (relatório, 15 páginas), `SPRINT1/Notebook_1_Analise_Antes_Intervencao.ipynb`, `SPRINT1/Notebook_2_Analise_depois_da_Intervencao.ipynb`, `tests/test_notebook_structure.py`, `tests/test_notebook_2_structure.py`.
Critérios: `SPRINT1/refs/rubrica_avaliacao_1.png`, `_2.png`, `_3.png`, `ORIENTAÇÕES SPRINT 1 - PROJETO 2-4-1.pdf` e o roteiro `Python - Distribuição Normal-1-1.pdf`.

## 1. Nota final

| Visão | Nota (0–10) | Nota (0–100) |
|---|---|---|
| **Pela rubrica, com o que está entregue** | **9,80** | **98** |
| Relatório (texto, tabelas, figuras) isolado | 9,80 | 98 |
| Código dos notebooks (comandos, comentários, saídas) | — | **95** |

A rubrica soma 10 pontos, então cada ponto vale 10 na escala de 0 a 100. A nota depende do pré-requisito do notebook (seção 4, item 1).

## 2. Pontuação por critério

| Critério | Máx. | Nota | Justificativa |
|---|---|---|---|
| Pré-requisitos (notebook + PDF) | 0 | Atendido, com ressalva | PDF organizado e completo. Notebook 1 tem link do Colab; o link do Notebook 2 ficou como `[inserir link de compartilhamento do notebook]`. |
| Questão 1 — situação-problema | 0,50 | **0,50** | Contexto (1.1), problema (1.2), possível causa (1.3), importância da variável (1.4) e valores de referência com justificativa (1.5, Tabela 1). Os cinco itens de 0,1 estão presentes. |
| Questão 2 — histograma e boxplot (Planilha 1) | 0,50 | **0,50** | Figuras 1 e 2 com título, variável e unidade (segundos). |
| Questão 3 — média e desvio-padrão | 0,50 | **0,50** | 2,51 s e 0,40 s com unidade (Tabela 3). |
| Questão 4 — testes de normalidade | 1,05 | **1,05** | Histograma (pico único em 2,54–2,69 s, perto da média e mediana de 2,51 s; 68,0%, 96,0% e 100,0% contra a regra empírica), boxplot (Q2−Q1 = 0,28 e Q3−Q2 = 0,26) e Q-Q (Figura 3), cada um com conclusão. |
| Questão 5 — probabilidade em intervalo | 0,80 | **0,80** | Intervalo [2, 3] s ligado à faixa ideal; P = 0,7885 com `norm.cdf`; resultado interpretado ("cerca de 4 em cada 5 pagamentos"). |
| Questão 6 — 20% menores e 30% maiores | 1,00 | **1,00** | 2,17 s (`ppf(0,20)`) e 2,72 s (`ppf(0,70)`), os dois contextualizados com unidade. |
| Questão 7.1 — situação, intervenção, objetivo | 1,05 | **1,05** | Os três itens separados e resumidos na Tabela 7. O objetivo (manter o tempo até 6 s) é uma meta sobre a variável. |
| Questão 7.2 — gráficos da Planilha 2 | 0,50 | **0,50** | Figuras 4 e 5 com título, variável e unidade. |
| Questão 7.3 — média e desvio-padrão (Planilha 2) | 0,50 | **0,50** | 5,10 s e 0,81 s (Tabela 8). |
| Questão 7.4 — intervalo e quantidade | 1,00 | **0,90** | Pergunta e contagem (85 de 100) corretas e ligadas ao objetivo. Desconto de 0,10 porque o intervalo é [0, 6] s e o p da Questão 5 é [2, 3] s; as orientações da Sprint 2 pedem exatamente essa checagem. |
| Questão 8 — comparação preliminar | 1,60 | **1,60** | Pergunta sobre indícios de mudança (0,80) e dois critérios ligados ao objetivo e à intervenção (0,40 cada): proporção até 3 s (89% → 0%) e até 6 s (100% → 85%), com Tabela 9, Figura 6 e conclusão preliminar. |
| Qualidade da entrega | 1,00 | **0,90** | PDF organizado, com capa, sumário, tabelas, fontes e texto explicativo. Desconto de 0,10 pelo link em branco nas referências. |
| **Total** | **10,00** | **9,80** | |

## 3. Conferência dos números

Recalculei tudo direto das planilhas e dos notebooks.

| Valor no relatório | Recalculado | Status |
|---|---|---|
| Planilha 1: n = 300, média 2,51, mediana 2,51, desvio 0,40, mín. 1,47, máx. 3,45 | idem | ok |
| 267 de 300 (89,0%) em até 3 s; 300 de 300 em até 6 s | idem | ok |
| ±1, ±2, ±3 desvios: 204, 288, 300 observações | idem (limites arredondados como no notebook; sem arredondar dá 203 no primeiro) | ok |
| Q1 = 2,23; Q2 = 2,51; Q3 = 2,77; limites de Tukey 1,42 e 3,59 | 2,23; 2,51; 2,7725; 1,416 e 3,586 | ok |
| P(2 ≤ X ≤ 3) = 0,7885 | 0,7885 com o método da disciplina (0,7881 sem arredondar) | ok |
| 20% menores ≤ 2,17 s; 30% maiores ≥ 2,72 s | 2,1734 e 2,7198 | ok |
| Planilha 2: média 5,10, mediana 5,12, desvio 0,81, mín. 3,01, máx. 6,87; 85 de 100 em até 6 s; 0 em até 3 s | idem | ok |

Nenhum número do relatório está errado. O texto do relatório também bate com os textos dos notebooks.

## 4. Riscos e pontos de melhoria, do mais grave ao menor

1. **Link do Notebook 2 em branco (risco alto).** Nas Referências consta `[inserir link de compartilhamento do notebook]`. A rubrica diz que o envio do notebook é pré-requisito para corrigir todos os critérios que envolvem comandos do Python. Se o Notebook 2 não foi enviado de outra forma (arquivo no Canvas, por exemplo), as questões 7.2, 7.3, 7.4 e 8 correm risco. Corrigir o link ou anexar o arquivo.
2. **Intervalos diferentes nas Questões 5 e 7.4.** [2, 3] s na 5 e [0, 6] s na 7.4. É defensável para a rubrica da Sprint 1, mas gera uma comparação de p com p̂ em intervalos distintos na Sprint 2. A Sprint 2 já corrigiu isso (seção 2 do relatório da Sprint 2).
3. **RA de Nicollas Tavares da Silva com 7 dígitos (2502655).** Os outros três têm 8 dígitos. Pode ser erro de digitação; vale conferir.
4. **Numeração das seções com ponto final** ("1.1.", "2.3.1."). A NBR 6024 pede a numeração sem pontuação ("1.1", "2.3.1"). A fonte (Times New Roman 12), o espaçamento 1,5 e as margens 3/3/2/2 cm já estão no padrão.
5. **Rótulo do Q-Q em inglês** ("Theoretical Quantiles"). Colocar "Quantis teóricos (distribuição normal)" deixaria o gráfico todo em português, como os demais.
6. **Nome do arquivo `.docx.pdf`.** Renomear para `Projeto 2 Sprint 1 - Grupo 6.pdf`.
7. **Capa sem a data completa nem o local.** Tem "Novembro, 2026"; a NBR 14724 prevê o local (Campinas) e o ano.

## 5. Avaliação do código dos notebooks (95/100)

**Pontos fortes**
- Os comandos seguem o roteiro "Python – Distribuição Normal": `pd.read_excel`, `sns.histplot(kde=True)`, `sns.boxplot`, `sm.qqplot(line='r')`, `norm.cdf` e `norm.ppf` com `loc` e `scale`, e arredondamento em 2 casas. Os imports `numpy`, `statsmodels`, `scipy.stats.norm` e `pylab` estão cobertos pela exceção da SPRINT1 no `AGENTS.md`.
- Cada comando tem comentário explicativo.
- Gráficos com título, variável e unidade; Q-Q com título e unidade no eixo y.
- Notebook 1 cobre as Questões 1 a 6 e o Notebook 2 as Questões 7 e 8; os dois executam do início ao fim, com saídas gravadas.
- Os 3 testes de estrutura dos notebooks passam (parte dos 81 testes da última rodada).

**Descontos**
- Rótulo do eixo x do Q-Q em inglês (−1).
- Caminho `../Refs/...` serve para o repositório, mas o relatório diz que a análise foi feita no Colab; é preciso lembrar de subir as planilhas no Colab (−1).
- Células repetidas (histograma e boxplot por planilha) poderiam seguir o mesmo padrão exato do roteiro (−1).
- Notebook 2 depende de reler a Planilha 1 só na Questão 8; está documentado, mas é uma segunda leitura (−1).
- Link do Notebook 2 ausente no relatório (−1).

## 6. Coerência com a Sprint 2

O relatório da Sprint 1 foi usado como base para a Sprint 2. Conferi os pontos que a Sprint 2 reaproveita.

| Item | Sprint 1 | Sprint 2 | Status |
|---|---|---|---|
| Média e desvio da Planilha 1 | 2,51 s e 0,40 s | μ = 2,51 e σ = 0,40 | coerente |
| p da Questão 5 | 0,7885 | p₀ = 0,7885 (mesmo comando) | coerente |
| Planilha 2 | 5,10 s e 0,81 s; 85/100 até 6 s | x̄ = 5,10; s = 0,81; 85/100 | coerente |
| Intervalo da proporção | [2, 3] (Q5) e [0, 6] (Q7.4) | [2, 3] nos dois, p̂ = 0/100 | corrigido na Sprint 2 |
| Pergunta da Questão 8 | composta ("mudou… e manteve aceitável") | reformulada com sentido e valor de referência | corrigido na Sprint 2 |
| Conclusão preliminar | etapa mantida, com ressalvas; verificação formal na Sprint 2 | testes rejeitam H₀ e confirmam | coerente |
| Capa | Escola Politécnica, Grupo 6, 4 integrantes | mesma capa (agora preenchida) | ajustado |
| Referências | autoria institucional (PUC-Campinas) | mesma convenção, mais o relatório do Grupo 6 | ajustado |

Resumo: a Sprint 2 continua a Sprint 1 sem contradição de números.

📎 Notas do Obsidian consultadas: busca por "PUC-Campinas" e "Sprint 1" (índice da disciplina Estatística e Análise de Dados e demais módulos), apenas para conferir instituição e disciplina.
