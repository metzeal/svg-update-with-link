# SVG Linker Utility

This Python tool adds clickable links to shapes (circles/ellipses) in SVG files based on coordinates from an Excel file.

## Setup

1. **Install Python** from [python.org](https://www.python.org/downloads).
2. **Clone the repo**:
   ```bash
   git clone https://github.com/metzeal/svg-update-with-link.git
3. **Install dependencies**:
    ````bash
    pip install -r requirements.txt
4. **Configure: Create a .env file with**:
    ````bash
    SVG_FOLDER=./svgs
    EXCEL_FOLDER=./excels
    OUTPUT_FOLDER=./output
5. **Usage**:
    Place your SVG files in svgs/ and Excel files in excels/. The updated SVG files will be saved in the output/ folder with _output suffix.

    Run the script:
    ````bash
        python add_links_to_svg.py
