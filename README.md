# Early-Detection-of-Diabetic-Foot-Using-PYNQ-Z2

##  Overview
This project presents a **low-cost, real-time system** for early detection of **Diabetic Foot Ulcers (DFU)** using standard RGB images.

A **CNN-based model** reconstructs multispectral information from RGB images and extracts biomedical features like:
- Haemoglobin (Hb)
- Oxygen Saturation (StO₂)
- Tissue Perfusion

The system is implemented on the **PYNQ-Z2 FPGA**, enabling fast and efficient edge-based medical analysis.

---

##  Objectives
- Convert RGB images into multispectral data using CNN
- Extract biomedical features (Hb, StO₂, Perfusion)
- Perform **zone-wise analysis** (Toe, Mid, Heel)
- Generate **risk heatmaps and clinical reports**
- Deploy on FPGA for **real-time processing**

---

##  Workflow

<img width="840" height="606" alt="image" src="https://github.com/user-attachments/assets/a5910285-332f-4042-af14-4fb0c8fdd5dd" />


---

##   System Architecture
- **Processing System (PS - ARM)**
  - Image acquisition
  - Preprocessing
  - Control

- **Programmable Logic (PL - FPGA)**
  - CNN Accelerator (SSRNet)
  - Spectral reconstruction

- **Communication**
  - AXI SmartConnect
  - M_AXI / S_AXI interfaces

<img width="1381" height="247" alt="image" src="https://github.com/user-attachments/assets/de82866a-adb9-4e8a-8c8b-555a560e1cf3" />


---

##  Hardware
- **Board**: PYNQ-Z2 (ZYNQ-7020)
- **Architecture**: ARM + FPGA (PS + PL)
- **Acceleration**: CNN implemented using HLS

---
 

##  Dataset
- **Primary**: Diabetic Foot Ulcer Dataset (Kaggle)
- **Additional**: DFU 2020 Challenge Dataset
 
##  Real Data Acquisition
- Device: **Micasense RedEdge-P Multispectral Camera**
- Used for capturing real multispectral reference data

---

## 🧪 Results
The system provides:
- ✅ Risk Heatmaps
- ✅ Zone-wise Analysis (Toe, Mid, Heel)
- ✅ Clinical Summary Reports

### Example
- Normal Foot → Low Risk  
- Ulcer Foot → High Risk (Clinical Attention Required)

---

## 🚀 Key Features
- Low-cost alternative to hyperspectral imaging
- Real-time FPGA-based processing
- Edge AI healthcare solution
- Explainable zone-wise risk analysis
- Automated clinical report generation

---

##  Conclusion
- Developed a complete end-to-end DFU detection system
- Implemented CNN-based spectral reconstruction on FPGA
- Achieved real-time biomedical analysis
- Validated using datasets and real-world data

---

##  Future Work
- Improve model accuracy with larger datasets
- Add mobile/web dashboard
- Real-time camera integration
- Deploy as a portable healthcare device

---

##  Authors
- Harshaa V  
- Dasarath B  
- Dinakarvel B  
- Janvi Kanakan  
- Sivaguru K  
