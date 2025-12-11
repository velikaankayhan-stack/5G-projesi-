import math
import pandas as pd
import os

PARAZIT_ESIK = 3e-4
PARAZIT_KATSAYISI = 0.8
MIN_GUC = 5.0
MIN_BANT = 5.0
KAYDIRMA_ADIMI = 5.0
HISTERESIS_FARKI = 5.0

def bant_araligi(mhz_merkez, mhz_genislik):
    yarim = mhz_genislik / 2
    return mhz_merkez - yarim, mhz_merkez + yarim

def cakisma_orani(a_merkez, a_genislik, b_merkez, b_genislik):
    a0, a1 = bant_araligi(a_merkez, a_genislik)
    b0, b1 = bant_araligi(b_merkez, b_genislik)
    kesisim = max(0.0, min(a1, b1) - max(a0, b0))
    return kesisim / min(a_genislik, b_genislik)

def parazit_miktari(site1, site2):
    overlap = cakisma_orani(site1['freq'], site1['bw'], site2['freq'], site2['bw'])
    if overlap == 0.0:
        return 0.0
    num = site1['power'] * site2['power'] * overlap
    denom = site1['freq'] * site2['freq']
    return PARAZIT_KATSAYISI * num / denom

def oncelik(site1, site2):
    if site1['users'] != site2['users']:
        return site1 if site1['users'] < site2['users'] else site2
    return site1 if site1['snr'] < site2['snr'] else site2

def parazit_coz(site_dusuk, site_yuksek):
    eski_bw = site_dusuk['bw']
    eski_guc = site_dusuk['power']
    eski_freq = site_dusuk['freq']

    site_dusuk['bw'] = max(MIN_BANT, eski_bw * 0.9)
    if parazit_miktari(site_dusuk, site_yuksek) < PARAZIT_ESIK:
        return

    site_dusuk['power'] = max(MIN_GUC, eski_guc * 0.85)
    if parazit_miktari(site_dusuk, site_yuksek) < PARAZIT_ESIK:
        return

    if abs(site_dusuk['freq'] - site_yuksek['freq']) < HISTERESIS_FARKI:
        return

    for kayma in [-KAYDIRMA_ADIMI, KAYDIRMA_ADIMI]:
        site_dusuk['freq'] = eski_freq + kayma
        if parazit_miktari(site_dusuk, site_yuksek) < PARAZIT_ESIK:
            return

    site_dusuk['bw'] = eski_bw
    site_dusuk['power'] = eski_guc
    site_dusuk['freq'] = eski_freq

    __________

def parazit_onleyici(df):
    df = df.copy()
    df['freq_before'] = df['freq']
    df['bw_before'] = df['bw']
    df['power_before'] = df['power']
    df['parazit_before'] = 0.0
    df['parazit_after'] = 0.0

    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            s1 = df.iloc[i].copy()
            s2 = df.iloc[j].copy()
            interf_before = parazit_miktari(s1, s2)

            if interf_before > PARAZIT_ESIK:
                dusuk = oncelik(s1, s2)
                yuksek = s2 if dusuk['site_id'] != s1['site_id'] else s1
                parazit_coz(dusuk, yuksek)
                interf_after = parazit_miktari(dusuk, yuksek)

                df.loc[df['site_id'] == dusuk['site_id'], 'freq'] = dusuk['freq']
                df.loc[df['site_id'] == dusuk['site_id'], 'bw'] = dusuk['bw']
                df.loc[df['site_id'] == dusuk['site_id'], 'power'] = dusuk['power']
                df.loc[df['site_id'] == dusuk['site_id'], 'parazit_before'] = round(interf_before, 6)
                df.loc[df['site_id'] == dusuk['site_id'], 'parazit_after'] = round(interf_after, 6)
    return df

def demo_run_parazitli():
    sites = []
    center_freqs = [3440, 3445, 3450]
    for i in range(3):
        sites.append({
            'site_id': f'Site_{i+1}',
            'freq': center_freqs[i],
            'bw': 40.0,
            'power': 80.0,
            'users': 100 + i * 20,
            'snr': 15.0 - i
        })

    results = []
    for t in pd.date_range("2025-05-01 08:00:00", periods=3, freq="H"):
        df_t = pd.DataFrame(sites)
        df_t['datetime'] = t
        df_result = parazit_onleyici(df_t)
        results.append(df_result)

    full = pd.concat(results)
    full.to_csv("parazit_schedule_ns3_v2.csv", index=False)

    for _, row in full.iterrows():
        print(f"\n🟦 {row['site_id']} – {row['datetime']}")
        print("🔹 Müdahale Öncesi:")
        print(f"   Frekans: {row['freq_before']} MHz")
        print(f"   Bant Genişliği: {row['bw_before']} MHz")
        print(f"   Güç: {row['power_before']} Watt")
        print(f"   Parazit: {row['parazit_before']:.6f}")
        print("🔸 Müdahale Sonrası:")
        print(f"   Frekans: {row['freq']} MHz")
        print(f"   Bant Genişliği: {row['bw']} MHz")
        print(f"   Güç: {row['power']} Watt")
        print(f"   Parazit: {row['parazit_after']:.6f}")

    print("Dosya konumu:", os.path.abspath("parazit_schedule_ns3_v2.csv"))

def demo_run_parazitli_senaryo2_agresif():
    sites = []
    center_freqs = [3442, 3444, 3446]
    for i in range(3):
        sites.append({
            'site_id': f'Site_C{i+1}',
            'freq': center_freqs[i],
            'bw': 45.0,
            'power': 100.0,
            'users': 90 + i * 25,
            'snr': 10.0 - i
        })

    results = []
    for t in pd.date_range("2025-05-01 17:00:00", periods=3, freq="H"):
        df_t = pd.DataFrame(sites)
        df_t['datetime'] = t
        df_result = parazit_onleyici(df_t)
        results.append(df_result)

    full = pd.concat(results)
    full.to_csv("parazit_schedule_ns3_senaryo2_agresif.csv", index=False)

    for _, row in full.iterrows():
        print(f"\n🟦 {row['site_id']} – {row['datetime']}")
        print("🔹 Müdahale Öncesi:")
        print(f"   Frekans: {row['freq_before']} MHz")
        print(f"   Bant Genişliği: {row['bw_before']} MHz")
        print(f"   Güç: {row['power_before']} Watt")
        print(f"   Parazit: {row['parazit_before']:.6f}")
        print("🔸 Müdahale Sonrası:")
        print(f"   Frekans: {row['freq']} MHz")
        print(f"   Bant Genişliği: {row['bw']} MHz")
        print(f"   Güç: {row['power']} Watt")
        print(f"   Parazit: {row['parazit_after']:.6f}")

    print("Dosya konumu:", os.path.abspath("parazit_schedule_ns3_senaryo2_agresif.csv"))