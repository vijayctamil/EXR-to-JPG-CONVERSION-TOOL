# ✨ EXR to JPG Converter – ACES & Color-Space Aware Tool

A user-friendly **PySide6 GUI application** that batch converts `.exr` image sequences to `.jpg` with **accurate color space transforms**, including **ACEScg** to `sRGB` or `Rec.709`. Built with production-ready tools like **OpenImageIO**, **OpenColorIO**, and **NumPy**, it ensures high-quality conversions while maintaining speed and flexibility.

---

## 🛠️ Features

- 🔍 **Batch convert** folders of EXR sequences to JPGs  
- 🎨 Supports accurate **ACEScg → sRGB / Rec.709** color pipeline using OCIO  
- 📦 Optional support for RAW (linear Rec.709) input  
- 📁 Custom **input and output folder selection**  
- 🧠 **Automatic filename tagging** with color space info (e.g., `ACEScg_to_sRGB_shot01.jpg`)  
- ⚡ **Optimized buffer-based OCIO processing** for speed  
- 🧰 Built using:
  - [PySide6](https://doc.qt.io/qtforpython/)
  - [OpenImageIO](https://sites.google.com/site/openimageio/)
  - [OpenColorIO](https://opencolorio.org/)
  - [NumPy](https://numpy.org/)

---

## 🎛️ Color Workflow

Supports two input color spaces:
- **ACEScg** (transformed via OCIO using ACES 1.0.3 config)
- **RAW (Linear Rec.709)** (converted using gamma curves)

And two output transforms:
- **sRGB**
- **Rec.709**

If input is ACEScg, the tool uses the OCIO config for accurate tone mapping and display rendering.

---

## 🚀 Getting Started

### 📦 Install dependencies:

```bash
pip install PySide6 OpenImageIO PyOpenColorIO numpy
```

Make sure you have the **ACES 1.0.3 OCIO config** and update the path in the script:

```python
OCIO_CONFIG_PATH = "C:/ACES/aces_1.0.3/config.ocio"
```

### ▶️ Run the tool:

```bash
python Conversion_Tool_v004.py
```

---

## 🖼️ Screenshots

(Add some GUI screenshots here if you want!)

---

## 📂 Folder Structure

```
EXR_to_JPG_Converter/
├── Conversion_Tool_v004.py
├── README.md
└── assets/               # Optional screenshots, logos, etc.
```

---

## 📜 License
MIT License – free to use, modify, and share.

