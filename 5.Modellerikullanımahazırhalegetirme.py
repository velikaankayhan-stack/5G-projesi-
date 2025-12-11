# preds.py
import pickle
import pandas as pd
import numpy as np

# 1. results.pkl'den verileri yükle
with open("results.pkl", "rb") as f:
    results = pickle.load(f)

print(f"SONUÇLAR YÜKLENDİ: {len(results)} site")

rows = []
for site, (real, pred) in results.items():
    for i, val in enumerate(pred[-168:]):  # son 7 gün (168 saat)
        hour = i % 24
        day = (i // 24) + 1

        # Gerçekçi SNR hesaplama: Kullanıcı arttıkça SNR düşer
        pred_users = int(np.round(val[0]))
        est_snr_db = max(10, 30 - 0.02 * pred_users + np.random.normal(0, 1.5))

        rows.append({
            "datetime": f"2025-04-{day:02d} {hour:02d}:00:00",
            "site_id": site,
            "pred_users": pred_users,
            "est_snr_db": round(est_snr_db, 2)
        })

df = pd.DataFrame(rows)
df.to_csv("preds.csv", index=False)
print("preds.csv OLUŞTURULDU!")
print(f"Toplam {len(df)} satır, {df['site_id'].nunique()} site")