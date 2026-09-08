from pathlib import Path
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

BASE = Path(__file__).resolve().parent
root = BASE / 'figma-report-v2'
output = BASE / 'Mohammad-Bakr-Portfolio-Report-v2.pdf'
width, height = 1920, 1080
pdf = canvas.Canvas(str(output), pagesize=(width, height), pageCompression=1)
for svg in sorted(root.glob('*.svg')):
    drawing = svg2rlg(str(svg))
    if drawing is None:
        raise RuntimeError(f'Could not parse {svg}')
    source_width = drawing.width or width
    source_height = drawing.height or height
    drawing.scale(width / source_width, height / source_height)
    renderPDF.draw(drawing, pdf, 0, 0)
    pdf.showPage()
pdf.setTitle('Mohammad J. Bakr — Portfolio Report V2')
pdf.setAuthor('Mohammad J. Bakr')
pdf.save()
print(f'created {output} with {len(list(root.glob("*.svg")))} pages')
