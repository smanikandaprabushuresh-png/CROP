import os
import numpy as np
import pandas as pd

# Define realistic agronomic distributions for standard crops
# Each entry: (crop, N_range, P_range, K_range, temp_range, humidity_range, ph_range, rainfall_range)
crop_profiles = [
    ("Rice", (60, 100), (35, 60), (35, 45), (20.0, 27.5), (80.0, 85.0), (5.0, 7.5), (180.0, 300.0)),
    ("Maize", (60, 100), (35, 60), (15, 25), (18.0, 27.0), (55.0, 75.0), (5.5, 7.0), (60.0, 110.0)),
    ("Chickpea", (20, 60), (55, 80), (75, 85), (17.0, 21.0), (14.0, 20.0), (5.7, 8.8), (65.0, 95.0)),
    ("Kidneybeans", (15, 40), (55, 80), (15, 25), (15.0, 25.0), (18.0, 25.0), (5.5, 6.0), (60.0, 150.0)),
    ("Pigeonpeas", (15, 40), (55, 80), (15, 25), (25.0, 35.0), (30.0, 65.0), (4.5, 7.5), (90.0, 200.0)),
    ("Mothbeans", (15, 40), (35, 60), (15, 25), (24.0, 32.0), (40.0, 65.0), (3.5, 9.9), (30.0, 75.0)),
    ("Mungbean", (15, 40), (35, 60), (15, 25), (27.0, 30.0), (80.0, 90.0), (6.2, 7.2), (35.0, 60.0)),
    ("Blackgram", (35, 60), (55, 80), (15, 25), (25.0, 35.0), (60.0, 70.0), (6.5, 7.5), (60.0, 75.0)),
    ("Lentil", (15, 40), (55, 80), (15, 25), (18.0, 30.0), (60.0, 70.0), (5.9, 7.8), (35.0, 55.0)),
    ("Pomegranate", (15, 40), (10, 30), (35, 45), (18.0, 25.0), (85.0, 95.0), (5.5, 7.2), (100.0, 115.0)),
    ("Banana", (90, 120), (70, 95), (45, 55), (25.0, 30.0), (75.0, 85.0), (5.5, 6.5), (90.0, 120.0)),
    ("Mango", (15, 40), (15, 35), (25, 35), (27.0, 36.0), (45.0, 55.0), (4.5, 7.0), (85.0, 105.0)),
    ("Grapes", (15, 40), (120, 145), (195, 205), (8.0, 42.0), (80.0, 85.0), (5.5, 6.5), (65.0, 75.0)),
    ("Watermelon", (80, 120), (5, 30), (45, 55), (24.0, 27.0), (80.0, 90.0), (6.0, 7.0), (40.0, 60.0)),
    ("Muskmelon", (80, 120), (5, 30), (45, 55), (27.0, 30.0), (90.0, 95.0), (6.0, 6.8), (20.0, 30.0)),
    ("Apple", (15, 40), (120, 145), (195, 205), (21.0, 24.0), (90.0, 95.0), (5.5, 6.5), (100.0, 125.0)),
    ("Orange", (15, 40), (5, 30), (5, 15), (10.0, 35.0), (90.0, 95.0), (6.0, 8.0), (100.0, 120.0)),
    ("Papaya", (35, 75), (45, 70), (45, 55), (23.0, 44.0), (90.0, 95.0), (6.5, 7.0), (140.0, 250.0)),
    ("Coconut", (15, 40), (5, 30), (25, 35), (25.0, 29.0), (90.0, 99.0), (5.5, 6.5), (130.0, 230.0)),
    ("Cotton", (100, 140), (35, 60), (15, 25), (22.0, 26.0), (75.0, 85.0), (6.0, 8.0), (60.0, 100.0)),
    ("Jute", (60, 100), (35, 60), (35, 45), (23.0, 26.0), (75.0, 90.0), (6.0, 7.5), (150.0, 200.0)),
    ("Coffee", (80, 120), (15, 40), (25, 35), (23.0, 28.0), (50.0, 70.0), (6.0, 7.5), (115.0, 200.0))
]

np.random.seed(42)
records = []
samples_per_crop = 100

for crop, n_r, p_r, k_r, t_r, h_r, ph_r, r_r in crop_profiles:
    n_vals = np.random.uniform(n_r[0], n_r[1], samples_per_crop).round().astype(int)
    p_vals = np.random.uniform(p_r[0], p_r[1], samples_per_crop).round().astype(int)
    k_vals = np.random.uniform(k_r[0], k_r[1], samples_per_crop).round().astype(int)
    t_vals = np.random.uniform(t_r[0], t_r[1], samples_per_crop).round(2)
    h_vals = np.random.uniform(h_r[0], h_r[1], samples_per_crop).round(2)
    ph_vals = np.random.uniform(ph_r[0], ph_r[1], samples_per_crop).round(2)
    r_vals = np.random.uniform(r_r[0], r_r[1], samples_per_crop).round(2)
    
    for i in range(samples_per_crop):
        records.append({
            "N": n_vals[i],
            "P": p_vals[i],
            "K": k_vals[i],
            "temperature": t_vals[i],
            "humidity": h_vals[i],
            "ph": ph_vals[i],
            "rainfall": r_vals[i],
            "label": crop
        })

os.makedirs("dataset", exist_ok=True)
df = pd.DataFrame(records)
# Shuffle rows
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv("dataset/crop_data.csv", index=False)
print(f"Dataset created successfully with {len(df)} rows across {len(crop_profiles)} crops at dataset/crop_data.csv")
