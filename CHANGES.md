# CHANGES

## 2026-11-04 — Corrigir execução do Notebook 1 e avaliar contra a rubrica

- **Erro corrigido:** `ImportError: Import openpyxl failed` em `pd.read_excel` (célula 3). O `.venv` não tinha `openpyxl`; instalado `requirements.txt` no `.venv` (inclui `openpyxl 3.1.5`, `nbclient`, `nbconvert`).
- Histograma da Planilha 1 (seção 4.1 "com a curva normal") passou a sobrepor a curva normal teórica N(média, DP), calculada com `math.exp` e escalada pela largura da classe, com legenda.
- Contagens de ±1/±2/±3 desvios-padrão convertidas com `int()` e impressas com rótulo (antes exibiam `np.int64(...)`); as três porcentagens foram unificadas numa célula com a referência da regra empírica (68 / 95 / 99,7%). Removidas as duas células avulsas de porcentagem.
- `limite_objetivo_segundos = 3.0` movido da Q7.4 para a célula da Q8, onde é usado.
- Q8: tabela comparativa ganhou a linha de desvio-padrão; aviso de causalidade deixou de ser impresso em duplicidade.
- Notebook reexecutado com `jupyter nbconvert --execute --inplace`; saídas e gráficos atuais gravados no `.ipynb` (a saída de erro antiga foi substituída).
- Testes novos em `tests/test_notebook_structure.py`: dependência `openpyxl`, curva normal no histograma, contagens/porcentagens impressas, local do limite do objetivo, aviso de causalidade único e execução completa do notebook via `nbclient` sem erros. Resultado: **21 testes OK**.
- Avaliação critério a critério contra a rubrica (relatório não versionado): **6,40 / 10 (64 / 100)** na rubrica completa; **92 / 100** nos critérios que dependem só de código. Pendências principais: Q1 e Q7.1 sem texto, intervalo [2, 3] s sem justificativa, PDF final não gerado.
- Nenhum commit, push ou pull request foi feito; aguardando validação do usuário.

## 2026-11-04 — Corrigir ambiente de execução e registrar interpretações

- Diagnóstico do erro de instalação: o `.venv` anterior usava Python 3.14 do MSYS2 com plataforma `mingw_x86_64_ucrt_gnu`. `psutil` e `pyzmq` tentavam compilar wheels nativas nesse alvo e a configuração CMake do `pyzmq` falhava. A captura não mostra a linha CMake mais específica, então a causa identificada é a incompatibilidade do interpretador/ABI escolhido para esse fluxo de instalação.
- O `.venv` antigo continha somente `pip`; foi substituído por um ambiente CPython 3.12 do Windows (`win-amd64`). Foi necessário criar o ambiente sem o `ensurepip` embutido, devido à restrição de gravação no diretório temporário do sandbox, e reutilizar os pacotes disponíveis no Python 3.12 local (`--system-site-packages`). O executável `pip.exe` local foi então instalado a partir do wheel embutido no próprio CPython. A checagem `pip install --no-index -r requirements.txt` confirmou todas as dependências, incluindo `psutil` e `pyzmq`, sem compilação.
- Atualizado `README.md` com a causa do erro e instruções para selecionar o CPython 3.12, recriar o ambiente e apontar o PyCharm para `.venv\\Scripts\\python.exe`.
- Substituídos os sete placeholders de interpretação no notebook por conclusões curtas calculadas a partir das duas planilhas. A Questão 4 registra a proximidade com a regra empírica, a simetria aproximada dos quartis e a leitura conjunta do Q-Q; as Questões 5 e 6 contextualizam a probabilidade e os percentis; a 7.4 registra a pergunta e a contagem; e a 8 compara critérios e explicita que os resultados não provam causalidade.
- Resultados usados nas interpretações: Planilha 1 (300 observações), média 2,5112 s, mediana 2,51 s, desvio-padrão amostral 0,4003 s; proporções em ±1/±2/±3 desvios-padrão: 68%, 96%, 100%; metades interquartis: 0,28 s e 0,2625 s; probabilidade normal estimada em [2, 3] s: 78,8127%; percentis: 2,1743 s e 2,7212 s. Planilha 2 (100 observações), média 5,0979 s, mediana 5,125 s, desvio-padrão 0,8102 s; contagem em [2, 3] s: 0; até 3 s: 89% antes e 0% depois; em [2, 3] s: 79,33% antes e 0% depois; diferença de médias depois menos antes: +2,5867 s.
- A execução sequencial em memória de todas as células de código terminou sem exceções e forneceu os resultados acima. A tentativa de iniciar um kernel Jupyter pelo `nbclient` não completou o handshake neste ambiente de execução, por isso as saídas não foram incorporadas ao `.ipynb`.
- Incluídos testes para verificar as interpretações baseadas nos resultados e a orientação de ambiente no README. Resultado final: `python -m unittest discover -s tests -p test_notebook_structure.py -v` — **15 testes passaram**.
- Nenhum commit, push ou pull request foi feito; aguardando validação do usuário.

## 2026-11-04 — Campos breves de interpretação no Notebook 1

- Adicionadas células Markdown imediatamente após os resultados que, conforme a rubrica, exigem análise ou contextualização.
- Na Questão 4, os campos orientam uma conclusão breve sobre: histograma e regra empírica; simetria pelas distâncias entre quartis; e diagrama Q-Q com conclusão conjunta de normalidade.
- Na Questão 5, o campo solicita interpretar a probabilidade para o intervalo selecionado.
- Na Questão 6, o campo solicita contextualizar, em segundos, os limites dos 20% menores e dos 30% maiores.
- Na Questão 7.4, o campo pede a pergunta associada ao intervalo e uma leitura breve da contagem em relação ao objetivo.
- Na Questão 8, o campo pede uma conclusão comparativa curta com base nos dois critérios e na direção observada, mantendo explícito o caráter descritivo.
- Na versão inicial, os campos eram placeholders editáveis; foram preenchidos com conclusões baseadas nos dados na atualização registrada no topo deste arquivo. O relatório continua reservado para o desenvolvimento completo. Não foram adicionados campos após gráficos e estatísticas descritivas que a rubrica não solicita interpretar.
- Adicionado teste estrutural em `tests/test_notebook_structure.py` para verificar a presença de um campo Markdown imediatamente após cada resultado interpretativo relevante.
- Validação: `python -m unittest discover -s tests -p test_notebook_structure.py -v` — **13 testes passaram**.
- Nenhum commit, push ou pull request foi feito; aguardando validação do usuário.

## 2026-11-04 — Completar análise da Sprint 1 e corrigir referências das planilhas

### Configuração do repositório e ambiente

- Criado `.gitignore` para caches Python, ambientes virtuais, checkpoints do Jupyter, caches de ferramentas, arquivos locais de IDE e arquivos comuns do sistema operacional.
- Criado `.editorconfig` para padronizar a edição dos arquivos do projeto.
- Criado `requirements.txt` com pandas, matplotlib, seaborn, openpyxl, Jupyter e ipykernel. `openpyxl` é o mecanismo usado pelo pandas para abrir os arquivos Excel.
- O repositório já estava inicializado e o remoto `origin` já estava configurado; nenhuma identidade, remoto ou configuração local de Git foi alterada.

### Notebook 1 e referências aos dados

- Reestruturado `SPRINT1/Notebook_1_Analise_Antes_Intervencao.ipynb` para manter a sequência didática do tutorial `SPRINT1/refs/Python - Distribuição Normal-1-1.pdf`, com uma célula separada para imports, definição de variáveis e leitura dos dados.
- Corrigidos os caminhos e o mapeamento das planilhas renomeadas:
  - `../Refs/Planilha 1 - TEMPO PAGAMENTO PIX.xlsx` → dados de antes, 300 observações.
  - `../Refs/Planilha 2 -TEMPO PAGAMENTO PIX-2.xlsx` → dados de depois, 100 observações.
- O notebook valida a quantidade esperada de linhas e a presença da coluna `Tempo_processamento_seg`; eliminada a antiga mensagem de divergência de tamanho.
- Desenvolvidas as seções correspondentes às Questões 1 a 8 da rubrica: espaço de contextualização manual; gráficos e estatísticas descritivas antes; regra empírica, quartis e Q-Q; probabilidade normal e percentis; espaços para registrar contexto/intervenção manualmente; gráficos e estatísticas depois; contagem no intervalo; e comparação dos critérios entre as amostras.
- Gráficos usam seaborn e matplotlib; o cálculo da CDF/quantis da normal usa `math`, sem incluir bibliotecas novas no código do notebook. O quadro comparativo é impresso com pandas.
- Intervalo de 2 a 3 segundos e objetivo de até 3 segundos estão identificados no notebook como valores provisórios, que precisam de justificativa do grupo no relatório manuscrito. Nenhum SLA ou critério oficial foi fornecido nos arquivos.
- A comparação descreve os dados observados e explicita que não demonstra causalidade. A redação informa a direção da diferença de médias.

### Resultado da execução com as planilhas atuais

- Execução sequencial em memória das células de código concluída sem exceções.
- Antes: 300 registros, média de 2,5112 s; 89% atendem ao critério provisório de até 3 s.
- Depois: 100 registros, média de 5,0979 s; 0% atendem ao critério provisório de até 3 s; 0 registros estão entre 2 e 3 s.
- A diferença observada entre as médias é de aproximadamente +2,5867 s (depois menos antes). Isso deve ser discutido no relatório sem atribuir causa à intervenção sem evidência adicional.
- As saídas de execução não foram gravadas dentro do `.ipynb`; as células executadas continuam sem outputs salvos. A execução de validação foi feita em memória.

### Testes e validação

- Atualizado `tests/test_notebook_structure.py`, incluindo verificações de formato e sintaxe do notebook, ordem/separação das células, imports permitidos, referências corretas, tamanhos reais das amostras, cobertura das questões, limiares provisórios, direção da comparação e cálculo dos quantis.
- Executado `python -m unittest discover -s tests -p test_notebook_structure.py -v`: **12 testes passaram**.
- Todas as células de código foram executadas em sequência com as planilhas atuais; a execução terminou sem exceções e confirmou 300/100 linhas e os resultados acima.
- Nenhum commit, push ou pull request foi feito. Aguardando validação e comando do usuário, conforme o fluxo do projeto.


## 2026-11-04 ? Coment?rios explicativos no backend do notebook

- Acrescentados coment?rios em portugu?s ?s etapas de leitura dos dados, aos c?lculos estat?sticos e ?s fun??es auxiliares de distribui??o normal, explicando o que cada comando faz e por que ? usado.
- Mantidas sem explica??o linha a linha as c?lulas de constru??o de gr?ficos e tabela, conforme solicitado.
- Adicionado `tests/test_backend_comments.py` para verificar coment?rios nas c?lulas de backend selecionadas.
- Valida??o: teste de coment?rios, sintaxe das c?lulas e execu??o integral do notebook conclu?dos com sucesso. A su?te estrutural completa ainda aponta verifica??es preexistentes de r?tulos/justificativas textuais que n?o correspondem ao conte?do atual.
