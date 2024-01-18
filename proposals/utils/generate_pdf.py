import io

from django.core.files.base import ContentFile
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


class FileGenerator:
    def __init__(self, content):
        self.content = content

    def generate_pdf(self):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        y_cord = 750
        
        pdfmetrics.registerFont(TTFont('DejaVuSerif', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'))
        p.setFont('DejaVuSerif', 12)

        for head in self.content.keys():
            p.drawString(100, y_cord, f'{head}: {self.content[head]}')
            y_cord -= 50

        p.showPage()
        p.save()
        buffer.seek(0)

        return buffer
