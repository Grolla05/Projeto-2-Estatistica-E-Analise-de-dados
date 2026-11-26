"""Testes do notebook da Sprint 2 — testes de hipótese da média e da proporção.

O notebook concentra o código e a explicação do código (comentários). Os
textos de análise (situação, conclusões, discussão) ficam no relatório Word
`SPRINT2/Relatorio_Sprint2.docx`, testado em `test_sprint2_relatorio.py`.
"""

import ast
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "SPRINT2" / "Notebook_Sprint2_Testes_de_Hipotese.ipynb"

EXPECTED_IMPORTS = {"pandas", "numpy", "math", "seaborn", "matplotlib.pyplot"}
MAX_MARKDOWN_CHARS = 400


class Sprint2StructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
        cls.cells = [
            {
                **cell,
                "source": "".join(cell["source"])
                if isinstance(cell["source"], list)
                else cell["source"],
            }
            for cell in cls.notebook["cells"]
        ]
        cls.markdown_cells = [c["source"] for c in cls.cells if c["cell_type"] == "markdown"]
        cls.all_code = "\n".join(
            cell["source"] for cell in cls.cells if cell["cell_type"] == "code"
        )

    def find_markdown(self, text):
        for index, cell in enumerate(self.cells):
            if cell["cell_type"] == "markdown" and text in cell["source"]:
                return index
        self.fail(f"Cabeçalho Markdown ausente: {text}")

    def following_code(self, markdown_index):
        for cell in self.cells[markdown_index + 1 :]:
            if cell["cell_type"] == "code":
                return cell["source"]
            if cell["cell_type"] == "markdown":
                break
        self.fail(f"Não há célula de código após a célula Markdown {markdown_index}.")

    def section_code(self, start_marker, end_marker):
        start = self.find_markdown(start_marker)
        end = self.find_markdown(end_marker)
        return "\n".join(
            cell["source"] for cell in self.cells[start:end] if cell["cell_type"] == "code"
        )

    def test_notebook_is_valid_and_code_cells_parse(self):
        self.assertEqual(self.notebook["nbformat"], 4)
        for cell in self.cells:
            if cell["cell_type"] == "code":
                ast.parse(cell["source"])

    def test_sections_are_in_order_and_each_has_code(self):
        steps = [
            "1. Importar as bibliotecas",
            "2. Definir as variáveis",
            "3. Leitura dos arquivos de dados",
            "## Introdução",
            "## Questão 1",
            "## Questão 2a",
            "## Questão 2b",
            "## Questão 2c",
            "## Questão 3a",
            "## Questão 3b",
            "## Questão 3c",
        ]
        positions = [self.find_markdown(step) for step in steps]
        self.assertEqual(positions, sorted(positions))
        for index in positions:
            with self.subTest(section=self.cells[index]["source"].splitlines()[0]):
                self.assertEqual(self.cells[index + 1]["cell_type"], "code")

    def test_markdown_is_only_short_titles(self):
        for text in self.markdown_cells:
            with self.subTest(markdown=text[:60]):
                self.assertLessEqual(len(text), MAX_MARKDOWN_CHARS)
                self.assertNotIn("Interpretação breve", text)

    def test_notebook_points_to_the_report(self):
        self.assertIn("Relatorio_Sprint2.docx", self.markdown_cells[0])

    def test_imports(self):
        source = self.following_code(self.find_markdown("1. Importar as bibliotecas"))
        tree = ast.parse(source)
        self.assertTrue(all(isinstance(node, (ast.Import, ast.ImportFrom)) for node in tree.body))
        imported = {
            alias.name
            for node in tree.body
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        self.assertEqual(imported, EXPECTED_IMPORTS)
        self.assertIn("from scipy.stats import norm", source)

    def test_both_spreadsheets_are_read(self):
        setup = self.following_code(self.find_markdown("2. Definir as variáveis"))
        self.assertIn('arquivo_antes = "../Refs/Planilha 1 - TEMPO PAGAMENTO PIX.xlsx"', setup)
        self.assertIn('arquivo_depois = "../Refs/Planilha 2 -TEMPO PAGAMENTO PIX-2.xlsx"', setup)
        self.assertIn('coluna = "Tempo_processamento_seg"', setup)
        read = self.following_code(self.find_markdown("3. Leitura dos arquivos de dados"))
        self.assertIn("df_antes=pd.read_excel(arquivo_antes)", read)
        self.assertIn("df_depois=pd.read_excel(arquivo_depois)", read)

    def test_introduction_code_shows_interval_correction(self):
        intro = self.following_code(self.find_markdown("## Introdução"))
        self.assertIn("i>=0 and i<=6", intro)
        self.assertIn("i>=2 and i<=3", intro)

    def test_parameters_use_the_same_commands_as_sprint_1(self):
        self.assertIn("media_pop = round(df_antes[coluna].mean(), 2)", self.all_code)
        self.assertIn("dpad_pop = round(df_antes[coluna].std(), 2)", self.all_code)
        self.assertIn(
            "p_pop = norm.cdf(3,loc=media_pop,scale=dpad_pop).round(4)-norm.cdf(2,loc=media_pop,scale=dpad_pop).round(4)",
            self.all_code,
        )
        self.assertIn("media_amostra = round(df_depois[coluna].mean(), 2)", self.all_code)
        self.assertIn("p_chapeu", self.all_code)

    def test_hypotheses_are_declared_in_code(self):
        mean_h = self.following_code(self.find_markdown("## Questão 2a"))
        self.assertIn("mu_0 = media_pop", mean_h)
        self.assertIn("H0", mean_h)
        self.assertIn("H1", mean_h)
        prop_h = self.following_code(self.find_markdown("## Questão 3a"))
        self.assertIn("p_0 = p_pop", prop_h)
        self.assertIn("H0", prop_h)
        self.assertIn("H1", prop_h)

    def test_test_statistics_and_critical_values(self):
        self.assertIn("erro_padrao_media = dpad_pop/math.sqrt(n)", self.all_code)
        self.assertIn("erro_padrao_prop = math.sqrt(p_0*(1-p_0)/n)", self.all_code)
        self.assertIn("norm.ppf(1-alfa", self.all_code)
        self.assertIn("norm.ppf(alfa", self.all_code)
        self.assertIn("alfa = 0.01", self.all_code)
        self.assertIn("alfa = 0.05", self.all_code)

    def test_four_rejection_region_graphs(self):
        for start, end in [("## Questão 2b", "## Questão 2c"), ("## Questão 3b", "## Questão 3c")]:
            code = self.section_code(start, end)
            with self.subTest(section=start):
                self.assertEqual(code.count("plt.show()"), 2)
                self.assertEqual(code.count("fill_between"), 4)
                self.assertGreaterEqual(code.count("axvline"), 2)
                self.assertGreaterEqual(code.count("annotate"), 2)

    def test_graphs_mark_the_calculated_z_on_a_full_scale_panel(self):
        # Rubrica 2b/3b: "indica o valor calculado de z". Como |z| fica muito além de 4,
        # cada gráfico tem um segundo painel com escala ampliada que contém o z calculado.
        for start, end, z_name in [
            ("## Questão 2b", "## Questão 2c", "z_media"),
            ("## Questão 3b", "## Questão 3c", "z_prop"),
        ]:
            code = self.section_code(start, end)
            with self.subTest(section=start):
                self.assertEqual(code.count("plt.subplots(1, 2"), 2)
                self.assertEqual(code.count("suptitle("), 2)
                self.assertGreaterEqual(code.count("set_title("), 4)
                self.assertGreaterEqual(code.count("axvspan"), 4)
                self.assertEqual(code.count(f"axvline({z_name}"), 2)
                self.assertGreaterEqual(code.count("set_xlim("), 2)

    def test_comparison_with_question_1_is_computed(self):
        for marker in ["## Questão 2c", "## Questão 3c"]:
            with self.subTest(marker=marker):
                code = self.following_code(self.find_markdown(marker))
                self.assertIn("if ", code)
                self.assertIn("coincide", code)

    def test_code_comments_explain_formulas(self):
        for expected in ["# Fórmula", "sigma / raiz(n)", "raiz(p0 * (1 - p0) / n)"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.all_code)

    def test_no_handmade_functions(self):
        self.assertNotIn("def ", self.all_code)
        self.assertNotIn("math.exp", self.all_code)


class Sprint2ExecutionTests(unittest.TestCase):
    def test_notebook_runs_and_produces_four_plus_figures(self):
        import nbformat
        from nbclient import NotebookClient

        notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
        client = NotebookClient(
            notebook,
            timeout=300,
            resources={"metadata": {"path": str(NOTEBOOK_PATH.parent)}},
        )
        client.execute()
        outputs = [
            output
            for cell in notebook.cells
            if cell.cell_type == "code"
            for output in cell.get("outputs", [])
        ]
        errors = [output for output in outputs if output.get("output_type") == "error"]
        self.assertEqual(errors, [])
        images = [output for output in outputs if "image/png" in output.get("data", {})]
        self.assertGreaterEqual(len(images), 4)
        text = "\n".join(
            "".join(output.get("text", "")) for output in outputs if output.get("output_type") == "stream"
        )
        for expected in ["64.75", "-19.31", "2.326", "1.645", "coincide"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, text)


if __name__ == "__main__":
    unittest.main()
