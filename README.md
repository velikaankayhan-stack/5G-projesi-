- .gitignore — Depoya dahil edilmemesi gereken dosya/patternler.

- 1.Veri_seti_olusturma.py — Ham veri setini okur, temizler ve model eğitimi için ön işlenmiş veri oluşturur.

- 2.LSTM_egitim.py — Ön işlenmiş veri ile LSTM modeli eğitir ve ağırlıkları kaydeder.

- 3.MetriklerIleLSTMDogrulama.py — Model tahminleri üzerinden doğruluk ve performans metriklerini hesaplar.

- 4.GrafiklerIleLSTMDogrulama.py — Tahminler ve metrikler için görselleştirmeler üretir.

- 5.Modellerikullanımahazırhalegetirme.py — Eğitilmiş modelleri yükler ve inference için gerekli hazırlıkları yapar.

- 5G projesi yöntemler kısmı kodları — Yöntemler bölümüne ilişkin kısa/yardımcı kod veya not içeriği.

- 5G_90gun_5site_veri.csv — Ham ölçüm veri seti (90 gün, 5 site).

- 6.Algoritma.py — Projedeki ana algoritma ve iş akışını uygular.

- 7.ParazitAlgoritması.py — Parazit (interference) hesaplama ve simülasyon algoritmalarını uygular.

- lstm_5site_sonuc.png — LSTM sonuçlarının görselleştirmesi.

- lstm_dogruluk_metrikleri.csv — LSTM doğruluk/performans metriklerinin CSV çıktısı.

- lstm_metrics.png — Eğitim/validasyon kayıp ve performans eğrilerini gösteren görsel.

- ns3_baseline.csv — NS-3 simülasyonu temel (baseline) sonuç seti.

- ns3_optimized.csv — NS-3 simülasyonu optimize edilmiş senaryo sonuçları.

- parazit_algoritma.csv — Parazit algoritması çıktılarının özeti.

- parazit_schedule_ns3_senaryo2_agresif.csv — NS-3 için senaryo2/agresif parametreli parazit zamanlama dosyası.

- parazit_schedule_ns3_v2.csv — NS-3 için başka bir parazit zamanlama sürümü.

- preds.csv — Model tahminlerinin CSV kaydı.

- results.pkl — Eğitime/analize ait pickle formatında seri hale getirilmiş sonuç nesneleri.

- schedule.csv — Simülasyon/algoritma zamanlama girdisi veya çıktısı.