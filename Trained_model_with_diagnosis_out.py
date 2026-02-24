import cv2
import torch
import numpy as np
import torch.nn as nn
import os

# ============================================================
# 1️⃣ DEFINE SSR MODEL (Same Architecture You Trained)
# ============================================================
class SSRNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 64, 3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, 3, padding=1)
        self.conv3 = nn.Conv2d(128, 64, 3, padding=1)
        self.conv4 = nn.Conv2d(64, 31, 3, padding=1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = self.relu(self.conv3(x))
        x = self.conv4(x)
        return x

# ============================================================
# 2️⃣ LOAD TRAINED SSR MODEL
# ============================================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = SSRNet().to(device)
model.load_state_dict(torch.load("ssr_model.pth", map_location=device))
model.eval()

print("✅ SSR Model Loaded")

# ============================================================
# 3️⃣ LOAD INPUT RGB IMAGE
# ============================================================
image_path = r"D:\DFU\TestSet\7a5e12fa15.jpg"   # <-- change to your test image
img = cv2.imread(image_path)

if img is None:
    raise Exception("❌ Image not found!")

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_norm = img_rgb.astype(np.float32) / 255.0

tensor = torch.from_numpy(img_norm).permute(2,0,1).unsqueeze(0).to(device)

# ============================================================
# 4️⃣ GENERATE HYPERSPECTRAL CUBE (31 Bands)
# ============================================================
with torch.no_grad():
    pred = model(tensor)

cube = pred.squeeze(0).cpu().numpy().transpose(1,2,0)
print("✅ Hyperspectral Cube Generated:", cube.shape)

# ============================================================
# 5️⃣ COMPUTE MEDICAL SPECTRAL INDICES
# ============================================================

# Hemoglobin Index (Blood Perfusion)
HbI = cube[:,:,14] - cube[:,:,10]

# Oxygenation Index
OI = cube[:,:,20] / (cube[:,:,10] + 1e-6)

# Tissue Degradation Index
TDI = cube[:,:,25] - cube[:,:,5]
# ============================================================
# 6️⃣ CREATE COMBINED DFU RISK MAP
# ============================================================

# ---- Normalize Each Biomarker ----
def normalize(x):
    return (x - np.min(x)) / (np.max(x) - np.min(x) + 1e-6)

HbI_n = normalize(HbI)
OI_n  = normalize(OI)
TDI_n = normalize(TDI)

# ---- DFU Risk Formula ----
# Higher risk if HbI low, OI low, TDI high
risk_map = (1 - HbI_n)*0.4 + (1 - OI_n)*0.4 + (TDI_n)*0.2

risk_map = normalize(risk_map)

# ============================================================
# 7️⃣ CONVERT TO MEDICAL COLOR MAP (Blue→Yellow→Red)
# ============================================================

risk_uint8 = (risk_map * 255).astype(np.uint8)

# Custom DFU colormap (Blue → Yellow → Red)
dfu_colormap = cv2.applyColorMap(risk_uint8, cv2.COLORMAP_JET)

# Overlay on original image for clinical interpretation
overlay = cv2.addWeighted(img, 0.6, dfu_colormap, 0.4, 0)

# ============================================================
# 8️⃣ SAVE FINAL DIAGNOSTIC IMAGE
# ============================================================
os.makedirs("dina_diagnosis_output", exist_ok=True)

cv2.imwrite("diagnosis_output/DFU_Risk_Map.png", dfu_colormap)
cv2.imwrite("diagnosis_output/DFU_Overlay.png", overlay)

print("✅ Combined DFU Diagnostic Map Saved")