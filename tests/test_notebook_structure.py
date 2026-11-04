import ast
import json
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "SPRINT1" / "Notebook_1_Analise_Antes_Intervencao.ipynb"


class NotebookStructureTests(unittest.TestCase):
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
            "4.1 Representação do histograma com a curva normal",
            "4.2 Boxplot",
            "5. Cálculo da Média, Mediana e do Desvio Padrão",
            "6. Testes de Normalidade",
            "7. Calculando a Probabilidade em Intervalos",
        ]
        positions = [self.find_markdown(step) for step in steps]
        self.assertEqual(positions, sorted(positions))
        for index in positions[:3]:
            self.assertEqual(self.cells[index + 1]["cell_type"], "code")

        question_1_index = self.find_markdown("Questão 1")
        self.assertGreater(question_1_index, positions[2])

    def test_imports_have_a_dedicated_cell(self):
        index = self.find_markdown("1. Importar as bibliotecas")
        source = self.following_code(index)
        tree = ast.parse(source)
        self.assertTrue(all(isinstance(node, (ast.Import, ast.ImportFrom)) for node in tree.body))
        imported = {
            alias.name
            for node in tree.body
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        self.assertEqual(imported, {"pandas", "math", "seaborn", "matplotlib.pyplot"})

    def test_file_column_setup_and_excel_read_are_separate(self):
        setup_index = self.find_markdown("2. Definir as variáveis")
        setup_source = self.following_code(setup_index)
        self.assertIn("arquivo =", setup_source)
        self.assertIn("coluna =", setup_source)
        self.assertNotIn("read_excel", setup_source)

        read_index = self.find_markdown("3. Leitura do arquivo de dados")
        read_source = self.following_code(read_index)
        self.assertIn("df_antes = pd.read_excel(arquivo)", read_source)
        self.assertNotIn("import ", read_source)

    def test_graph_cells_follow_the_reference_pattern(self):
        histogram_index = self.find_markdown(
            "4.1 Representação do histograma com a curva normal"
        )
        histogram = self.following_code(histogram_index)
        self.assertIn("sns.histplot(data=df_antes[coluna], kde=True)", histogram)
        self.assertIn("plt.show()", histogram)

        boxplot_index = self.find_markdown("4.2 Boxplot")
        boxplot = self.following_code(boxplot_index)
        self.assertIn("sns.boxplot(data=df_antes[coluna])", boxplot)
        self.assertIn("plt.show()", boxplot)

    def test_notebook_preserves_assignment_outputs_and_units(self):
        all_markdown = "\n".join(
            cell["source"] for cell in self.cells if cell["cell_type"] == "markdown"
        )
        all_code = "\n".join(
            cell["source"] for cell in self.cells if cell["cell_type"] == "code"
        )
        self.assertIn("Questão 1", all_markdown)
        self.assertIn("segundos", all_markdown.lower())
        self.assertIn("Questão 2", all_markdown)
        self.assertIn("Questão 3", all_markdown)
        self.assertIn("Questão 4", all_markdown)
        self.assertIn("Questão 5", all_markdown)
        self.assertIn("Questão 6", all_markdown)
        self.assertIn("quantidade_esperada_antes = 300", all_code)
        self.assertIn("quantidade_esperada_depois = 100", all_code)
        self.assertIn("quantil_normal_padrao(0.20)", all_code)
        self.assertIn("quantil_normal_padrao(0.70)", all_code)

    def test_source_workbooks_match_the_assignment_sample_sizes(self):
        before_path = ROOT / "Refs" / "Planilha 1 - TEMPO PAGAMENTO PIX.xlsx"
        after_path = ROOT / "Refs" / "Planilha 2 -TEMPO PAGAMENTO PIX-2.xlsx"
        self.assertEqual(len(pd.read_excel(before_path)), 300)
        self.assertEqual(len(pd.read_excel(after_path)), 100)

    def test_correct_workbooks_are_mapped_to_before_and_after(self):
        all_code = "\n".join(
            cell["source"] for cell in self.cells if cell["cell_type"] == "code"
        )
        self.assertIn('arquivo = "../Refs/Planilha 1 - TEMPO PAGAMENTO PIX.xlsx"', all_code)
        self.assertIn('arquivo_depois = "../Refs/Planilha 2 -TEMPO PAGAMENTO PIX-2.xlsx"', all_code)
        self.assertIn("df_antes = pd.read_excel(arquivo)", all_code)
        self.assertIn("df_depois = pd.read_excel(arquivo_depois)", all_code)

    def test_notebook_covers_post_intervention_and_comparison_criteria(self):
        all_markdown = "\n".join(
            cell["source"] for cell in self.cells if cell["cell_type"] == "markdown"
        )
        all_code = "\n".join(
            cell["source"] for cell in self.cells if cell["cell_type"] == "code"
        )
        for heading in ["Questão 7.1", "Questão 7.2", "Questão 7.3", "Questão 7.4", "Questão 8"]:
            self.assertIn(heading, all_markdown)
        self.assertIn("sns.histplot(data=df_depois[coluna], kde=True)", all_code)
        self.assertIn("sns.boxplot(data=df_depois[coluna])", all_code)
        self.assertIn("media_depois", all_code)
        self.assertIn("desvio_padrao_depois", all_code)
        self.assertIn("quantidade_intervalo_depois", all_code)
        self.assertIn("proporcao_criterio_1_antes", all_code)
        self.assertIn("proporcao_criterio_1_depois", all_code)
        self.assertIn("proporcao_criterio_2_antes", all_code)
        self.assertIn("proporcao_criterio_2_depois", all_code)

    def test_interval_reference_values_are_explicit_and_flagged_for_manual_justification(self):
        all_code = "\n".join(
            cell["source"] for cell in self.cells if cell["cell_type"] == "code"
        )
        all_markdown = "\n".join(
            cell["source"] for cell in self.cells if cell["cell_type"] == "markdown"
        )
        self.assertIn("limite_inferior_probabilidade = 2.0", all_code)
        self.assertIn("limite_superior_probabilidade = 3.0", all_code)
        self.assertIn("limite_objetivo_segundos = 3.0", all_code)
        self.assertTrue(
            "justificativa do grupo" in all_markdown.lower()
            or "justifique manualmente" in all_markdown.lower()
        )

    def test_comparison_reports_direction_without_claiming_causality(self):
        comparison_code = next(
            cell["source"]
            for cell in reversed(self.cells)
            if cell["cell_type"] == "code"
            and "diferenca_media_segundos" in cell["source"]
        )
        self.assertIn("if diferenca_media_segundos > 0", comparison_code)
        self.assertIn("não comprova causalidade", comparison_code.lower())

    def test_interpretation_fields_follow_results_that_require_explanation(self):
        required_result_markers = [
            "porcentagem_3dp =",  # conclusão sobre histograma e regra empírica
            "metade_superior_antes =",  # simetria dos quartis
            "quantis_teoricos_antes = [",  # diagrama Q-Q
            "probabilidade_intervalo_antes =",  # contexto da probabilidade
            "valor_minimo_30_maiores =",  # contexto dos percentis
            "quantidade_intervalo_depois =",  # pergunta/interpretação da faixa
            "diferenca_media_segundos =",  # análise comparativa
        ]
        for marker in required_result_markers:
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

    def test_interpretation_fields_contain_conclusions_from_the_workbooks(self):
        fields = [
            cell["source"]
            for cell in self.cells
            if cell["cell_type"] == "markdown"
            and "**Interpretação breve:**" in cell["source"]
        ]
        all_fields = "\n".join(fields).lower()
        self.assertEqual(len(fields), 7)
        self.assertNotIn("[", all_fields)
        for expected in [
            "68%",
            "96%",
            "100%",
            "0,28",
            "0,26",
            "78,81%",
            "2,17",
            "2,72",
            "0 de 100",
            "89%",
            "79,3%",
            "5,10",
            "2,51",
            "causalidade",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected.lower(), all_fields)

    def test_readme_documents_supported_windows_notebook_environment(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("python312\\python.exe", readme)
        self.assertIn(".venv\\scripts\\python.exe", readme)
        self.assertIn("msys2", readme)

    def test_normal_quantile_helper_matches_reference_probabilities(self):
        helper_cell = next(
            cell
            for cell in self.cells
            if cell["cell_type"] == "code"
            and "def cdf_normal_padrao" in cell["source"]
            and "def quantil_normal_padrao" in cell["source"]
        )
        namespace = {"math": __import__("math")}
        exec(helper_cell["source"], namespace)

        self.assertAlmostEqual(namespace["cdf_normal_padrao"](0), 0.5, places=12)
        self.assertAlmostEqual(
            namespace["quantil_normal_padrao"](0.20), -0.841621, places=5
        )
        self.assertAlmostEqual(
            namespace["quantil_normal_padrao"](0.70), 0.524401, places=5
        )


class NotebookCodeQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
        cls.code_cells = [
            "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]
            for cell in notebook["cells"]
            if cell["cell_type"] == "code"
        ]

    def code_with(self, marker):
        return next(source for source in self.code_cells if marker in source)

    def test_excel_engine_dependency_is_installed(self):
        __import__("openpyxl")

    def test_histogram_overlays_the_fitted_normal_curve(self):
        histogram = self.code_with("sns.histplot(data=df_antes[coluna], kde=True)")
        self.assertIn("math.exp", histogram)
        self.assertIn("plt.legend()", histogram)

    def test_counts_and_percentages_are_printed_with_labels(self):
        for marker in ["quantidade_1dp =", "quantidade_2dp =", "quantidade_3dp ="]:
            with self.subTest(marker=marker):
                source = self.code_with(marker)
                self.assertIn("int(", source)
                self.assertIn("print(", source)
        percentages = self.code_with("porcentagem_3dp =")
        self.assertIn("porcentagem_1dp =", percentages)
        self.assertIn("porcentagem_2dp =", percentages)
        self.assertIn("print(", percentages)

    def test_goal_threshold_is_defined_where_the_comparison_uses_it(self):
        comparison = self.code_with("proporcao_criterio_1_antes =")
        self.assertIn("limite_objetivo_segundos = 3.0", comparison)

    def test_causality_warning_is_printed_once(self):
        comparison = self.code_with("diferenca_media_segundos =")
        self.assertEqual(comparison.lower().count("causalidade"), 1)


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
