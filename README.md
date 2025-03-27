# EXR to JPG CONVERSION TOOL
A user-friendly PySide6 GUI application that batch converts .exr image sequences to .jpg with accurate color space transforms, including ACEScg to sRGB or Rec.709. Built with production-ready tools like OpenImageIO, OpenColorIO, and NumPy, it ensures high-quality conversions while maintaining speed and flexibility.

🛠️ Features
🔍 Batch convert folders of EXR sequences to JPGs

🎨 Supports accurate ACEScg → sRGB / Rec.709 color pipeline using OCIO

📦 Optional support for RAW (linear Rec.709) input

📁 Custom input and output folder selection

🧠 Automatic filename tagging with color space info (e.g., ACEScg_to_sRGB_shot01.jpg)

⚡ Optimized buffer-based OCIO processing for speed

🧰 Built using:

PySide6

OpenImageIO

OpenColorIO

NumPy

🎛️ Color Workflow
Supports two input color spaces:

ACEScg (transformed via OCIO using ACES 1.0.3 config)

RAW (Linear Rec.709) (converted using gamma curves)

And two output transforms:

sRGB

Rec.709

If input is ACEScg, the tool uses the OCIO config for accurate tone mapping and display rendering.

🚀 Getting Started
📦 Install dependencies:
bash
Copy
Edit
pip install PySide6 OpenImageIO PyOpenColorIO numpy
