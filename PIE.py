import fitz  # PyMuPDF
import os
import math

output_dir = "pdf_images"
os.makedirs(output_dir, exist_ok=True)

for pdf_file in [f for f in os.listdir('.') if f.lower().endswith('.pdf')]:
    doc = fitz.open(pdf_file)

    base_name = os.path.splitext(pdf_file)[0]
    pdf_output_dir = os.path.join(output_dir, base_name)
    os.makedirs(pdf_output_dir, exist_ok=True)

    total_images = 0
    for page_index in range(len(doc)):
        total_images += len(doc[page_index].get_images(full=True))

    digits = max(3, len(str(total_images)))
    counter = 1
    img_count = 0

    for page_index in range(len(doc)):
        images = doc[page_index].get_images(full=True)

        for img in images:
            xref = img[0]
            info = doc.extract_image(xref)
            image_bytes = info["image"]
            image_ext = info["ext"]

            image_filename = f"{counter:0{digits}d}.{image_ext}"
            image_path = os.path.join(pdf_output_dir, image_filename)

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            counter += 1
            img_count += 1

    doc.close()

    print(f"Done: {pdf_file}  -> {img_count} images exported")

print("\n✅ All PDFs processed.")
