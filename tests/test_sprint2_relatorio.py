"""Testes do relatório Word da Sprint 2 (`SPRINT2/Relatorio_Sprint2.docx`).

A rubrica exige capa (Escola, Curso, Componente curricular, nomes e RAs,
data), texto estruturado (não no formato de respostas às questões) e todos os
itens solicitados: situação, parâmetros, hipóteses, regiões, z calculado,
decisões, conclusões e comparação com a análise preliminar.
"""

import html
import re
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "SPRINT2" / "Relatorio_Sprint2.docx"
PDF_PATH = ROOT / "SPRINT2" / "Relatorio_Sprint2.pdf"


class Sprint2ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with zipfile.ZipFile(REPORT_PATH) as docx:
            cls.names = docx.namelist()
            xml = docx.read("word/document.xml").decode("utf-8")
        paragraphs = re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S)
        cls.paragraphs = [
            html.unescape("".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", p))) for p in paragraphs
        ]
        cls.text = "\n".join(cls.paragraphs)

    def test_cover_has_required_items(self):
        cover = "\n".join(self.paragraphs[:40]).lower()
        for expected in [
            "pontifícia universidade católica de campinas",
            "escola politécnica",
            "estatística e análise de dados",
            "grupo 6",
            "eduarda barbosa kauffmann – ra 24004761",
            "felipe grolla freitas – ra 24004846",
            "nicollas tavares da silva – ra 2502655",
            "vitória marques pires – ra 24011312",
            "novembro de 2026",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, cover)

    def test_structured_text_not_question_answers(self):
        self.assertNotIn("Questão", self.text)

    def test_situation_items_and_parameters(self):
        lowered = self.text.lower()
        for expected in ["situação", "problema", "objetivo", "intervenção", "população", "amostra"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, lowered)
        for expected in ["2,51", "0,40", "5,10", "0,81", "78,85%", "0/100"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.text)

    def test_question_reformulation_and_interval_correction(self):
        self.assertIn("?", self.text)
        self.assertIn("[2, 3]", self.text)
        self.assertIn("[0, 6]", self.text)

    def test_formulas_are_described(self):
        for expected in ["σ/√n", "√(p₀(1 − p₀)/n)", "H₀", "H₁", "μ > 2,51", "p < 0,7885"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.text)

    def test_results_for_both_tests_and_levels(self):
        for expected in ["64,75", "−19,31", "2,326", "1,645", "1%", "5%", "rejeita"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.text)
        self.assertGreaterEqual(self.text.count("região de rejeição"), 4)

    def test_comparison_with_preliminary_analysis(self):
        lowered = self.text.lower()
        self.assertIn("análise preliminar", lowered)
        self.assertIn("coincide", lowered)

    def test_four_graphs_are_embedded(self):
        images = [name for name in self.names if name.startswith("word/media/")]
        self.assertGreaterEqual(len(images), 4)

    def test_graphs_have_two_panels_with_the_calculated_z(self):
        # Cada figura tem dois painéis lado a lado (curva de -4 a 4 e escala ampliada com o z): proporção larga, bem acima dos 4:3 anteriores.
        import struct

        with zipfile.ZipFile(REPORT_PATH) as docx:
            images = [n for n in docx.namelist() if n.startswith("word/media/")]
            for name in images:
                header = docx.read(name)[:24]
                width, height = struct.unpack(">II", header[16:24])
                with self.subTest(image=name):
                    self.assertGreaterEqual(width / height, 1.7)

    def test_report_text_mentions_the_two_panels(self):
        self.assertIn("escala ampliada", self.text.lower())

    def test_pdf_delivery_exists(self):
        # A rubrica pede a entrega em PDF (Qualidade de entrega).
        self.assertTrue(PDF_PATH.exists(), "Exporte o relatório para SPRINT2/Relatorio_Sprint2.pdf")
        data = PDF_PATH.read_bytes()
        self.assertTrue(data.startswith(b"%PDF"))
        self.assertGreater(len(data), 50_000)


if __name__ == "__main__":
    unittest.main()
