import io
import markdown
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from weasyprint import HTML


class FileGenerator:
    def __init__(self, content):
        self.content = content


    def generate_pdf(self):
        buffer = io.BytesIO()
        markdown_content = markdown.markdown(self.content)
        html_content =  f"""
        <html>
            <head>
                <style>
                    @font-face {{
                        font-family: 'Roboto';
                        src: url('https://fonts.gstatic.com/s/roboto/v27/KFOmCnqEu92Fr1Mu4mxP.ttf') format('truetype');
                    }}
                    body {{
                        font-family: 'Roboto', sans-serif;
                    }}
                </style>
            </head>
            <body>
                {markdown_content}
            </body>
        </html>
        """
        
        HTML(string=html_content).write_pdf(buffer)

        buffer.seek(0)

        return buffer
