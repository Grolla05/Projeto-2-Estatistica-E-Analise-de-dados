"""Testes do padrão ABNT do relatório da Sprint 2 (`SPRINT2/Relatorio_Sprint2.docx`).

Normas consideradas: NBR 14724 (trabalhos acadêmicos: página, margens, fonte,
espaçamento, estrutura), NBR 6024 (numeração progressiva das seções),
NBR 6028 (resumo), NBR 10520 (citações) e NBR 6023 (referências).
"""

import re
import unittest
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "SPRINT2" / "Relatorio_Sprint2.docx"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
ALLOWED_FONTS = {"Arial", "Cambria Math", "Times New Roman"}  # Times só na capa, igual à da Sprint 1
TWIPS_CM = 566.93


def attr(element, name):
    return element.get(W + name) if element is not None else None


class Sprint2AbntTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with zipfile.ZipFile(REPORT_PATH) as docx:
            cls.document = ET.fromstring(docx.read("word/document.xml"))
            cls.styles = ET.fromstring(docx.read("word/styles.xml"))
            cls.headers = {
                name: ET.fromstring(docx.read(name))
                for name in docx.namelist()
                if re.fullmatch(r"word/header\d+\.xml", name)
            }
        cls.body = cls.document.find(W + "body")
        cls.paragraphs = list(cls.document.iter(W + "p"))
        # O Word regrava os identificadores dos estilos; por isso tudo é consultado pelo NOME do estilo.
        cls.style_names = {
            attr(style, "styleId"): attr(style.find(W + "name"), "val") for style in cls.styles.iter(W + "style")
        }

    # -- utilidades ---------------------------------------------------------
    @staticmethod
    def text_of(paragraph):
        return "".join(t.text or "" for t in paragraph.iter(W + "t"))

    def style_of(self, paragraph):
        style_id = attr(paragraph.find(f"{W}pPr/{W}pStyle"), "val")
        return self.style_names.get(style_id)

    def style(self, name):
        for style in self.styles.iter(W + "style"):
            if attr(style.find(W + "name"), "val") == name:
                return style
        self.fail(f"Estilo ausente: {name}")

    def resolved(self, style_name, path, name, default=None):
        """Valor efetivo de um atributo de estilo: o próprio estilo, os estilos-base e os padrões do documento.

        O Word omite do estilo o que já vale nos padrões, então é preciso resolver a herança.
        """
        style = self.style(style_name)
        while style is not None:
            element = style.find(path)
            if element is not None and attr(element, name) is not None:
                return attr(element, name)
            based = style.find(W + "basedOn")
            style = self.style(attr(based, "val")) if based is not None else None
        tag = W + path.rsplit("}", 1)[1]
        defaults = self.styles.find(f"{W}docDefaults/{W}pPrDefault/{W}pPr/{tag}")
        if defaults is not None and attr(defaults, name) is not None:
            return attr(defaults, name)
        return default

    def sections(self):
        return list(self.document.iter(W + "sectPr"))

    # -- página -------------------------------------------------------------
    def test_a4_page_and_abnt_margins_in_every_section(self):
        sections = self.sections()
        self.assertGreaterEqual(len(sections), 3, "capa, pré-textuais e textuais em seções distintas")
        for index, section in enumerate(sections):
            size = section.find(W + "pgSz")
            margin = section.find(W + "pgMar")
            with self.subTest(section=index):
                self.assertEqual((attr(size, "w"), attr(size, "h")), ("11906", "16838"))
                # superior e esquerda 3 cm; inferior e direita 2 cm
                self.assertAlmostEqual(int(attr(margin, "top")), 3 * TWIPS_CM, delta=10)
                self.assertAlmostEqual(int(attr(margin, "left")), 3 * TWIPS_CM, delta=10)
                self.assertAlmostEqual(int(attr(margin, "bottom")), 2 * TWIPS_CM, delta=10)
                self.assertAlmostEqual(int(attr(margin, "right")), 2 * TWIPS_CM, delta=10)

    def test_page_number_only_in_textual_section_at_top_right(self):
        sections = self.sections()
        with_header = [s for s in sections if s.find(W + "headerReference") is not None]
        self.assertEqual(len(with_header), 1)
        self.assertIs(with_header[0], sections[-1])
        self.assertAlmostEqual(int(attr(with_header[0].find(W + "pgMar"), "header")), 2 * TWIPS_CM, delta=10)
        self.assertEqual(len(self.headers), 1)
        header = next(iter(self.headers.values()))
        instructions = "".join(i.text or "" for i in header.iter(W + "instrText"))
        self.assertIn("PAGE", instructions)
        self.assertEqual(attr(header.find(f".//{W}jc"), "val"), "right")

    # -- fonte, tamanho e espaçamento ----------------------------------------
    def test_font_is_arial_12_and_nothing_is_larger_than_12(self):
        defaults = self.styles.find(f"{W}docDefaults/{W}rPrDefault/{W}rPr")
        self.assertEqual(attr(defaults.find(W + "rFonts"), "ascii"), "Arial")
        self.assertEqual(attr(defaults.find(W + "sz"), "val"), "24")
        for root in [self.document, self.styles]:
            for size in root.iter(W + "sz"):
                with self.subTest(size=attr(size, "val")):
                    self.assertLessEqual(int(attr(size, "val")), 24)
            for fonts in root.iter(W + "rFonts"):
                ascii_font = attr(fonts, "ascii")
                if ascii_font:
                    self.assertIn(ascii_font, ALLOWED_FONTS)

    def test_body_text_is_justified_with_1_5_spacing_and_1_25_cm_indent(self):
        name = "Corpo de texto"
        self.assertEqual(self.resolved(name, f"{W}pPr/{W}spacing", "line"), "360")
        self.assertEqual(self.resolved(name, f"{W}pPr/{W}spacing", "before", "0"), "0")
        self.assertEqual(self.resolved(name, f"{W}pPr/{W}spacing", "after", "0"), "0")
        self.assertEqual(self.resolved(name, f"{W}pPr/{W}jc", "val", "left"), "both")
        self.assertAlmostEqual(
            int(self.resolved(name, f"{W}pPr/{W}ind", "firstLine")), 1.25 * TWIPS_CM, delta=10
        )
        self.assertEqual(self.resolved("Corpo de texto sem recuo", f"{W}pPr/{W}ind", "firstLine"), "0")
        used = [p for p in self.paragraphs if self.style_of(p) in {"Corpo de texto", "Corpo de texto sem recuo"}]
        self.assertGreater(len(used), 20)

    def test_captions_sources_tables_and_references_are_10pt_single_spaced(self):
        for name in ["caption", "Fonte da ilustração", "Texto de tabela"]:
            style = self.style(name)
            with self.subTest(style=name):
                self.assertEqual(attr(style.find(f"{W}rPr/{W}sz"), "val"), "20")
                self.assertEqual(self.resolved(name, f"{W}pPr/{W}spacing", "line"), "240")
        self.assertEqual(self.resolved("Referência", f"{W}pPr/{W}spacing", "line"), "240")
        self.assertEqual(self.resolved("Referência", f"{W}pPr/{W}jc", "val", "left"), "left")

    def test_headings_follow_nbr_6024_typography(self):
        h1, h2, h3 = self.style("heading 1"), self.style("heading 2"), self.style("heading 3")
        self.assertIsNotNone(h1.find(f"{W}pPr/{W}pageBreakBefore"), "seção primária em nova página")
        self.assertIsNotNone(h1.find(f"{W}rPr/{W}b"))
        self.assertIsNone(h2.find(f"{W}rPr/{W}b"))
        self.assertIsNotNone(h3.find(f"{W}rPr/{W}b"))
        for style, level in [(h1, "0"), (h2, "1"), (h3, "2")]:
            self.assertEqual(attr(style.find(f"{W}pPr/{W}outlineLvl"), "val"), level)
        for name in ["heading 1", "heading 2", "heading 3"]:
            self.assertEqual(self.resolved(name, f"{W}pPr/{W}jc", "val", "left"), "left")

    def test_numbered_headings_use_arabic_progressive_numbering(self):
        primary = [self.text_of(p) for p in self.paragraphs if self.style_of(p) == "heading 1"]
        numbered = [h for h in primary if h[0].isdigit()]
        self.assertEqual([h.split(" ", 1)[0] for h in numbered], [str(i) for i in range(1, 9)])
        for heading in numbered:
            self.assertEqual(heading, heading.upper())
        for p in self.paragraphs:
            if self.style_of(p) in {"heading 2", "heading 3"}:
                self.assertRegex(self.text_of(p), r"^\d+\.\d+(\.\d+)? \S")

    # -- elementos obrigatórios e ordem ---------------------------------------
    def test_pre_textual_and_textual_elements_are_in_abnt_order(self):
        texts = [self.text_of(p).strip() for p in self.paragraphs]
        order = [
            "RESUMO",
            "LISTA DE FIGURAS",
            "LISTA DE TABELAS",
            "SUMÁRIO",
            "1 INTRODUÇÃO",
            "2 PERGUNTA DE INVESTIGAÇÃO",
            "3 DADOS E METODOLOGIA",
            "4 RESULTADOS ANTES E DEPOIS DA INTERVENÇÃO",
            "5 TESTE DE HIPÓTESE PARA A MÉDIA",
            "6 TESTE DE HIPÓTESE PARA A PROPORÇÃO",
            "7 COMPARAÇÃO COM A ANÁLISE PRELIMINAR",
            "8 CONCLUSÃO",
            "REFERÊNCIAS",
        ]
        positions = []
        for title in order:
            self.assertIn(title, texts, f"Elemento ausente: {title}")
            positions.append(len(texts) - 1 - texts[::-1].index(title))
        self.assertEqual(positions, sorted(positions))

    def first_section_paragraphs(self):
        end = next(
            index for index, p in enumerate(self.paragraphs) if p.find(f"{W}pPr/{W}sectPr") is not None
        )
        return self.paragraphs[: end + 1], self.paragraphs[end + 1 :]

    def test_cover_is_identical_to_the_sprint_1_cover(self):
        cover, _ = self.first_section_paragraphs()
        lines = [self.text_of(p) for p in cover]
        self.assertEqual(
            lines,
            [
                "PONTIFÍCIA UNIVERSIDADE CATÓLICA DE CAMPINAS",
                "ESCOLA POLITÉCNICA",
                "DISCIPLINA DE ESTATÍSTICA E ANÁLISE DE DADOS",
                "PROJETO 2: SPRINT 2",
                "GRUPO 6",
                "Eduarda Barbosa Kauffmann - RA: 24004761",
                "Felipe Grolla Freitas - RA: 24004846",
                "Nicollas Tavares da Silva - RA: 2502655",
                "Vitória Marques Pires - RA: 24011312",
                "Novembro, 2026",
            ],
        )
        # Sprint 1: tudo em negrito, Times New Roman 12, centralizado, espaçamento simples
        for paragraph in cover:
            for run in paragraph.iter(W + "r"):
                with self.subTest(text=self.text_of(paragraph)):
                    self.assertIsNotNone(run.find(f"{W}rPr/{W}b"))
                    self.assertEqual(attr(run.find(f"{W}rPr/{W}rFonts"), "ascii"), "Times New Roman")
                    # o Word omite o tamanho quando é igual ao padrão do documento (12 pt)
                    self.assertIn(attr(run.find(f"{W}rPr/{W}sz"), "val"), (None, "24"))
            self.assertEqual(self.style_of(paragraph), "Capa")
        self.assertEqual(self.resolved("Capa", f"{W}pPr/{W}jc", "val", "left"), "center")

    def test_title_page_elements(self):
        _, rest = self.first_section_paragraphs()
        title_page = "\n".join(self.text_of(p) for p in rest[:25])
        for expected in [
            "RA 24004846",
            "TESTES DE HIPÓTESES",
            "Relatório",
            "Estatística e Análise de Dados",
            "Escola Politécnica",
            "Professores",
            "Campinas",
            "novembro de 2026",
        ]:
            with self.subTest(title_page=expected):
                self.assertIn(expected, title_page)

    def test_abstract_and_keywords(self):
        texts = [self.text_of(p) for p in self.paragraphs]
        start = texts.index("RESUMO")
        words = len(texts[start + 1].split())
        self.assertGreater(words, 100)
        self.assertLess(words, 250)
        self.assertTrue(any(t.startswith("Palavras-chave:") for t in texts[start + 1 : start + 4]))

    def test_summary_and_lists_are_word_fields(self):
        instructions = " ".join(
            "".join(i.text or "" for i in p.iter(W + "instrText")) for p in self.paragraphs
        )
        self.assertIn('TOC \\o "1-3"', instructions)
        self.assertIn('\\c "Figura"', instructions)
        self.assertIn('\\c "Tabela"', instructions)

    # -- ilustrações, tabelas e equações -------------------------------------
    def test_figure_captions_above_with_source_below(self):
        captions = [p for p in self.paragraphs if self.style_of(p) == "caption"]
        figures = [p for p in captions if self.text_of(p).startswith("Figura ")]
        self.assertEqual(len(figures), 4)
        for index, caption in enumerate(figures, start=1):
            position = self.paragraphs.index(caption)
            with self.subTest(figure=index):
                self.assertTrue(self.text_of(caption).startswith(f"Figura {index} – "))
                self.assertIsNotNone(self.paragraphs[position + 1].find(f".//{W}drawing"))
                self.assertTrue(self.text_of(self.paragraphs[position + 2]).startswith("Fonte:"))

    def test_table_captions_above_with_source_below_and_ibge_borders(self):
        captions = [
            p for p in self.paragraphs if self.style_of(p) == "caption" and self.text_of(p).startswith("Tabela ")
        ]
        self.assertEqual(len(captions), 3)
        tables = list(self.body.iter(W + "tbl"))
        self.assertEqual(len(tables), 3)
        for index, table in enumerate(tables, start=1):
            borders = table.find(f"{W}tblPr/{W}tblBorders")
            with self.subTest(table=index):
                self.assertTrue(self.text_of(captions[index - 1]).startswith(f"Tabela {index} – "))
                self.assertEqual(attr(borders.find(W + "top"), "val"), "single")
                self.assertEqual(attr(borders.find(W + "bottom"), "val"), "single")
                for side in ["left", "right", "insideV"]:
                    element = borders.find(W + side)
                    self.assertTrue(element is None or attr(element, "val") in {"nil", "none"})
        sources = [p for p in self.paragraphs if self.text_of(p).startswith("Fonte:")]
        self.assertGreaterEqual(len(sources), 7)

    def test_equations_are_numbered_on_the_right(self):
        numbers = []
        for p in self.paragraphs:
            if self.style_of(p) == "Equação":
                match = re.search(r"\((\d+)\)$", self.text_of(p))
                self.assertIsNotNone(match, self.text_of(p))
                numbers.append(int(match.group(1)))
        self.assertGreaterEqual(len(numbers), 12)
        self.assertEqual(numbers, list(range(1, len(numbers) + 1)))

    # -- citações, referências e contexto da Sprint 1 --------------------------
    def test_citations_and_references_follow_abnt(self):
        texts = [self.text_of(p) for p in self.paragraphs]
        puc = "PONTIFÍCIA UNIVERSIDADE CATÓLICA DE CAMPINAS"
        self.assertTrue(any(f"({puc}, 2026a)" in t for t in texts))
        self.assertTrue(any(f"({puc}, 2026b)" in t for t in texts))
        self.assertTrue(any("(GRUPO 6, 2026)" in t for t in texts))
        references = [t for t, p in zip(texts, self.paragraphs) if self.style_of(p) == "Referência"]
        self.assertEqual(len(references), 3)
        self.assertTrue(references[0].startswith("GRUPO 6. Projeto 2: Sprint 1"))
        for entry in references[1:]:
            self.assertTrue(entry.startswith(puc + ". Orientações Sprint"))
            self.assertIn("Campinas: PUC-Campinas, 2026", entry)
        self.assertEqual(references, sorted(references), "referências em ordem alfabética")

    def test_report_recaps_what_was_done_in_sprint_1(self):
        texts = [self.text_of(p) for p in self.paragraphs]
        self.assertIn("1.2 RETOMADA DA ETAPA ANTERIOR (SPRINT 1)", texts)
        start = texts.index("1.2 RETOMADA DA ETAPA ANTERIOR (SPRINT 1)")
        recap = "\n".join(texts[start + 1 : start + 4])
        for expected in ["2,17", "2,72", "normal", "89%", "85 das 100", "Planilha 1", "Planilha 2"]:
            with self.subTest(expected=expected):
                self.assertIn(expected, recap)

    def test_placeholders_are_highlighted(self):
        for p in self.paragraphs:
            for run in p.iter(W + "r"):
                text = "".join(t.text or "" for t in run.iter(W + "t"))
                # intervalos matemáticos como [2, 3] não são placeholders
                if re.search(r"\[[^\]]*(?:[A-Za-zÀ-ÿ]|0{4,})", text):
                    with self.subTest(text=text):
                        self.assertEqual(attr(run.find(f"{W}rPr/{W}highlight"), "val"), "yellow")


if __name__ == "__main__":
    unittest.main()
