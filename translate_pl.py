import os
from urllib.parse import quote
from playwright.sync_api import sync_playwright
import time
# Path to the browser extension CRX file
# unzip
extension_path = "chrome-immersive-translate-0.6.1"
extension_path = os.path.join(os.path.dirname(__file__), extension_path)

# https://github.com/immersive-translate/immersive-translate/releases/download/v0.6.1/chrome-immersive-translate-0.6.1.zip

# Path to the folder containing PDF files
pdf_folder = "hine-en"

# Output folder to save the result PDFs
output_folder = "hine-cn"

def save_pdf_with_extension(page, pdf_path, output_path):
    # Load the PDF file in the browser
    page.goto("file://" + pdf_path)

    # Wait for the PDF to load
    page.wait_for_load_state("networkidle")

    # Use the browser extension to modify the page if needed
    # Replace "extension_function" with the actual function provided by your extension
    page.evaluate("extension_function()")

    
    # Save the modified page as a PDF
    page.pdf(path=output_path)

with sync_playwright() as playwright:
    # Launch the browser with the extension loaded
    context = playwright.chromium.launch_persistent_context(
        "",
        headless=False,
        args=[
            f"--disable-extensions-except={extension_path}",
            f"--load-extension={extension_path}",
        ],
    )
    # for manifest v2:
    # background = context.background_pages[0]
    # if not background:
    #     background = context.wait_for_event("backgroundpage")

    # for manifest v3:
    print(len(context.service_workers))
    background = context.service_workers[0]
    if not background:
        background = context.wait_for_event("serviceworker")

    extension_id = background.url.split("/")[2]
    print('id=====',extension_id)
    page = context.new_page()


# chrome-extension://bpoadfkcbjbfhfodiogcnhhhpibjhbnh/pdf/index.html
# chrome-extension://bpoadfkcbjbfhfodiogcnhhhpibjhbnh/pdf/index.html?file=file%3A%2F%2F%2FUsers%2Fwenke%2Fgithub%2Fhine-latest-paper%2Fhine-en%2Fwinston1991.pdf

# chrome-extension://bpoadfkcbjbfhfodiogcnhhhpibjhbnh/pdf/index.html?file=file%3A%2F%2F%2FUsers%2Fwenke%2Fgithub%2Fhine-latest-paper%2Fhine-en%2Fwinston1991.pdf
# chrome-extension://bpoadfkcbjbfhfodiogcnhhhpibjhbnh/pdf/index.html?file=files:///Users/wenke/github/hine-latest-paper/hine-en/chin2018%20(2).pdf
    base="chrome-extension://bpoadfkcbjbfhfodiogcnhhhpibjhbnh/pdf/index.html"
    # Iterate over the PDF files in the folder
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            output_filename = quote(filename)
            # url=base+"?file=files://"+os.path.join(os.path.dirname(__file__),pdf_path)
            page.goto(base)
            page.wait_for_load_state('networkidle')
            
            page.locator('#openFile').set_input_files(os.path.join(os.path.dirname(__file__),pdf_path))
            output_path = os.path.join(output_folder, output_filename)
            
            # Save the PDF page with the extension
            save_pdf_with_extension(page, pdf_path, output_path)

    # Close the browser
    context.close()
