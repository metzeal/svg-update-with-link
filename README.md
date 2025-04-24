# SVG Linker Utility

This Python tool adds clickable links to shapes (circles/ellipses) in SVG files based on coordinates from an Excel file.

## Setup

1. **Install Python** from [python.org](https://www.python.org/downloads).
2. **Clone the repo**:
   ```bash
   git clone https://github.com/metzeal/svg-update-with-link.git
3. **Set up a virtual environment**
   ```bash
   python -m venv venv
4. **Activate the virtual environment**
   ```bash
    .\venv\Scripts\activate
5. **Install dependencies**:
    ````bash
    pip install -r requirements.txt
6. **Configure: Create a .env file with**:
    ````bash
    SVG_FOLDER=./svg_files
    EXCEL_FOLDER=./excel_files
    OUTPUT_FOLDER=./output_svgs
7. **Usage**:
    Place your SVG files in svg_files/ and Excel files in excel_files/. The updated SVG files will be saved in the output_svgs/ folder with _output suffix.

    Run the script:
    ````bash
        python add_links_to_svg.py
