# Avaliação da Sprint 2 versus a rubrica — Projeto 2 (Estatística e Análise de Dados)

Data da avaliação: 26/11/2026
Material avaliado: `SPRINT2/Notebook_Sprint2_Testes_de_Hipotese.ipynb`, `SPRINT2/Relatorio_Sprint2.docx`, `tests/test_sprint2_*.py`
Critérios: `SPRINT2/refs/rubrica_avaliacao_1.png`, `rubrica_avaliacao_2.png`, `image.png` (avisos da atividade) e `ORIENTAÇÕES SPRINT 2 - PROJETO 2-3.pdf`.

> **Atualização (26/11/2026, depois das correções):** a nota passou de **97** para **99/100** (9,95). O z calculado agora aparece nos 4 gráficos (+0,10), a capa foi preenchida com Escola Politécnica, Grupo 6 e os 4 integrantes com RA, copiados do relatório da Sprint 1 (+0,10), e o PDF foi exportado (+0,05). Falta só o item "Curso" da capa (−0,05); a Sprint 1 também não trazia o curso. A tabela abaixo é a avaliação original, mantida como histórico.

## 1. Nota final

| Situação | Nota (0–10) | Nota (0–100) |
|---|---|---|
| **Como está hoje** (capa com campos vazios, arquivo em .docx) | **9,70** | **97** |
| Depois de preencher a capa e exportar o PDF | 9,95 a 10,00 | 99 a 100 |

A conta é direta: a rubrica soma 10 pontos, então cada ponto vale 10 na escala de 0 a 100.

## 2. Pontuação por critério

| Critério da rubrica | Máx. | Nota | Justificativa |
|---|---|---|---|
| Notebook com gráficos (pré-requisito) | 0 | Atendido | 4 gráficos: média × (1%, 5%) e proporção × (1%, 5%). Notebook executa do início ao fim sem erro. |
| Introdução (pergunta adequada) | 0 | Atendido | A pergunta da Sprint 1 era composta e sem valor de referência. Foi reformulada com sentido (aumento da média, redução da proporção) e valor de comparação (2,51 s e 78,85%). |
| Questão 1 — síntese e comparação | 1,50 | **1,50** | Situação, problema, objetivo e intervenção (seção 1). Parâmetros da população e da amostra (Tabela 1). Comparação com os indícios preliminares (seção 4). |
| Questão 2a — hipóteses da média | 1,00 | **1,00** | H0: μ = 2,51 e H1: μ > 2,51, unilateral à direita, coerente com a pergunta. |
| Questão 2b — teste da média | 1,50 | **1,45** | Regiões de rejeição e não rejeição para 1% e 5%, z = 64,75, decisão e conclusão contextualizada em cada nível. Desconto de 0,05 porque o z calculado não aparece plotado na curva, só uma seta fora da escala (ver 4.2). |
| Questão 2c — comparação com a Q1 | 1,25 | **1,25** | Retoma a Q1, afirma que as conclusões coincidem e discute robustez (z = 31,98 com o desvio da amostra), premissas e significância estatística × prática. |
| Questão 3a — hipóteses da proporção | 1,00 | **1,00** | H0: p = 0,7885 e H1: p < 0,7885, unilateral à esquerda. |
| Questão 3b — teste da proporção | 1,50 | **1,45** | Condições n·p₀ e n(1−p₀) ≥ 5, erro-padrão com p₀, z = −19,31, valores críticos −2,326 e −1,645, decisão por nível. Mesmo desconto da 2b. |
| Questão 3c — comparação com a Q1 | 1,25 | **1,25** | Compara com a Q1, explica por que p̂ = 0 é extremo e contextualiza os 85/100 dentro de 6 s. |
| Qualidade de entrega | 1,00 | **0,80** | Texto estruturado, sem formato de "respostas às questões", 12 páginas, 4 figuras e 3 tabelas. Perde pontos: capa com 3 dos 5 itens ainda em branco (−0,15) e entrega prevista em PDF, que ainda não foi exportado (−0,05 de formatação). |
| **Total** | **10,00** | **9,70** | |

## 3. Conferência dos números (recalculados direto das planilhas)

| Valor | No relatório | Recalculado | Status |
|---|---|---|---|
| n da Planilha 1 / Planilha 2 | 300 / 100 | 300 / 100 | ok |
| Média e desvio da Planilha 1 | 2,51 / 0,40 | 2,5112 / 0,4003 | ok |
| Média e desvio da Planilha 2 | 5,10 / 0,81 | 5,0979 / 0,8102 | ok |
| p (probabilidade em [2, 3] s) | 0,7885 | 0,7881 sem arredondar | ok, 0,7885 vem do mesmo comando e arredondamento da Sprint 1 |
| p̂ em [2, 3] s | 0/100 | 0 (mínimo da amostra é 3,01 s) | ok |
| Transações até 6 s | 85/100 | 85 | ok |
| z da média | 64,75 | 64,61 sem arredondar | ok, diferença só do arredondamento de x̄ e σ |
| z da proporção | −19,31 | −19,308 | ok |
| Valores críticos | ±2,326 / ±1,645 | idem | ok |

Decisões corretas nos 4 casos (rejeita H0). Nenhuma conclusão muda com o arredondamento.

## 4. Análise do código (versus rubrica e AGENTS.md)

Nota do código: **94/100**.

### 4.1 Pontos fortes
- Sequência fiel à rubrica: leitura, parâmetros (Q1), hipóteses (a), teste por nível (b), comparação (c).
- Fórmulas corretas: `dpad_pop/math.sqrt(n)` para a média, `math.sqrt(p_0*(1-p_0)/n)` para a proporção, `norm.ppf(1-alfa)` à direita e `norm.ppf(alfa)` à esquerda.
- Hipóteses definidas em código (`mu_0`, `p_0`) a partir dos parâmetros da Planilha 1, sem número digitado à mão.
- Cada comando tem comentário explicativo, seguindo o padrão do repositório de referência.
- Parâmetros reaproveitam exatamente os comandos da Sprint 1, então os valores batem com a entrega anterior.
- Correção do intervalo ([0, 6] → [2, 3]) feita e explicada em código, como as orientações pediam.
- Verificação de sensibilidade (z com o desvio da amostra) dá base real à discussão da 2c.
- Testes: 60 testes passam (rodei `test_sprint2_notebook_structure`, `test_sprint2_relatorio`, `test_backend_comments`, `test_notebook_structure`, `test_notebook_2_structure`, 25 s).

### 4.2 Problemas e riscos, do mais grave ao menor

1. **Capa com campos vazios (impacto: −0,15 ponto).** Escola, Curso, nomes e RAs estão como `[Nome da Escola]`, `[00000000]` etc. (12 trechos em amarelo). Rubrica dá 0,05 por item da capa.
2. **Entrega em .docx, rubrica pede PDF (impacto: ~0,05 e risco de formatação).** Exportar o Word para PDF e conferir a paginação das figuras antes de enviar.
3. **z calculado não aparece sobre a curva (impacto: −0,10 no total das duas questões).** Com z = 64,75 e −19,31 é impossível plotar no eixo de −4 a 4. A seta "fora da escala" é razoável, mas um corretor que espera ver a marca pode descontar. Opção: ampliar o eixo (ex.: −5 a 70 em um segundo gráfico) ou escrever o valor em destaque no título.
4. **`p̂ = 0` torna o teste da proporção trivial.** Todas as 100 transações da Planilha 2 estão em [3,01; 6,87], logo nenhuma cai em [2, 3]. A decisão é correta, mas a 3c "coincide" fica óbvia. O relatório já explica o extremo, o que mitiga. Vale conferir a correção da Sprint 1 para confirmar que o grupo quer manter [2, 3] e não, por exemplo, outro intervalo de interesse.
5. **Nome da instituição não verificado.** A capa diz "Pontifícia Universidade Católica de Campinas". Não achei essa informação em nenhum arquivo de referência (as orientações só citam os professores). Confirmar se está correta.
6. **Bibliotecas fora da lista do AGENTS.md.** O `AGENTS.md` só autoriza `pandas`, `math`, `seaborn`, `matplotlib`; a exceção documentada de `numpy` e `scipy.stats.norm` é da SPRINT1. O CHANGES.md diz que a aprovação vale para a Sprint 2, mas o `AGENTS.md` não registra isso. Sugestão: acrescentar uma linha de exceção para a SPRINT2.
7. **`seaborn` importado e não usado** no notebook (`sns` não aparece em nenhuma célula). Não afeta o resultado. Ou remover, ou usar `sns` nos gráficos para manter o padrão da Sprint 1.
8. **Código repetido.** Os blocos de gráfico (4×) e de decisão (4×) são cópias com poucas trocas. Aceitável em notebook didático, mas uma função como `desenhar_regioes(z_critico, z_calc, lado)` reduziria erro de edição. Só mudaria se o grupo quiser; a rubrica não exige.
9. **Tabela de síntese com textos fixos** (`"Média (H1: μ > 2,51 s)"`, `"Proporção ... 0,7885"`). Se os dados mudarem, a tabela não acompanha. Ideal: montar com f-strings a partir de `mu_0` e `p_0`.
10. **Caminho relativo** `../Refs/...` exige que o kernel rode a partir de `SPRINT2/`. Funciona no teste automático e no VS Code/Jupyter padrão, mas falha se o notebook for aberto de outra pasta.

## 5. O que não consegui verificar
- **Aparência do documento Word e dos gráficos.** Li o texto do `.docx` e conferi que há 4 imagens embutidas, mas não renderizei as páginas nem os gráficos. O CHANGES.md afirma que o grupo conferiu a exportação para PDF no Word.
- **Contexto do Obsidian.** A rotina pedida no `CLAUDE.md` global falhou: o `obsidian_simple_search` deu timeout (127.0.0.1:27124, leitura de 6 s). Nenhuma nota do vault foi consultada.
- **Correção da Sprint 1 pelo professor.** Não há feedback oficial no repositório, então o desconto possível por erro herdado da Sprint 1 não está considerado.

## 6. Ações para chegar a 10/10
1. Preencher escola, curso, nomes, RAs na capa e remover o destaque amarelo (+0,15).
2. Exportar para PDF e revisar a paginação (+0,05).
3. Marcar o z calculado de forma mais visível nos gráficos (até +0,10).
4. Confirmar o nome da instituição.
5. Opcional: remover `seaborn` não usado, registrar a exceção de `numpy`/`scipy` da SPRINT2 no `AGENTS.md` e parametrizar a tabela de síntese.

📎 Notas do Obsidian consultadas: nenhuma (servidor MCP indisponível por timeout).
