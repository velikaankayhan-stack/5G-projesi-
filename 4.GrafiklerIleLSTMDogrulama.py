import matplotlib.pyplot as plt

# Veriler
sites = ['Site_1', 'Site_2', 'Site_3', 'Site_4', 'Site_5']
mae = [35.26, 40.15, 35.12, 34.25, 31.65]
rmse = [44.62, 50.77, 44.5, 44.42, 41.08]
r2 = [0.8903, 0.8686, 0.8858, 0.8867, 0.9037]

# Stil ayarları
plt.style.use('seaborn-v0_8')
fig, axs = plt.subplots(3, 1, figsize=(10, 12))
metrics = [('MAE', mae), ('RMSE', rmse), ('R²', r2)]

for i, (label, values) in enumerate(metrics):
    axs[i].bar(sites, values, color='steelblue')
    axs[i].set_title(f'{label} Değerleri', fontsize=14)
    axs[i].set_ylabel(label)
    axs[i].set_xlabel('Baz İstasyonları')
    axs[i].grid(axis='y', linestyle='--', alpha=0.7)

    # Etiket ekleme
    for j, val in enumerate(values):
        axs[i].text(j, val + (0.5 if label != 'R²' else 0.001),
                    f'{val:.4f}' if label == 'R²' else f'{val:.2f}',
                    ha='center', va='bottom', fontsize=10)

    # R² için özel Y ekseni sınırı
    if label == 'R²':
        axs[i].set_ylim(0.85, 0.92)

plt.tight_layout()
plt.savefig("lstm_metrics.png", dpi=300)
plt.show()