import os
import xml.etree.ElementTree as ET
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SVG_FOLDER = os.getenv("SVG_FOLDER")
EXCEL_FOLDER = os.getenv("EXCEL_FOLDER")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER")

if not SVG_FOLDER or not EXCEL_FOLDER or not OUTPUT_FOLDER:
    raise ValueError("SVG_FOLDER, EXCEL_FOLDER, and OUTPUT_FOLDER must be set in the .env file.")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ET.register_namespace("", "http://www.w3.org/2000/svg")
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
ns = {"svg": "http://www.w3.org/2000/svg"}

def wrap_element_with_link(parent, element, link):
    index = list(parent).index(element)
    parent.remove(element)
    a = ET.Element("{http://www.w3.org/2000/svg}a", {
        "{http://www.w3.org/1999/xlink}href": link,
        "target": "_blank"
    })
    a.append(element)
    parent.insert(index, a)

def process_svg(svg_path, excel_path, output_path):
    print(f"🔍 Processing {svg_path} with {excel_path}")
    try:
        df = pd.read_excel(excel_path)
        df["cx"] = df["cx"].astype(float).round(2).astype(str)
        df["cy"] = df["cy"].astype(float).round(2).astype(str)
    except Exception as e:
        print(f"❌ Failed to read Excel: {excel_path}\n   Error: {e}")
        return

    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()

        for shape_tag in ["circle", "ellipse"]:
            for shape in root.findall(f".//svg:{shape_tag}", ns):
                try:
                    cx = round(float(shape.get("cx")), 2)
                    cy = round(float(shape.get("cy")), 2)
                except (TypeError, ValueError):
                    continue

                match = df[(df["cx"] == str(cx)) & (df["cy"] == str(cy))]
                if not match.empty:
                    link = str(match.iloc[0]["link"])

                    # Make clickable
                    if not shape.get("stroke"):
                        shape.set("stroke", "black")
                        shape.set("stroke-width", "1")
                    if shape.get("fill") == "none" or not shape.get("fill"):
                        shape.set("fill", "white")
                        shape.set("fill-opacity", "0.01")

                    title = ET.Element("title")
                    title.text = link
                    shape.insert(0, title)

                    parent = root
                    for g in root.iter():
                        for child in list(g):
                            if child is shape:
                                parent = g
                                break
                    wrap_element_with_link(parent, shape, link)

        base = os.path.basename(svg_path).replace(".svg", "_output.svg")
        output_file = os.path.join(output_path, base)
        tree.write(output_file, encoding="utf-8", xml_declaration=True)
        print(f"✅ Saved: {output_file}\n")
    except Exception as e:
        print(f"❌ Error processing SVG {svg_path}:\n   Error: {e}")

# Match SVGs and Excels by base name
svg_files = [f for f in os.listdir(SVG_FOLDER) if f.endswith(".svg")]
excel_files = {os.path.splitext(f)[0]: f for f in os.listdir(EXCEL_FOLDER) if f.endswith(".xlsx")}

skipped = []

for svg_file in svg_files:
    base_name = os.path.splitext(svg_file)[0]
    if base_name not in excel_files:
        print(f"❌ No matching Excel for: {svg_file} — Skipping.\n")
        skipped.append(svg_file)
        continue

    svg_path = os.path.join(SVG_FOLDER, svg_file)
    excel_path = os.path.join(EXCEL_FOLDER, excel_files[base_name])
    process_svg(svg_path, excel_path, OUTPUT_FOLDER)

# Report skipped files
if skipped:
    print("⚠️ Skipped SVGs due to missing Excel files:")
    for f in skipped:
        print(f"   - {f}")
