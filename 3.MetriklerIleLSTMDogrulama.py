import pickle

with open("results.pkl", "rb") as f:
    results = pickle.load(f)
print("LSTM sonuçları yüklendi.")

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pandas as pd
import numpy as np

# LSTM çıktıları: results sözlüğü içinde
# results[site] = (real_values, predicted_values)

print("LSTM DOĞRULUK METRİKLERİ")
metrics = []

for site, (real, pred) in results.items():
    mae = mean_absolute_error(real, pred)
    rmse = np.sqrt(mean_squared_error(real, pred))
    r2 = r2_score(real, pred)
    metrics.append({
        "Site": site,
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "R²": round(r2, 4)
    })
    print(f"{site} → MAE: {mae:.2f}, RMSE: {rmse:.2f}, R²: {r2:.4f}")

# Tablo olarak kaydet
df_metrics = pd.DataFrame(metrics)
df_metrics.to_csv("lstm_dogruluk_metrikleri.csv", index=False)
print("Doğruluk tablosu kaydedildi: lstm_dogruluk_metrikleri.csv")