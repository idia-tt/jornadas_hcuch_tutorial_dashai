"""Comprueba las guías descargables y sus enlaces internos."""

import unittest
from html.parser import HTMLParser

from scripts.generar_html import DOCUMENTOS, ROOT, renderizar


class Pagina(HTMLParser):
    def __init__(self, contenido):
        super().__init__()
        self.ids = set()
        self.enlaces = []
        self.logos = []
        self.feed(contenido)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a":
            self.enlaces.append(attrs.get("href", ""))
        if tag == "img":
            self.logos.append(attrs)


class GenerarHTMLTest(unittest.TestCase):
    def test_guias_actualizadas_y_enlaces_validos(self):
        paginas = {}
        for fuente, destino in DOCUMENTOS.items():
            contenido = renderizar(fuente)
            self.assertEqual(destino.read_text(encoding="utf-8"), contenido)
            self.assertIn('<html lang="es">', contenido)
            paginas[destino.name] = Pagina(contenido)
        for pagina in paginas.values():
            self.assertEqual(len(pagina.logos), 3)
            for logo in pagina.logos:
                self.assertTrue(logo["alt"])
                self.assertTrue(logo["src"].startswith("data:image/svg+xml;base64,"))
            for href in pagina.enlaces:
                if ":" in href:
                    continue
                ruta, _, fragmento = href.partition("#")
                if ruta:
                    self.assertTrue((ROOT / ruta).is_file(), href)
                if fragmento:
                    destino = paginas[ruta] if ruta else pagina
                    self.assertIn(fragmento, destino.ids, href)

    def test_diagramas_y_codigo(self):
        guia = renderizar(ROOT / "DashAI_Guia.md")
        self.assertEqual(guia.count('<pre class="mermaid">'), 2)
        self.assertIn("mermaid.initialize", guia)
        self.assertIn("--&gt;", guia)
        self.assertNotIn("&amp;gt;", guia)
        local = renderizar(ROOT / "docs/dashai-local.md")
        self.assertIn('<pre><code class="language-powershell">', local)
        self.assertIn("DashAI_Guia.html", local)
        self.assertNotIn("mermaid.min.js", local)


if __name__ == "__main__":
    unittest.main()
