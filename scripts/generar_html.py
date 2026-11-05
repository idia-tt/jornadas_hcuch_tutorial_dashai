"""Genera las dos guías HTML desde sus fuentes Markdown."""

import argparse
import base64
import re
import unicodedata
from html import escape
from pathlib import Path
from string import Template

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent.parent
DOCUMENTOS = {
    ROOT / "DashAI_Guia.md": ROOT / "DashAI_Guia.html",
    ROOT / "docs/dashai-local.md": ROOT / "DashAI_Local.html",
}


def renderizar(fuente):
    md = MarkdownIt("commonmark")
    tokens = md.parse(fuente.read_text(encoding="utf-8"))
    for i, token in enumerate(tokens):
        if token.type == "heading_open":
            titulo = unicodedata.normalize("NFKD", tokens[i + 1].content)
            slug = titulo.encode("ascii", "ignore").decode().lower()
            token.attrSet("id", re.sub(r"[^\w\s-]", "", slug).replace(" ", "-"))
        if token.type == "fence" and token.info.strip() == "mermaid":
            token.type = "html_block"
            token.content = f'<pre class="mermaid">{escape(token.content)}</pre>\n'
        for child in token.children or []:
            if child.type == "link_open":
                href = child.attrGet("href")
                ruta, _, fragmento = href.partition("#")
                destino = (fuente.parent / ruta).resolve()
                if destino in DOCUMENTOS:
                    child.attrSet(
                        "href",
                        DOCUMENTOS[destino].name
                        + (f"#{fragmento}" if fragmento else ""),
                    )
                elif ruta == "../DashAI_Guia.html":
                    child.attrSet("href", "DashAI_Guia.html")
    titulo = next(t.content for t in tokens if t.type == "inline" and t.level == 1)
    logos = []
    for nombre, sitio, alt in [
        ("idia", "https://idia.uchile.cl/", "IDIA"),
        ("dcc", "https://dcc.uchile.cl/", "DCC, Universidad de Chile"),
        ("dashai", "https://www.dash-ai.com/", "DashAI"),
    ]:
        logo = base64.b64encode((ROOT / f"assets/logo-{nombre}.svg").read_bytes())
        logos.append(
            f'<a href="{sitio}"><img alt="{alt}" '
            f'src="data:image/svg+xml;base64,{logo.decode()}" width="360" '
            'height="150"></a>'
        )
    scripts = ""
    if any(t.info.strip() == "mermaid" for t in tokens):
        scripts = (
            '<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/'
            'mermaid.min.js"></script>\n'
            "<script>if(window.mermaid){mermaid.initialize("
            '{startOnLoad:true,theme:"neutral"})}</script>'
        )
    return Template(
        (ROOT / "docs/plantilla.html").read_text(encoding="utf-8")
    ).substitute(
        title=escape(titulo),
        source=fuente.relative_to(ROOT).as_posix(),
        banner='<div class="logos">' + "".join(logos) + "</div>",
        body=md.renderer.render(tokens, md.options, {}),
        scripts=scripts,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Comprueba sin escribir")
    args = parser.parse_args()
    desactualizados = []
    for fuente, destino in DOCUMENTOS.items():
        contenido = renderizar(fuente)
        if args.check:
            if not destino.exists() or destino.read_text(encoding="utf-8") != contenido:
                desactualizados.append(destino.name)
        else:
            destino.write_text(contenido, encoding="utf-8", newline="\n")
            print(f"Generado: {destino.name}")
    if desactualizados:
        parser.exit(1, "Regenera los HTML: " + ", ".join(desactualizados) + "\n")


if __name__ == "__main__":
    main()
