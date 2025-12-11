import argparse
import pandas as pd
import numpy as np
import os

B_MIN_MHZ = 5
B_MAX_MHZ = 100
R_PER_USER = 2
P_BASE = 60
P_MIN = 5
ALPHA = 0.6
HYSTERESIS_MHZ = 5

def db2lin(db):
    return 10 ** (db / 10.0)

def needed_bw_mhz(users, snr_db):
    if users <= 0:
        return B_MIN_MHZ
    if np.isnan(snr_db):
        snr_db = 6.0
    snr_lin = db2lin(snr_db)
    total_rate = users * R_PER_USER * 1e6  # bps
    bw_hz = total_rate / np.log2(1 + snr_lin)
    bw_mhz = bw_hz / 1e6
    return max(B_MIN_MHZ, min(bw_mhz, B_MAX_MHZ))

def power_w(users, bw_mhz):
    if users <= 3:
        return P_MIN
    load = users / 500
    p = P_BASE * (bw_mhz / B_MAX_MHZ) * (1 + ALPHA * load)
    return round(max(P_MIN, min(p, P_BASE * 1.5)), 2)

def apply_hysteresis(prev_df, new_df):
    if prev_df is None:
        return new_df
    prev = prev_df.set_index(['datetime', 'site_id'])['assigned_B_MHz'].to_dict()
    def choose(row):
        key = (row['datetime'], row['site_id'])
        prev_b = prev.get(key)
        if prev_b is not None:
            if abs(prev_b - row['assigned_B_MHz']) < HYSTERESIS_MHZ:
                return prev_b
        return row['assigned_B_MHz']
    new_df = new_df.copy()
    new_df['assigned_B_MHz'] = new_df.apply(choose, axis=1)
    return new_df

def main():
    parser = argparse.ArgumentParser(description="LSTM → Frekans + Güç Atama")
    parser.add_argument('--input', default='preds.csv', help='Girdi: preds.csv')
    parser.add_argument('--prev', default='', help='Önceki schedule.csv (histerezis için)')
    parser.add_argument('--out', default='schedule.csv', help='Çıktı: schedule.csv')
    args = parser.parse_args()

    print(f"{args.input} OKUNUYOR...")
    df = pd.read_csv(args.input)
    df['datetime'] = pd.to_datetime(df['datetime'])

    print(f"Toplam {len(df)} satır, {df['site_id'].nunique()} site")

    # Gerekli bant
    df['req_B_MHz'] = df.apply(
        lambda r: needed_bw_mhz(r['pred_users'], r['est_snr_db']), axis=1
    )
    df['assigned_B_MHz'] = df['req_B_MHz']

    prev_df = None
    if args.prev and os.path.exists(args.prev):
        prev_df = pd.read_csv(args.prev)
        print(f"Önceki schedule yüklendi: {args.prev}")
    df = apply_hysteresis(prev_df, df)

    # Güç
    df['tx_power_W'] = df.apply(
        lambda r: power_w(r['pred_users'], r['assigned_B_MHz']), axis=1
    )

    # Not
    df['note'] = ''
    df.loc[df['pred_users'] <= 3, 'note'] = 'uyku modu'
    df.loc[df['assigned_B_MHz'] >= 90, 'note'] = 'yüksek yük'

    # Sonuç
    result = df[[
        'datetime', 'site_id', 'pred_users', 'est_snr_db',
        'assigned_B_MHz', 'tx_power_W', 'note'
    ]].copy()

    result.to_csv(args.out, index=False)
    print(f"{args.out} OLUŞTURULDU!")
    print(f"Ortalama bant: {result['assigned_B_MHz'].mean():.1f} MHz")
    print("\nİLK 5 SATIR:")
    print(result.head(5).to_string(index=False))

if __name__ == "__main__":
    main()