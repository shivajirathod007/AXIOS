<div align="center">

# AXIOS — NHA Hackathon · Problem Statement 3

**Document Forgery Detection Pipeline**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-CV2-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![Tesseract](https://img.shields.io/badge/OCR-Tesseract-DD0031?style=flat-square&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)
![Team](https://img.shields.io/badge/Team-KAAL-0f172a?style=flat-square)

*A robust, mathematically deterministic Computer Vision Hybrid Engine for detecting visible document tampering in medical claims — no cloud Vision APIs required.*

</div>

---

## &#x2139; Overview

This repository contains the KAAL Team's submission for **Problem Statement 3** of the NHA Hackathon. The objective is to detect visible document tampering in medical claims (images and PDFs), classify the type of forgery using predefined **Category IDs**, and output precise bounding box coordinates in **YAML format** alongside a **JSON summary**.

Our solution processes documents locally with high precision and rapid inference speeds, capable of scanning hundreds of pages and generating strictly compliant outputs.

---

## &#x2728; Key Features & Architecture

The pipeline processes documents sequentially through multiple specialized analysis tiers to detect various forms of manipulation.

---

### &#x1F50D; Tier 1 — Spatial OCR Engine (Tesseract)

| Property | Detail |
|---|---|
| **Targets** | `C2` Overwriting, `C7` Irregular Spacing |
| **Logic** | Analyzes text bounding boxes for physical intersection (IoU > 0.01) to catch sloppy copy-paste text injections. Calculates median line spacing and flags significant mathematical outliers to catch manual numerical edits. |

---

### &#x1F9E9; Tier 2 — Feature Matching (SIFT)

| Property | Detail |
|---|---|
| **Targets** | `C1` Copy-Paste (within same document) |
| **Logic** | Extracts keypoints and uses FLANN matching to find duplicated visual regions (e.g., a cloned signature). |

---

### &#x1F4CA; Tier 3 — Error Level Analysis (ELA)

| Property | Detail |
|---|---|
| **Targets** | `C4` Erased Text, `C3` Added Content, `C6` Watermark Removal |
| **Logic** | Identifies unnatural JPEG compression artifacts at the edges of digital edits using OpenCV contour detection. |

---

### &#x1F6E1; Tier 4 — Zero-Variance Masking (HSV & Grayscale)

| Property | Detail |
|---|---|
| **Targets** | `C4` Digital Redactions |
| **Logic** | Hunts for mathematically "flat" blocks of solid color (e.g., whiteout or black marker) used to obscure PII or dates, completely ignoring natural scanner noise. |

---

### &#x1F4CB; Tier 5 — Stitched Document Detection

| Property | Detail |
|---|---|
| **Targets** | `C5` Merging Documents |
| **Logic** | Compares median pixel intensity between the top and bottom halves of a page to detect poorly spliced images. |

---

## &#x1F4C4; Output Compliance

The pipeline strictly adheres to the hackathon guidelines:

- **JSON Summary** (`submission.json`) — Contains `link`, `file_name`, and `Category_ID` (joined by `||` and sorted by dominant manipulation area).
- **YAML Annotations** — Generated per-page (e.g., `abc_page_1.yaml`) containing precise `x`, `y`, `w`, `h` coordinates and category IDs.
- **Category Exclusion** — Pages strictly categorized as `C8` (Fully AI-generated) or `C10` (Clean) skip YAML generation entirely, as per the rules.
- **Metadata Integrity** — Correctly maps required `type` metadata (e.g., `erased` for C4, `text` for C3, `body` for C5).

---

## &#x1F527; Setup & Installation

### Prerequisites

- Python **3.10+** (developed on 3.13)
- **Tesseract OCR** installed on the host machine (must include English and Hindi language packs for optimal performance)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/shivajirathod007/AXIOS.git
cd AXIOS-main
```

**2. Create and activate a virtual environment** *(recommended)*

```bash
python -m venv .venv
source .venv/bin/activate        # On Windows use: .venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

> Required packages: `opencv-python-headless`, `pytesseract`, `numpy`, `PyYAML`, `PyMuPDF` (`fitz`), `Pillow`

---

## &#x25B6; Usage

**1. Prepare the dataset**

Place target claim documents (PDFs, JPGs, PNGs) into the input directory:

```
./Claim_Documents/
```

**2. Run the pipeline**

```bash
# Using the main script
python main.py

# Or run all cells in the provided Jupyter Notebook
```

**3. View results**

The pipeline will automatically:

- Wipe any previous outputs to prevent conflicts
- Render PDFs into individual page images
- Analyze every page through all five tiers
- Output `submission.json` and all `.yaml` files into:
  - `./outputs/`
  - `./outputs/annotations/`

---

## &#x1F4F6; Live Tracking

The pipeline features live console tracking, providing real-time feedback on:

- Processing queue status
- Predicted categories per page
- Bounding box counts
- YAML annotation targets

---

## &#x1F4C1; Repository Structure

```
.
├── Claim_Documents/          # Input directory for claim documents
├── outputs/
│   ├── submission.json       # Final JSON summary
│   └── annotations/          # Per-page YAML annotation files
├── main.py                   # Main pipeline entrypoint
├── nha_ps3_skeletal_notebook_main.ipynb
├── requirements.txt
└── README.md
```

---

<div align="center">

Created by **KAAL Team** &nbsp;·&nbsp; NHA Hackathon 2026

</div>
