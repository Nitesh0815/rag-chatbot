from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

pdf_path = 'test_document.pdf'
c = canvas.Canvas(pdf_path, pagesize=letter)
c.setFont('Helvetica', 12)
c.drawString(50, 750, 'Sample Document: Python Programming')
c.drawString(50, 730, '')
c.drawString(50, 710, 'Chapter 1: Introduction to Python')
c.drawString(50, 690, 'Python is a high-level programming language known for its simplicity and readability.')
c.drawString(50, 670, 'It was created by Guido van Rossum and first released in 1991.')
c.drawString(50, 650, '')
c.drawString(50, 630, 'Key Features of Python:')
c.drawString(50, 610, '1. Easy to learn and read')
c.drawString(50, 590, '2. Versatile and powerful')
c.drawString(50, 570, '3. Large standard library')
c.drawString(50, 550, '4. Cross-platform compatibility')
c.drawString(50, 530, '')
c.drawString(50, 510, 'Chapter 2: Getting Started')
c.drawString(50, 490, 'To start programming in Python, you need to install Python from python.org.')
c.drawString(50, 470, 'Then you can write your first program: print("Hello, World!")')
c.save()
print('test_document.pdf created successfully')
