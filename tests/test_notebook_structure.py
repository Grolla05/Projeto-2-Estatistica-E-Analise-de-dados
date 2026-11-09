"""Testes do Notebook 1 — análise da Planilha 1 (antes da intervenção).

O Notebook 1 deve conter apenas as Questões 1 a 6, usando exclusivamente os
dados da Planilha 1 e os comandos do material "Python - Distribuição Normal"
(SPRINT1/refs/Python - Distribuição Normal-1-1.pdf).
"""

import ast
import json
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "SPRINT1" / "Notebook_1_Analise_Antes_Intervencao.ipynb"

PDF_IMPORTS = {"pandas", "numpy", "math", "seaborn", "matplotlib.pyplot", "statsmodels.api", "pylab"}


def load_cells(path):
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = [
        {
            **cell,
            "source": "".join(cell["source"])
            if isinstance(cell["source"], list)
            else cell["source"],
        }
        for cell in notebook["cells"]
    ]
    return notebook, cells


class NotebookStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notebook, cls.cells = load_cells(NOTEBOOK_PATH)
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

    def code_with(self, marker):
        return next(
            cell["source"]
            for cell in self.cells
            if cell["cell_type"] == "code" and marker in cell["source"]
        )

    def test_notebook_is_valid_and_code_cells_parse(self):
        self.assertEqual(self.notebook["nbformat"], 4)
        for cell in self.cells:
            if cell["cell_type"] == "code":
                ast.parse(cell["source"])

    def test_tutorial_steps_are_separate_cells_in_order(self):
        steps = [
            "1. Importar as bibliotecas",
            "2. Definir as variáveis",
            "3. Leitura do arquivo de dados",
            "## Questão 1",
            "## Questão 2",
            "4.1 Representação do histograma com a curva normal",
            "4.2 Boxplot",
            "## Questão 3",
            "5. Cálculo da Média, Mediana e do Desvio Padrão",
            "## Questão 4",
            "6. Testes de Normalidade",
            "6.1 Análise do Histograma",
            "6.2 Análise do Boxplot",
            "6.3 Gráfico Q-Q",
            "## Questão 5",
            "7. Calculando a Probabilidade em Intervalos",
            "## Questão 6",
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
        self.assertIn("import statsmodels.api as sm", source)
        self.assertIn("import numpy as np", source)

    def test_file_column_setup_and_excel_read_follow_the_pdf(self):
        setup_source = self.following_code(self.find_markdown("2. Definir as variáveis"))
        self.assertIn('arquivo = "../Refs/Planilha 1 - TEMPO PAGAMENTO PIX.xlsx"', setup_source)
        self.assertIn('coluna = "Tempo_processamento_seg"', setup_source)
        self.assertNotIn("read_excel", setup_source)

        read_source = self.following_code(self.find_markdown("3. Leitura do arquivo de dados"))
        self.assertIn("df=pd.read_excel(arquivo)", read_source)
        self.assertNotIn("import ", read_source)

    def test_notebook_only_uses_spreadsheet_1(self):
        for forbidden in ["df_depois", "df_antes", "arquivo_depois", "Planilha 2 -TEMPO"]:
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, self.all_code)
        for forbidden in ["Questão 7", "Questão 8"]:
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, self.all_markdown)

    def test_question_1_has_complete_problem_statement(self):
        question_1 = self.cells[self.find_markdown("## Questão 1")]["source"]
        lowered = question_1.lower()
        for expected in [
            "contexto",
            "problema",
            "possível causa",
            "importância",
            "valores de referência",
            "antifraude",
            "2 e 3 segundos",
            "6 segundos",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, lowered)
        self.assertNotIn("preencher manualmente", lowered)
        self.assertNotIn("[", question_1)

    def test_graph_cells_use_the_pdf_commands_with_titles_and_units(self):
        histogram = self.following_code(
            self.find_markdown("4.1 Representação do histograma com a curva normal")
        )
        self.assertIn("sns.histplot(data=df[coluna],kde=True)", histogram)
        self.assertIn("plt.title(", histogram)
        self.assertIn("segundos", histogram)
        self.assertIn("plt.show()", histogram)

        boxplot = self.following_code(self.find_markdown("4.2 Boxplot"))
        self.assertIn("sns.boxplot(data=df[coluna])", boxplot)
        self.assertIn("plt.title(", boxplot)
        self.assertIn("segundos", boxplot)
        self.assertIn("plt.show()", boxplot)

    def test_mean_median_and_standard_deviation_follow_project_1(self):
        self.assertIn("media = round(df[coluna].mean(), 2)", self.all_code)
        self.assertIn("mediana = round(df[coluna].median(), 2)", self.all_code)
        self.assertIn("dpad = round(df[coluna].std(), 2)", self.all_code)
        for marker in ["media = round(", "dpad = round("]:
            with self.subTest(marker=marker):
                self.assertIn("segundos", self.code_with(marker))

    def test_empirical_rule_uses_the_pdf_commands(self):
        for command in [
            "limite_inf1dp=round(media-dpad,2)",
            "limite_inf2dp=round(media-2*dpad,2)",
            "limite_inf3dp=round(media-3*dpad,2)",
            "limite_sup1dp=round(media+dpad,2)",
            "limite_sup2dp=round(media+2*dpad,2)",
            "limite_sup3dp=round(media+3*dpad,2)",
            "quantidade_1dp=sum(i>=limite_inf1dp and i<= limite_sup1dp for i in df[coluna].sort_values())",
            "quantidade_2dp=sum(i>=limite_inf2dp and i<= limite_sup2dp for i in df[coluna].sort_values())",
            "quantidade_3dp=sum(i>=limite_inf3dp and i<= limite_sup3dp for i in df[coluna].sort_values())",
            "porcentagem1 = round((quantidade_1dp/len(df[coluna]))*100,2)",
            "porcentagem2 = round((quantidade_2dp/len(df[coluna]))*100,2)",
            "porcentagem3 = round((quantidade_3dp/len(df[coluna]))*100,2)",
        ]:
            with self.subTest(command=command):
                self.assertIn(command, self.all_code)
        self.assertNotIn("99,7", self.all_code + self.all_markdown)

    def test_quartiles_follow_project_1(self):
        self.assertIn("Q1 = df[coluna].quantile(q=0.25)", self.all_code)
        self.assertIn("Q2 = df[coluna].quantile(q=0.50)", self.all_code)
        self.assertIn("Q3 = df[coluna].quantile(q=0.75)", self.all_code)

    def test_qq_plot_uses_statsmodels_like_the_pdf(self):
        qq = self.following_code(self.find_markdown("6.3 Gráfico Q-Q"))
        self.assertIn("sm.qqplot(df[coluna], line = 'r')", qq)
        self.assertIn("pylab.show()", qq)
        self.assertIn("plt.title(", qq)

    def test_probability_uses_norm_cdf_with_justified_interval(self):
        self.assertIn(
            "norm.cdf(3,loc=media,scale=dpad).round(4)-norm.cdf(2,loc=media,scale=dpad).round(4)",
            self.all_code,
        )
        question_5 = self.cells[self.find_markdown("## Questão 5")]["source"].lower()
        self.assertIn("justificativa", question_5)
        self.assertNotIn("provisório", self.all_markdown.lower())

    def test_percentiles_use_norm_ppf(self):
        self.assertIn("norm.ppf(0.20,loc=media,scale=dpad).round(2)", self.all_code)
        self.assertIn("norm.ppf(0.70,loc=media,scale=dpad).round(2)", self.all_code)

    def test_no_handmade_normal_functions(self):
        self.assertNotIn("def ", self.all_code)
        self.assertNotIn("math.erf", self.all_code)
        self.assertNotIn("math.exp", self.all_code)

    def test_normality_tests_have_explicit_conclusions(self):
        lowered = self.all_markdown.lower()
        self.assertIn("conclusão geral", lowered)
        self.assertIn("distribuição normal", lowered)

    def test_interpretation_fields_follow_results_that_require_explanation(self):
        for marker in [
            "porcentagem3 =",
            "Q3_menos_Q2 =",
            "sm.qqplot(",
            "probabilidade_intervalo =",
            "valor_minimo_30_maiores =",
        ]:
            with self.subTest(marker=marker):
                result_index = next(
                    index
                    for index, cell in enumerate(self.cells)
                    if cell["cell_type"] == "code" and marker in cell["source"]
                )
                following = self.cells[result_index + 1]
                self.assertEqual(following["cell_type"], "markdown")
                self.assertIn("**Interpretação breve:**", following["source"])
                self.assertNotIn("[", following["source"])

    def test_interpretation_fields_contain_conclusions_from_the_workbook(self):
        fields = [
            cell["source"]
            for cell in self.cells
            if cell["cell_type"] == "markdown"
            and "**Interpretação breve:**" in cell["source"]
        ]
        all_fields = "\n".join(fields).lower()
        self.assertEqual(len(fields), 5)
        for expected in ["68%", "96%", "100%", "0,28", "0,26", "78,85%", "2,17", "2,72"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, all_fields)

    def test_source_workbooks_match_the_assignment_sample_sizes(self):
        before_path = ROOT / "Refs" / "Planilha 1 - TEMPO PAGAMENTO PIX.xlsx"
        after_path = ROOT / "Refs" / "Planilha 2 -TEMPO PAGAMENTO PIX-2.xlsx"
        self.assertEqual(len(pd.read_excel(before_path)), 300)
        self.assertEqual(len(pd.read_excel(after_path)), 100)

    def test_readme_documents_environment_and_both_notebooks(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("python312\\python.exe", readme)
        self.assertIn(".venv\\scripts\\python.exe", readme)
        self.assertIn("msys2", readme)
        self.assertIn("notebook_1_analise_antes_intervencao.ipynb", readme)
        self.assertIn("notebook_2_analise_depois_da_intervencao.ipynb", readme)

    def test_pdf_dependencies_are_installed_and_listed(self):
        for module in ["openpyxl", "numpy", "scipy", "statsmodels"]:
            with self.subTest(module=module):
                __import__(module)
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8").split()
        for package in ["numpy", "scipy", "statsmodels"]:
            with self.subTest(package=package):
                self.assertIn(package, requirements)


class NotebookExecutionTests(unittest.TestCase):
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
