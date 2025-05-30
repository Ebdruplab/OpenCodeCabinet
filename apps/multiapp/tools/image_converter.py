from nicegui import ui
from PIL import Image
import os
import uuid

OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

@ui.page("/image-converter")
def image_converter():
    ui.dark_mode()
    with ui.element("div").classes("absolute top-0 left-0 w-screen min-h-screen bg-[#1c2431] text-white"):
        with ui.column().classes("p-6 gap-4 max-w-3xl mx-auto"):
            ui.label("🖼️ Image Converter & Resizer").classes("text-6xl font-bold text-[#3ABFF8]")

            uploaded_image = ui.upload(label="Upload Image", max_files=1, auto_upload=True).classes("mt-2")
            format_select = ui.select(["PNG", "JPEG", "WEBP"], value="PNG", label="Output Format")
            scale_slider = ui.slider(min=0.1, max=2.0, value=1.0, step=0.1,
                                     label="Scale Factor (⚠️ scaling up may reduce quality)").classes("mt-4")

            convert_btn = ui.button("Convert & Download", 
                                    on_click=lambda: convert_image(uploaded_image, format_select.value, scale_slider.value)
                                   ).classes("bg-[#3ABFF8] text-black font-bold text-xl")

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
                ui.link("🔗 Download Converted Image", f'/{os.path.relpath(out_path, OUTPUT_DIR)}', new_tab=True)\
                    .classes("text-[#3ABFF8] underline text-xl")

