"""Testes do Notebook 2 — análise da Planilha 2 (depois da intervenção).

O Notebook 2 contém as Questões 7.1 a 7.4 (Planilha 2) e a Questão 8, que
compara a Planilha 2 com a Planilha 1, usando os comandos do material
"Python - Distribuição Normal".
"""

import ast
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "SPRINT1" / "Notebook_2_Analise_depois_da_Intervencao.ipynb"

PDF_IMPORTS = {"pandas", "numpy", "math", "seaborn", "matplotlib.pyplot", "statsmodels.api", "pylab"}


class Notebook2StructureTests(unittest.TestCase):
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
        cls.all_markdown = "\n".join(
            cell["source"] for cell in cls.cells if cell["cell_type"] == "markdown"
        )
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

    def code_index(self, marker):
        return next(
            index
            for index, cell in enumerate(self.cells)
            if cell["cell_type"] == "code" and marker in cell["source"]
        )

    def code_with(self, marker):
        return self.cells[self.code_index(marker)]["source"]

    def test_notebook_is_valid_and_code_cells_parse(self):
        self.assertEqual(self.notebook["nbformat"], 4)
        for cell in self.cells:
            if cell["cell_type"] == "code":
                ast.parse(cell["source"])

    def test_sections_are_in_order(self):
        steps = [
            "1. Importar as bibliotecas",
            "2. Definir as variáveis",
            "3. Leitura do arquivo de dados",
            "## Questão 7.1",
            "## Questão 7.2",
            "## Questão 7.3",
            "## Questão 7.4",
            "## Questão 8",
        ]
        positions = [self.find_markdown(step) for step in steps]
        self.assertEqual(positions, sorted(positions))
        for index in positions[:3]:
            self.assertEqual(self.cells[index + 1]["cell_type"], "code")

    def test_imports_match_the_pdf(self):
        source = self.following_code(self.find_markdown("1. Importar as bibliotecas"))
        tree = ast.parse(source)
        self.assertTrue(all(isinstance(node, (ast.Import, ast.ImportFrom)) for node in tree.body))
        imported = {
            alias.name
            for node in tree.body
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        self.assertEqual(imported, PDF_IMPORTS)
        self.assertIn("from scipy.stats import norm", source)

    def test_spreadsheet_2_is_the_main_data_source(self):
        setup = self.following_code(self.find_markdown("2. Definir as variáveis"))
        self.assertIn('arquivo = "../Refs/Planilha 2 -TEMPO PAGAMENTO PIX-2.xlsx"', setup)
        self.assertIn('coluna = "Tempo_processamento_seg"', setup)
        self.assertNotIn("read_excel", setup)

        read = self.following_code(self.find_markdown("3. Leitura do arquivo de dados"))
        self.assertIn("df=pd.read_excel(arquivo)", read)

    def test_spreadsheet_1_is_only_read_for_the_comparison(self):
        question_8_index = self.find_markdown("## Questão 8")
        self.assertGreater(self.code_index("df_antes"), question_8_index)
        self.assertIn(
            'arquivo_antes = "../Refs/Planilha 1 - TEMPO PAGAMENTO PIX.xlsx"', self.all_code
        )
        self.assertIn("df_antes=pd.read_excel(arquivo_antes)", self.all_code)

    def test_question_7_1_describes_situation_action_and_goal(self):
        section = self.cells[self.find_markdown("## Questão 7.1")]["source"]
        lowered = section.lower()
        for expected in ["situação", "ação", "objetivo", "antifraude", "6 segundos"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, lowered)
        self.assertIn("?", section)
        self.assertNotIn("[", section)

    def test_question_7_2_graphs_use_pdf_commands_with_titles_and_units(self):
        histogram = self.code_with("sns.histplot(data=df[coluna],kde=True)")
        self.assertIn("plt.title(", histogram)
        self.assertIn("segundos", histogram)
        self.assertIn("plt.show()", histogram)

        boxplot = self.code_with("sns.boxplot(data=df[coluna])")
        self.assertIn("plt.title(", boxplot)
        self.assertIn("segundos", boxplot)
        self.assertIn("plt.show()", boxplot)

    def test_question_7_3_mean_and_standard_deviation_with_units(self):
        mean = self.code_with("media = round(df[coluna].mean(), 2)")
        self.assertIn("segundos", mean)
        std = self.code_with("dpad = round(df[coluna].std(), 2)")
        self.assertIn("segundos", std)

    def test_question_7_4_interval_and_question(self):
        self.assertIn("limite_tolerancia_segundos = 6.0", self.all_code)
        self.assertIn(
            "quantidade_intervalo_depois=sum(i>=0 and i<= limite_tolerancia_segundos for i in df[coluna].sort_values())",
            self.all_code,
        )
        section = self.cells[self.find_markdown("## Questão 7.4")]["source"]
        self.assertIn("Pergunta", section)
        self.assertIn("?", section)

    def test_question_8_question_and_two_criteria(self):
        section = self.cells[self.find_markdown("## Questão 8")]["source"]
        self.assertIn("Pergunta", section)
        self.assertIn("?", section)
        self.assertIn("Critério 1", section)
        self.assertIn("Critério 2", section)
        for name in [
            "proporcao_criterio_1_antes",
            "proporcao_criterio_1_depois",
            "proporcao_criterio_2_antes",
            "proporcao_criterio_2_depois",
        ]:
            with self.subTest(name=name):
                self.assertIn(name, self.all_code)

    def test_comparison_reports_direction_without_claiming_causality(self):
        comparison = self.code_with("diferenca_media_segundos =")
        self.assertIn("if diferenca_media_segundos > 0", comparison)
        self.assertIn("não comprova causalidade", comparison.lower())
        self.assertEqual(comparison.lower().count("causalidade"), 1)

    def test_no_handmade_normal_functions(self):
        self.assertNotIn("def ", self.all_code)
        self.assertNotIn("math.exp", self.all_code)

    def test_interpretation_fields_follow_results(self):
        for marker in [
            "sns.boxplot(data=df[coluna])",
            "dpad = round(df[coluna].std(), 2)",
            "quantidade_intervalo_depois=",
            "proporcao_criterio_2_depois =",
            "diferenca_media_segundos =",
        ]:
            with self.subTest(marker=marker):
                following = self.cells[self.code_index(marker) + 1]
                self.assertEqual(following["cell_type"], "markdown")
                self.assertIn("**Interpretação breve:**", following["source"])
                self.assertNotIn("[", following["source"])

    def test_interpretation_fields_contain_conclusions_from_the_workbooks(self):
        fields = "\n".join(
            cell["source"]
            for cell in self.cells
            if cell["cell_type"] == "markdown"
            and "**Interpretação breve:**" in cell["source"]
        ).lower()
        for expected in ["5,10", "0,81", "85 de 100", "89%", "0%", "100%", "85%", "2,59", "causalidade"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, fields)


class Notebook2ExecutionTests(unittest.TestCase):
    def test_notebook_runs_from_top_to_bottom_without_errors(self):
        import nbformat
        from nbclient import NotebookClient

        notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
        client = NotebookClient(
            notebook,
            timeout=300,
            resources={"metadata": {"path": str(NOTEBOOK_PATH.parent)}},
        )
        client.execute()
        errors = [
            output
            for cell in notebook.cells
            if cell.cell_type == "code"
            for output in cell.get("outputs", [])
            if output.get("output_type") == "error"
        ]
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
