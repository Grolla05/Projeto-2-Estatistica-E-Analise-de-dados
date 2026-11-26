# CHANGES — Sprint 2: testes de hipótese (notebook só com código + relatório Word)

## Resumo

Entrega da Sprint 2 dividida em duas partes:
- **Notebook** `SPRINT2/Notebook_Sprint2_Testes_de_Hipotese.ipynb`: somente código, com comentários que explicam cada comando e cada fórmula. As células Markdown são apenas títulos curtos.
- **Relatório Word** `SPRINT2/Relatorio_Sprint2.docx`: todos os textos (situação, pergunta, metodologia, fórmulas, resultados, decisões, conclusões e discussão), em texto estruturado e sem o formato de "respostas às questões", conforme a rubrica.

Resultados: teste da média z = 64,75 (H1: μ > 2,51 s) e teste da proporção no intervalo [2, 3] s z = −19,31 (H1: p < 0,7885). Os valores críticos são ±2,326 (1%) e ±1,645 (5%). H0 é rejeitada nos dois testes e nos dois níveis.

## Avaliação da Sprint 1 e ajustes da Sprint 2 a partir do relatório da Sprint 1

- **Novo `SPRINT1/Relatorio_Avaliacao_Rubrica.md`:** avaliação do relatório do Grupo 6 e dos notebooks da Sprint 1 contra as rubricas da Sprint 1 (98/100; código dos notebooks 95/100), com conferência dos números direto das planilhas, riscos e coerência com a Sprint 2. Principal risco: link do Notebook 2 em branco nas Referências do relatório da Sprint 1.
- **`SPRINT2/Relatorio_Avaliacao_Rubrica.md`:** incluída a atualização da nota da Sprint 2 (97 → 99/100).
- **Capa da Sprint 2 idêntica à da Sprint 1:** mesmas linhas e mesma posição (conferido página a página no PDF): instituição, Escola Politécnica, disciplina, "PROJETO 2: SPRINT 2", "GRUPO 6", os quatro integrantes no formato "Nome - RA: número" e "Novembro, 2026", tudo em Times New Roman 12 negrito, centralizado, espaçamento simples. A folha de rosto (ABNT) segue em Arial e traz os integrantes, o título, a nota de natureza, os professores, Campinas e a data. O RA de Nicollas Tavares da Silva tem 7 dígitos no original e foi mantido; conferir. O curso não consta na capa da Sprint 1 e ficou de fora.
- **Citações e referências da Sprint 2:** passaram a seguir a convenção da Sprint 1 (autoria institucional PUC-Campinas) em vez de "MONTEIRO et al.", com o relatório do Grupo 6 como terceira referência: (GRUPO 6, 2026) e (PONTIFÍCIA UNIVERSIDADE CATÓLICA DE CAMPINAS, 2026a/2026b).
- **Testes:** `test_sprint2_relatorio.py` (capa com Escola Politécnica, Grupo 6 e os RAs) e `test_sprint2_relatorio_abnt.py` (capa idêntica à da Sprint 1, folha de rosto, citações e 3 referências em ordem alfabética) atualizados; 82 testes passam.

## Relatório no padrão ABNT (NBR 14724, 6024, 6028, 6023, 10520)

O `SPRINT2/Relatorio_Sprint2.docx` foi reconstruído (e o `Relatorio_Sprint2.pdf` reexportado pelo Word, 22 páginas) seguindo a ABNT. O conteúdo técnico e os números não mudaram.

- **Página:** A4, margens superior e esquerda 3 cm, inferior e direita 2 cm.
- **Fonte e espaçamento:** Arial 12 em todo o texto; corpo justificado, espaçamento 1,5, recuo de 1,25 cm na primeira linha; legendas, fontes, tabelas e referências em Arial 10 com espaçamento simples; nenhum texto acima de 12 pt.
- **Numeração de página:** só na parte textual, canto superior direito, a 2 cm da borda superior; a contagem começa na folha de rosto (a capa não conta).
- **Elementos pré-textuais:** capa, folha de rosto (com nota de natureza do trabalho e professores), resumo com palavras-chave, lista de figuras, lista de tabelas e sumário, os três últimos como campos do Word (atualizados antes de salvar).
- **Seções (NBR 6024):** numeração arábica progressiva; seção primária em MAIÚSCULAS e negrito, começando em página nova; secundária em MAIÚSCULAS sem negrito; terciária em negrito.
- **Ilustrações e tabelas:** legenda acima ("Figura 1 – …", "Tabela 1 – …", numeração por campo SEQ) e "Fonte:" abaixo; tabelas no modelo IBGE (sem linhas laterais nem verticais); texto alternativo nas figuras.
- **Equações:** centralizadas e numeradas à direita, (1) a (16), com referência no texto.
- **Citações e referências:** citação autor-data (MONTEIRO et al., 2026a e 2026b) e lista de REFERÊNCIAS (as duas orientações das Sprints).
- **Contexto da Sprint 1:** nova seção 1.2 resume a etapa anterior (média 2,51 s e desvio 0,40 s, normalidade, p = 78,85%, 2,17 s e 2,72 s, Planilha 2 com média 5,10 s e 85/100 em até 6 s, critérios de 89% → 0% e 100% → 85% e a conclusão preliminar), tirada dos dois notebooks da Sprint 1.
- **Capa:** Escola Politécnica, Grupo 6 e os quatro integrantes com RA, conforme o relatório da Sprint 1 (instituição e disciplina também conferidas no Obsidian).
- **Testes:** novo `tests/test_sprint2_relatorio_abnt.py` (17 testes: margens, fonte, espaçamento, estilos, ordem dos elementos, legendas, tabelas, equações, citações, referências, contexto da Sprint 1 e ausência de placeholders sem destaque). Os testes consultam os estilos pelo nome, porque o Word regrava os identificadores ao salvar.
- **Geração:** o `.docx` foi gerado por script (biblioteca padrão do Python) fora do repositório e depois atualizado e salvo pelo Word.

## Correções após a avaliação contra a rubrica (`SPRINT2/Relatorio_Avaliacao_Rubrica.md`)

- **z calculado visível nos gráficos (Questões 2b e 3b).** Cada um dos 4 gráficos agora é uma figura com 2 painéis (`plt.subplots(1, 2, ...)`): à esquerda a curva normal padrão de −4 a 4 com as regiões; à direita uma escala ampliada (`set_xlim`, `axvspan`) com a linha azul no z calculado (`axvline(z_media...)` / `axvline(z_prop...)`). O valor do z crítico passou para a legenda (a legenda fica abaixo dos painéis, sem cobrir a curva).
- **Relatório:** as 4 imagens foram trocadas pelas novas figuras (largura do texto, proporção mantida), as legendas das Figuras 1–4 e as frases das seções 5.3 e 6.3 citam a escala ampliada, e as conclusões por nível dizem onde o z calculado aparece.
- **PDF mantido como formato de entrega:** `SPRINT2/Relatorio_Sprint2.pdf`, exportado pelo Word (12 páginas) a partir do `.docx`. Precisa ser exportado de novo depois que a capa for preenchida.
- **Testes:** `test_sprint2_notebook_structure.py` ganhou `test_graphs_mark_the_calculated_z_on_a_full_scale_panel`; `test_sprint2_relatorio.py` ganhou testes das figuras largas, da menção à escala ampliada e da existência do PDF.
- **Ainda pendente:** conferir o RA de Nicollas Tavares da Silva (7 dígitos) e decidir se a capa deve trazer o curso.

## Arquivos

### Novo: `SPRINT2/Notebook_Sprint2_Testes_de_Hipotese.ipynb`
Notebook executado (com saídas), 38 células.
- **Imports:** `pandas`, `numpy`, `math`, `seaborn`, `matplotlib.pyplot`, `from scipy.stats import norm` (numpy e scipy aprovados pelo usuário). Cada import tem um comentário dizendo para que serve (cdf, ppf, pdf etc.).
- **Introdução (código):** conta a Planilha 2 em [0, 6] s (85/100, o intervalo usado na Sprint 1) e em [2, 3] s (0/100, o intervalo corrigido, igual ao da Q5).
- **Questão 1 (código):** `media_pop` = 2,51, `dpad_pop` = 0,40, `p_pop` = 0,7885 (mesmo comando `norm.cdf` da Sprint 1), `media_amostra` = 5,10, `dpad_amostra` = 0,81, `n` = 100, `p_chapeu` = 0. Inclui tabela comparativa.
- **Questão 2a / 3a (código):** `mu_0 = media_pop` e `p_0 = p_pop`, com print de H0 e H1.
- **Questão 2b:** erro-padrão `dpad_pop/math.sqrt(n)` e `z_media`. Por nível: `norm.ppf(1-alfa)`, regiões, decisão por `if` e um gráfico (curva normal padrão, regiões verde/vermelha, linha no z crítico, seta para o z calculado fora da escala).
- **Questão 2c (código):** compara o indício da Q1 com a decisão do teste e imprime "As conclusões coincidem". Calcula também z com o desvio-padrão da amostra (31,98) como verificação de sensibilidade.
- **Questão 3b:** condições n·p0 ≥ 5 e n(1−p0) ≥ 5, erro-padrão `math.sqrt(p_0*(1-p_0)/n)`, `z_prop`, `norm.ppf(alfa)` e 2 gráficos.
- **Questão 3c (código):** compara com a Q1 e mostra o contexto dos 85/100 dentro de 6 s.
- **Síntese:** tabela com o teste, o nível, z calculado, z crítico e a decisão.

### Novo: `SPRINT2/Relatorio_Sprint2.docx` (12 páginas, A4)
- **Capa (versão inicial, já substituída pela capa do Grupo 6 descrita acima):** instituição, título, integrantes (Nome — RA), professores e "Campinas, novembro de 2026".
- **Seções:**
  1. Introdução (situação, problema, intervenção, objetivo)
  2. Pergunta de investigação (por que a pergunta da Sprint 1 não é testável, nova pergunta e correção do intervalo [0, 6] → [2, 3])
  3. Dados e metodologia (população × amostra, fórmulas de média, desvio, p, p̂, z da média com σ/√n, z da proporção com √(p₀(1 − p₀)/n), valores críticos e ferramentas Python)
  4. Resultados antes e depois (Tabela 1 e análise preliminar)
  5. Teste da média (hipóteses, cálculo, Tabela 2, Figuras 1–2 e conclusão por nível)
  6. Teste da proporção (hipóteses, condições, cálculo, Tabela 3, Figuras 3–4 e conclusão por nível)
  7. Comparação com a análise preliminar (as conclusões coincidem; robustez, premissas, significância estatística × prática, contexto do limite de 6 s)
  8. Conclusão
- Os gráficos são os mesmos gerados pelo notebook.
- O documento foi gerado com docx-js e conferido visualmente após exportação para PDF pelo Word.

### Novo: `tests/test_sprint2_notebook_structure.py`
- Ordem das seções, cada uma seguida de código.
- Markdown só com títulos curtos (≤ 400 caracteres, sem "Interpretação breve") e cabeçalho apontando para o relatório.
- Imports e caminhos das planilhas; correção do intervalo em código.
- Comandos dos parâmetros iguais aos da Sprint 1; hipóteses em código (`mu_0`, `p_0`).
- Fórmulas dos erros-padrão, `norm.ppf` e alfas.
- Exatamente 2 gráficos por teste.
- Comparação com a Q1 calculada em código; comentários explicando as fórmulas.
- Execução completa via `nbclient` (≥ 4 imagens, saídas com 64.75, −19.31, 2.326, 1.645 e "coincide").

### Novo: `tests/test_sprint2_relatorio.py`
Lê o `word/document.xml` do .docx e verifica:
- itens da capa;
- ausência do formato "Questão";
- situação, problema, objetivo, intervenção, população e amostra, com os valores;
- pergunta reformulada e correção do intervalo;
- fórmulas (σ/√n, √(p₀(1 − p₀)/n), H₀/H₁);
- z calculados, z críticos e "rejeita", com ≥ 4 menções a "região de rejeição";
- comparação com a análise preliminar ("coincide");
- ≥ 4 imagens embutidas.

### Editado: `tests/test_backend_comments.py`
Incluído o notebook da Sprint 2 na verificação de "comentário antes de cada comando".

### Editado: `README.md`
Incluídos o notebook e o relatório da Sprint 2, o PDF de entrega e os novos módulos no comando de testes.

## Verificação
```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_sprint2_notebook_structure tests.test_sprint2_relatorio tests.test_sprint2_relatorio_abnt tests.test_backend_comments tests.test_notebook_structure tests.test_notebook_2_structure
```
Resultado: 60 testes, OK.

## Pendências do grupo
- Conferir o RA de Nicollas Tavares da Silva (7 dígitos) e decidir se a capa deve trazer o curso; se mudar a capa, exportar o PDF de novo.
- Entregar `SPRINT2/Relatorio_Sprint2.pdf` e o notebook no Canvas.
