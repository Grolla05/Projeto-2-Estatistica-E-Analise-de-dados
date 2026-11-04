import ast
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "SPRINT1" / "Notebook_1_Analise_Antes_Intervencao.ipynb"


class BackendCommentTests(unittest.TestCase):
    def test_backend_cells_explain_each_top_level_command(self):
        notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
        backend_cell_indexes = {
            2, 4, 6, 8, 16, 18, 20, 23, 25, 27, 29, 31, 34, 37, 41, 44, 53, 55,
            57, 59, 63,
        }

        for index in backend_cell_indexes:
            with self.subTest(cell=index):
                cell = notebook["cells"][index]
                source = "".join(cell["source"])
                comments = [line for line in source.splitlines() if line.lstrip().startswith("#")]
                statements = ast.parse(source).body
                self.assertGreaterEqual(
                    len(comments),
                    len(statements),
                    f"A célula {index} precisa explicar cada comando de backend.",
                )
                for statement in statements:
                    preceding_lines = source.splitlines()[: statement.lineno - 1]
                    self.assertTrue(
                        any(line.lstrip().startswith("#") for line in preceding_lines),
                        f"O comando da linha {statement.lineno} na célula {index} não tem explicação.",
                    )


if __name__ == "__main__":
    unittest.main()
