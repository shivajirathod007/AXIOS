<div align="center">

# AXIOS — NHA Hackathon · Problem Statement 3

**Document Forgery Detection Pipeline**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-CV2-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![Tesseract](https://img.shields.io/badge/OCR-Tesseract-DD0031?style=flat-square&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)
![Team](https://img.shields.io/badge/Team-Chakravyuh-0f172a?style=flat-square)

*A robust, mathematically deterministic Computer Vision Hybrid Engine for detecting visible document tampering in medical claims — no cloud Vision APIs required.*

</div>

---

## &#x25A6; Overview

This repository contains the Chakravyuh Team's submission for **Problem Statement 3** of the NHA Hackathon. The objective is to detect visible document tampering in medical claims (images and PDFs), classify the type of forgery using predefined **Category IDs**, and output precise bounding box coordinates in **YAML format** alongside a **JSON summary**.

Our solution processes documents locally with high precision and rapid inference speeds, capable of scanning hundreds of pages and generating strictly compliant outputs.

---

## &#x25C6; Key Features & Architecture

The pipeline processes documents sequentially through multiple specialized analysis tiers to detect various forms of manipulation.

---

### &#x25B7; Tier 1 — Spatial OCR Engine (Tesseract)

| Property | Detail |
|---|---|
| **Targets** | `C2` Overwriting, `C7` Irregular Spacing |
| **Logic** | Analyzes text bounding boxes for physical intersection (IoU > 0.01) to catch sloppy copy-paste text injections. Calculates median line spacing and flags significant mathematical outliers to catch manual numerical edits. |

---

### &#x25B7; Tier 2 — Feature Matching (SIFT)

| Property | Detail |
|---|---|
| **Targets** | `C1` Copy-Paste (within same document) |
| **Logic** | Extracts keypoints and uses FLANN matching to find duplicated visual regions (e.g., a cloned signature). |

---

### &#x25B7; Tier 3 — Error Level Analysis (ELA)

| Property | Detail |
|---|---|
| **Targets** | `C4` Erased Text, `C3` Added Content, `C6` Watermark Removal |
| **Logic** | Identifies unnatural JPEG compression artifacts at the edges of digital edits using OpenCV contour detection. |

---

### &#x25B7; Tier 4 — Zero-Variance Masking (HSV & Grayscale)

| Property | Detail |
|---|---|
| **Targets** | `C4` Digital Redactions |
| **Logic** | Hunts for mathematically "flat" blocks of solid color (e.g., whiteout or black marker) used to obscure PII or dates, completely ignoring natural scanner noise. |

---

### &#x25B7; Tier 5 — Stitched Document Detection

| Property | Detail |
|---|---|
| **Targets** | `C5` Merging Documents |
| **Logic** | Compares median pixel intensity between the top and bottom halves of a page to detect poorly spliced images. |

---

## &#x25A0; Output Compliance

The pipeline strictly adheres to the hackathon guidelines:

- **JSON Summary** (`submission.json`) — Contains `link`, `file_name`, and `Category_ID` (joined by `||` and sorted by dominant manipulation area).
- **YAML Annotations** — Generated per-page (e.g., `abc_page_1.yaml`) containing precise `x`, `y`, `w`, `h` coordinates and category IDs.
- **Category Exclusion** — Pages strictly categorized as `C8` (Fully AI-generated) or `C10` (Clean) skip YAML generation entirely, as per the rules.
- **Metadata Integrity** — Correctly maps required `type` metadata (e.g., `erased` for C4, `text` for C3, `body` for C5).

---

## &#x25C6; Why This Architecture Wins — Engineering Rationale

Many deepfake and forgery detection systems rely on heavy Vision-Language Models (VLMs) or large-scale neural networks. The **AXIOS Computer Vision Hybrid Engine** was designed from the ground up to outperform those approaches within the strict constraints of the NHA Hackathon environment. Below is a precise account of our engineering decisions and why they translate to a dominant F1 score.

---

### &#x25AA; 1 — Zero-Shot Precision (No Hallucinations)

VLMs such as GPT-4V and Claude are notoriously unreliable at precise spatial mathematics. When prompted to generate `x, y, w, h` bounding box coordinates, they guess or hallucinate values that fail strict format validation.

Our pipeline uses **deterministic mathematical engines** — OpenCV contours, Tesseract bounding boxes, FLANN feature matching. If the pipeline outputs a bounding box for a `C4` redaction, it is because there is **mathematically zero pixel variance** in that exact grid location. This guarantees absolute adherence to the YAML coordinate syntax with no probabilistic error margins.

---

### &#x25AA; 2 — Built for Constrained Hardware (4 vCPU Optimized)

Heavy deep learning inference requires GPU acceleration to remain viable at scale. On a standard **4-core vCPU** cloud instance, pushing 800+ high-resolution medical documents through a VLM results in massive timeouts and out-of-memory crashes.

**The AXIOS solution:** We rely entirely on **highly optimized C++ binaries** running under the Python runtime — OpenCV, NumPy, PyTesseract. Our engine processes complex multi-page PDFs and high-resolution images in seconds, completely bypassing the need for GPU acceleration or paid API calls.

---

### &#x25AA; 3 — Aggressive False-Positive Reduction (F1 Score Optimization)

Medical documents are inherently noisy — scanned at irregular angles, filled with cursive handwriting, and rendered by inconsistent hospital software. A naive model will flag every cursive text overlap as a `C2` forgery. We invested significant effort in **threshold tuning** to maximize the F1 Score:

| Mechanism | Configuration | Purpose |
|---|---|---|
| **IoU Tuning** | Threshold raised to `> 0.15`, confidence `> 45` | Allows natural cursive handwriting without triggering false `C2` (Overwriting) flags |
| **Std. Dev. Multiplier** | `3.0x` against document median line spacing | Ignores natural human typing inconsistencies; flags only deliberate, malicious spacing anomalies (`C7`) |
| **Contour Area Floor** | Minimum `400 px²` for ELA detection | Prevents scanner dust and paper folds from being misclassified as `C3` (Added Content) |

---

### &#x25AA; 4 — Color-Agnostic Redaction Hunting

Real-world document scammers do not rely on a single tool. They use **whiteout**, **black bars**, **red WhatsApp markers**, and **grey PDF overlay boxes** to conceal Patient Identifiable Information (PII).

Instead of building fragile, color-specific masks, our **Zero-Variance Engine** calculates local pixel standard deviations via **Gaussian blur** and **Laplacian transformations**. It hunts for mathematically "flat" regions — catching `C4` redactions regardless of the color used — while fully ignoring the natural texture of scanned paper.

---

### &#x25AA; 5 — Multi-Layer Forgery Resolution with NMS

A single document may simultaneously be a stitched page (`C5`), contain erased text (`C4`), and carry a pasted signature (`C2`). Our orchestrator:

1. Runs all five analysis tiers **independently and in parallel**
2. Collects all candidate bounding boxes from each tier
3. Applies **Non-Maximum Suppression (NMS)** to intelligently merge overlapping regions
4. Sorts the final JSON output by **dominant manipulation area**, ensuring absolute compliance with the hackathon grading scripts

---

## ■ Setup & Installation

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
python main.py # but prefer running the cells

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

## &#x25A0; Live Tracking

The pipeline features live console tracking, providing real-time feedback on:

- Processing queue status
- Predicted categories per page
- Bounding box counts
- YAML annotation targets

---

## &#x25A0; Repository Structure

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

Created by **Chakravyuh Team** &nbsp;·&nbsp; NHA Hackathon 2026

</div>
