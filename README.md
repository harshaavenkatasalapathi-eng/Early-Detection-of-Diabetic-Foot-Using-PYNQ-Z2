# Early-Detection-of-Diabetic-Foot-Using-PYNQ-Z2
FPGA-Based Spectral Super-Resolution of RGB Images for Early Detection of Diabetic Foot using PYNQ-Z2
## System Workflow

RGB Capture → Spectral Reconstruction → Band Selection → Spectral Analysis  
→ Tissue Classification → Risk Heatmap → Embedded Output

---

## Stage 1: RGB Image Acquisition (Camera Input)

Runs On: ARM Processor (PS) — Python + OpenCV  
Purpose: Capture visible image of the patient’s foot.

### Input
- Live USB camera image or stored RGB image.

### Processing
- Resize image to required model size (e.g., 224×224).
- Normalize pixel values to range 0–1.
- Convert image into tensor format for AI model.

### Output
Preprocessed RGB Image (224×224×3)

### Why This Stage?
Hyperspectral cameras are costly. This stage enables spectral simulation using a standard RGB camera.

---

## Stage 2: Spectral Super-Resolution (SSR Network)

Runs On: Initially PC for training, then accelerated on FPGA (PL).

Purpose: Convert RGB image into pseudo-hyperspectral cube.

### Input
RGB Image (H×W×3)

### Processing
- CNN model (SSRNet) reconstructs hidden spectral reflectance.
- Learns mapping from RGB to spectral domain.

RGB → 31 Spectral Bands

### Output
Spectral Cube (H×W×31)  
Example: 224×224×31 tensor

### Why Needed?
Diabetic tissue variations are visible in:
- Oxygen absorption characteristics
- Water content variation
- Hemoglobin reflectance

These features cannot be observed in RGB alone.

---

## Stage 3: FSFDA — Feature and Spectral Band Selection

Runs On: ARM Processor (Software Optimization)

Purpose: Remove redundant wavelengths and retain medically relevant spectral bands.

### Input
31-Band Spectral Cube

### Processing
- Analyze spectral importance.
- Select only diagnostically useful wavelengths.

Example:
31 Bands → Select 6 Critical Bands

### Output
Reduced Spectral Cube (H×W×6)

### Why This Stage?
Reduces:
- FPGA computation load
- Memory usage
- Power consumption

Enables efficient embedded implementation.

---

## Stage 4: Lightweight SpecTr (Spectral Attention Module)

Runs On: Hybrid (ARM + FPGA)

Purpose: Learn relationships between spectral bands.

### Input
Selected Spectral Bands (H×W×6)

### Processing
- Attention-based learning of spectral correlations.
- Identifies abnormal tissue characteristics such as:
  - Poor oxygenation
  - Infection onset
  - Tissue stress

### Output
Spectrally Enhanced Feature Map

### Why Needed?
Disease signatures are reflected in relationships between spectral bands rather than a single wavelength.

---

## Stage 5: DCCN Classification Network

Runs On: FPGA (PL Accelerator)

Purpose: Classify tissue condition.

### Input
Spectral Feature Tensor

### Processing
CNN classifier predicts:
- Normal
- At-Risk
- Ulcer Formation

Uses fixed-point arithmetic and parallel FPGA convolution.

### Output
Risk Probability Map (H×W×1)

---

## Stage 6: Risk Heatmap Generation

Runs On: ARM Processor (Visualization)

Purpose: Convert predictions into interpretable diagnostic output.

### Input
- Risk Probability Map
- Original RGB Image

### Processing
Overlay prediction heatmap using OpenCV.

Color Mapping:
- Green → Healthy Tissue
- Yellow → Early Risk
- Red → Critical Region

### Output
Final Diagnostic Image

---

## Stage 7: Embedded Deployment on PYNQ-Z2

The system runs fully on-board as a real-time edge AI device.

| Component | Runs On |
|----------|---------|
Camera Interface | ARM (PS)
SSR CNN | FPGA (PL)
Band Selection | ARM
Spectral Attention | Hybrid
DCCN Classifier | FPGA (PL)
Visualization | ARM

---

## Final Output
Real-time diabetic foot screening system providing early risk indication using FPGA-accelerated AI.

---

## Technologies Used
