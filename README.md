# Projeto-2-Estatistica-E-Analise-de-dados

## Ambiente Python no Windows

Para instalar as dependências do notebook, use CPython 3.12 de 64 bits instalado para Windows. O ambiente `.venv` presente neste checkout foi criado com Python 3.14 do MSYS2 (`mingw_x86_64_ucrt_gnu`); nesse interpretador, `pyzmq` e `psutil` tentam compilar wheels incompatíveis com o ambiente.

No PowerShell, se o `.venv` existente tiver sido criado pelo MSYS2, recrie-o usando o CPython 3.12 padrão do Windows. Nesta máquina, o interpretador está em `$env:LOCALAPPDATA\Programs\Python\Python312\python.exe`:

```powershell
# Execute apenas se o .venv existente tiver sido criado pelo MSYS2.
Remove-Item -LiteralPath .venv -Recurse -Force
$python = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"
& $python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

No PyCharm, selecione `.venv\Scripts\python.exe` como interpretador do projeto. Se o Python estiver instalado em outro local, ajuste `$python` para o caminho completo desse `python.exe`. Não selecione o interpretador em `C:\msys64\...`.

## Executar os notebooks

Situação-problema: a empresa de e-commerce adicionou uma etapa extra de validação antifraude nos pagamentos via Pix. Isso deixa o processamento mais lento, e o grupo investiga se o tempo ainda é aceitável. Variável: `Tempo_processamento_seg` (segundos). Referências: faixa ideal de 2 a 3 segundos e limite tolerável de até 6 segundos.

Abra os notebooks no Jupyter ou no PyCharm com o ambiente configurado acima, nesta ordem:

1. `SPRINT1/Notebook_1_Analise_Antes_Intervencao.ipynb` — Planilha 1 (300 observações, antes da intervenção): Questões 1 a 6.
2. `SPRINT1/Notebook_2_Analise_depois_da_Intervencao.ipynb` — Planilha 2 (100 observações, depois da intervenção): Questões 7.1 a 7.4 e a comparação com a Planilha 1 na Questão 8.

Os caminhos das planilhas são relativos aos notebooks e apontam para `Refs/` na raiz do projeto.

## Testes

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_notebook_structure tests.test_notebook_2_structure tests.test_backend_comments -v
```
