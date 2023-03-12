from weasyprint import HTML
import flask

html = HTML('templates/invoice.html')
html.write_pdf('invoice.pdf')