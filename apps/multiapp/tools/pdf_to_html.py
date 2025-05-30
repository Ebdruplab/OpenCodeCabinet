from nicegui import ui
from pdf2image import convert_from_path
import os
import uuid

OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def convert_pdf_to_images(pdf_path: str, output_folder: str):
    pages = convert_from_path(pdf_path, 300)
    image_files = []
    for i, page in enumerate(pages):
        image_path = os.path.join(output_folder, f'page_{i+1}.jpg')
        page.save(image_path, 'JPEG')
        image_files.append(image_path)
    return image_files


def generate_html_content(image_files):
    html = """
    <html>
    <head>
    <style>
        body { margin: 0; padding: 0; background-color: #f0f0f0; }
        img { display: block; margin: 0 auto; width: 100%; max-width: 1200px; }
    </style>
    </head>
    <body>
    """
    for image_file in image_files:
        relative_path = os.path.relpath(image_file, OUTPUT_DIR)
        html += f'<div><img src="/{relative_path}" /></div>\n'
    html += "</body></html>"
    return html


@ui.page("/pdf-to-html")
def pdf_to_html_page():
    ui.label("PDF to HTML Converter").classes("text-2xl m-4")

    uploaded_pdf = ui.upload(label="Upload PDF", max_files=1, auto_upload=True)
    output_area = ui.column().classes("w-full items-center")

    def handle_upload():
        if not uploaded_pdf.files:
            ui.notify("Please upload a PDF file first.", type="warning")
            return

        pdf_file = uploaded_pdf.files[0]
        pdf_path = os.path.join(OUTPUT_DIR, f'{uuid.uuid4()}.pdf')
        pdf_file.save(pdf_path)

        image_folder = os.path.join(OUTPUT_DIR, str(uuid.uuid4()))
        os.makedirs(image_folder, exist_ok=True)
        image_files = convert_pdf_to_images(pdf_path, image_folder)

        html_content = generate_html_content(image_files)
        html_path = os.path.join(image_folder, 'output.html')
        with open(html_path, 'w') as f:
            f.write(html_content)

        with output_area:
            output_area.clear()
            ui.label("Converted Images:").classes("text-lg mt-4")
            for image_file in image_files:
                ui.image(f'/{os.path.relpath(image_file, OUTPUT_DIR)}').classes("w-full max-w-3xl")
            ui.link("Download Full HTML", f'/{os.path.relpath(html_path, OUTPUT_DIR)}', new_tab=True)

    ui.button("Convert to HTML", on_click=handle_upload).classes("mt-4")

