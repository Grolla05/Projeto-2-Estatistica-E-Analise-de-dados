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

## Executar o notebook

Abra `SPRINT1/Notebook_1_Analise_Antes_Intervencao.ipynb` no Jupyter ou no PyCharm com o ambiente configurado acima. Os caminhos das planilhas são relativos ao notebook e apontam para `Refs/` na raiz do projeto.
