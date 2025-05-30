from nicegui import ui
from pdf2image import convert_from_path
from PIL import Image
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
        body { margin: 0; padding: 0; background-color: #1c2431; color: #f0f0f0; font-size: 1.5em; }
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
def pdf_to_html():
    ui.dark_mode()
    with ui.element("div").classes("absolute top-0 left-0 w-screen min-h-screen bg-[#1c2431] text-white"):
        with ui.column().classes("p-6 gap-4 max-w-5xl mx-auto"):
            ui.label("📄 PDF to HTML Converter").classes("text-6xl font-bold text-[#3ABFF8]")

            with ui.card().classes("w-full p-6 bg-[#2a2f3a] shadow-lg rounded-xl"):
                ui.label("1️⃣ Upload your PDF file").classes("text-xl font-semibold text-[#f0f0f0]")
                uploaded_pdf = ui.upload(label="Upload PDF", max_files=1, auto_upload=True).classes("mt-2")

            with ui.card().classes("w-full p-6 bg-[#2a2f3a] shadow-lg rounded-xl"):
                ui.label("2️⃣ Convert to HTML").classes("text-xl font-semibold text-[#f0f0f0]")
                ui.button("Convert", on_click=lambda: handle_upload(uploaded_pdf))\
                    .classes("w-full bg-[#3ABFF8] text-black font-bold hover:bg-[#2ec4d6] mt-2 text-xl")

            output_area = ui.column().classes("w-full items-center gap-4")

            def handle_upload(upload_widget):
                output_area.clear()
                if not upload_widget.files:
                    ui.notify("Please upload a PDF first.", type="warning")
                    return

                pdf_file = upload_widget.files[0]
                pdf_path = os.path.join(OUTPUT_DIR, f'{uuid.uuid4()}.pdf')
                pdf_file.save(pdf_path)

                image_folder = os.path.join(OUTPUT_DIR, str(uuid.uuid4()))
                os.makedirs(image_folder, exist_ok=True)
                image_files = convert_pdf_to_images(pdf_path, image_folder)

                html_content = generate_html_content(image_files)
                html_path = os.path.join(image_folder, 'output.html')
                with open(html_path, 'w') as f:
                    f.write(html_content)

                ui.notify("✅ Conversion complete!")

                with output_area:
                    ui.label("🖼️ Converted Pages").classes("text-3xl font-semibold text-[#3ABFF8] mt-4")
                    for image_file in image_files:
                        ui.image(f'/{os.path.relpath(image_file, OUTPUT_DIR)}').classes("w-full max-w-3xl rounded-lg shadow")
                    ui.link("🔗 Download HTML", f'/{os.path.relpath(html_path, OUTPUT_DIR)}', new_tab=True)\
                        .classes("text-[#3ABFF8] underline text-xl")

@ui.page("/image-converter")
def image_converter():
    ui.dark_mode()
    with ui.element("div").classes("absolute top-0 left-0 w-screen min-h-screen bg-[#1c2431] text-white"):
        with ui.column().classes("p-6 gap-4 max-w-3xl mx-auto"):
            ui.label("🖼️ Image Converter & Resizer").classes("text-6xl font-bold text-[#3ABFF8]")

            uploaded_image = ui.upload(label="Upload Image", max_files=1, auto_upload=True).classes("mt-2")
            format_select = ui.select(["PNG", "JPEG", "WEBP"], value="PNG", label="Output Format")
            scale_slider = ui.slider(min=0.1, max=2.0, value=1.0, step=0.1, label="Scale Factor (⚠️ scaling up may reduce quality)").classes("mt-4")
            convert_btn = ui.button("Convert & Download", on_click=lambda: convert_image(uploaded_image, format_select.value, scale_slider.value)).classes("bg-[#3ABFF8] text-black font-bold text-xl")
            status = ui.label("...").classes("text-lg text-[#3ABFF8] mt-2")

            def convert_image(upload_widget, out_format, scale):
                if not upload_widget.files:
                    ui.notify("Please upload an image first.", type="warning")
                    return

                image_file = upload_widget.files[0]
                src_path = os.path.join(OUTPUT_DIR, f'{uuid.uuid4()}_{image_file.name}')
                image_file.save(src_path)

                with Image.open(src_path) as img:
                    new_size = (int(img.width * scale), int(img.height * scale))
                    img = img.resize(new_size)
                    out_path = src_path.rsplit('.', 1)[0] + f'_converted.{out_format.lower()}'
                    img.save(out_path, format=out_format.upper())

                status.text = "✅ Converted successfully."
                ui.link("🔗 Download Converted Image", f'/{os.path.relpath(out_path, OUTPUT_DIR)}', new_tab=True).classes("text-[#3ABFF8] underline text-xl")

@ui.page("/")
def main_page():
    ui.dark_mode()
    with ui.element("div").classes("absolute top-0 left-0 w-screen min-h-screen bg-[#1c2431] text-white"):
        with ui.column().classes("p-6 gap-4 max-w-xl mx-auto"):
            ui.label("🔧 Welcome to the Multi-Tool App").classes("text-6xl font-bold text-[#3ABFF8]")
            ui.link("📄 PDF to HTML Tool", "/pdf-to-html").classes("text-[#3ABFF8] underline text-xl")
            ui.link("🖼️ Image Converter", "/image-converter").classes("text-[#3ABFF8] underline text-xl")

ui.run(reload=False)

