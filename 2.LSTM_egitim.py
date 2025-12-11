# lstm_5site.py
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Layer
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

print("VERİ OKUNUYOR...")
df = pd.read_csv("5G_90gun_5site_veri.csv", parse_dates=["datetime"])
print("VERİ OKUNDU:", len(df), "satır")


def train_lstm(site_name):
    print(f"EĞİTİM: {site_name}")
    data = df[df.site_id == site_name]["users"].values.reshape(-1, 1)
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(data)

    SEQ_LEN = 24
    X, y = [], []
    for i in range(SEQ_LEN, len(scaled) - 1):
        X.append(scaled[i - SEQ_LEN:i])
        y.append(scaled[i])
    X, y = np.array(X), np.array(y)

    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    class Attention(Layer):
        def __init__(self, **kwargs): super().__init__(**kwargs)

        def build(self, input_shape):
            self.W = self.add_weight(shape=(input_shape[-1], input_shape[-1]))
            self.V = self.add_weight(shape=(input_shape[-1], 1))

        def call(self, inputs):
            score = tf.nn.tanh(tf.tensordot(inputs, self.W, axes=1))
            attention = tf.nn.softmax(tf.tensordot(score, self.V, axes=1), axis=1)
            return tf.reduce_sum(attention * inputs, axis=1)

    inputs = Input(shape=(SEQ_LEN, 1))
    x = LSTM(64, return_sequences=True)(inputs)
    x = LSTM(32, return_sequences=True)(x)
    att = Attention()(x)
    out = Dense(1)(att)
    model = Model(inputs, out)
    model.compile(optimizer="adam", loss="mse")
    model.fit(X_train, y_train, epochs=30, validation_split=0.2, verbose=0)

    pred = model.predict(X_test, verbose=0)
    pred_inv = scaler.inverse_transform(pred)
    real_inv = scaler.inverse_transform(y_test.reshape(-1, 1))
    print(f"{site_name} TAMAM!")
    return real_inv[-168:], pred_inv[-168:]


results = {}
for site in df["site_id"].unique():
    real, pred = train_lstm(site)
    results[site] = (real, pred)

plt.figure(figsize=(16, 10))
for i, site in enumerate(results.keys(), 1):
    real, pred = results[site]
    plt.subplot(3, 2, i)
    plt.plot(real, label="Gerçek", marker="o", markersize=2)
    plt.plot(pred, label="Tahmin", marker="x", markersize=2)
    plt.title(f"{site} - Son 7 Gün")
    plt.ylabel("Kullanıcı")
    plt.legend()
    plt.grid(True)

plt.tight_layout()
plt.savefig("lstm_5site_sonuc.png", dpi=300)
plt.show()
print("GRAFİK HAZIR: lstm_5site_sonuc.png")

import pickle

with open("results.pkl", "wb") as f:
    pickle.dump(results, f)
print("LSTM sonuçları kaydedildi: results.pkl")
