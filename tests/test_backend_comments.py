"""Garante que cada comando de backend dos notebooks tenha uma explicação.

Para toda célula de código, cada comando de nível superior precisa ser
precedido imediatamente (ignorando linhas em branco) por um comentário.
"""

import ast
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATHS = [
    ROOT / "SPRINT1" / "Notebook_1_Analise_Antes_Intervencao.ipynb",
    ROOT / "SPRINT1" / "Notebook_2_Analise_depois_da_Intervencao.ipynb",
]


class BackendCommentTests(unittest.TestCase):
    def test_backend_cells_explain_each_top_level_command(self):
        for path in NOTEBOOK_PATHS:
            notebook = json.loads(path.read_text(encoding="utf-8"))
            for index, cell in enumerate(notebook["cells"]):
                if cell["cell_type"] != "code":
                    continue
                source = "".join(cell["source"])
                lines = source.splitlines()
                for statement in ast.parse(source).body:
                    with self.subTest(notebook=path.name, cell=index, line=statement.lineno):
                        previous = [
                            line.strip()
                            for line in lines[: statement.lineno - 1]
                            if line.strip()
                        ]
                        self.assertTrue(
                            previous and previous[-1].startswith("#"),
                            f"{path.name}, célula {index}: o comando da linha "
                            f"{statement.lineno} não tem comentário explicativo logo acima.",
                        )


if __name__ == "__main__":
    unittest.main()
