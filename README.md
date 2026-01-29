Dosya İşlevleri

- .gitignore
  - Depoya dahil edilmemesi gereken dosya/pattern listesi (geçici/derleme/ortam dosyaları).

- 1.Veri_seti_olusturma.py
  - Ham veri setini okur, temizleme ve ön işlem adımlarını (zaman serisi pencerelendirme, normalizasyon vb.) uygular ve model eğitimi için kullanılacak ön işlenmiş veriyi oluşturur.

- 2.LSTM_egitim.py
  - Ön işlenmiş veriye LSTM tabanlı modeli uygular, eğitir ve eğitim çıktıları ile ağırlıkları kaydeder.

- 3.MetriklerIleLSTMDogrulama.py
  - Eğitilmiş modelin tahminleri üzerinden doğruluk ve diğer metrik hesaplamalarını yapar ve çıktı verir.

- 4.GrafiklerIleLSTMDogrulama.py
  - Model tahminleri ve metrikler için grafikler üretir (ör. eğitim/validasyon eğrileri, gerçek vs tahmin) ve görseller oluşturur.

- 5.Modellerikullanımahazırhalegetirme.py
  - Eğitilmiş modelleri yükleme ve inference için gerekli ön hazırlıkları sağlar (model ve scaler yükleme, pipeline).

- 5G projesi yöntemler kısmı kodları
  - Yöntemler bölümüne ilişkin kısa/yardımcı kod veya not içeriği (placeholder/ek açıklama dosyası).

- 5G_90gun_5site_veri.csv
  - Ham ölçüm veri seti (90 gün, 5 site). Projenin ana giriş verisi.

- 6.Algoritma.py
  - Proje kapsamında önerilen ana algoritmayı/iş akışını uygular (model çıktıları ve optimizasyon adımları).

- 7.ParazitAlgoritması.py
  - Parazit (interference) ile ilgili hesaplama ve simülasyon algoritmalarını uygular.

- lstm_5site_sonuc.png
  - LSTM modelinin 5 site için ürettiği sonuçların görselleştirmesi.

- lstm_dogruluk_metrikleri.csv
  - LSTM doğruluk/performans metriklerinin CSV çıktısı.

- lstm_metrics.png
  - Eğitim/validasyon kayıp ve performans metriklerinin görsel eğrileri.

- ns3_baseline.csv
  - NS-3 simülasyonu için elde edilmiş temel (baseline) sonuç seti.

- ns3_optimized.csv
  - NS-3 simülasyonu için optimize edilmiş senaryo sonuçları.

- parazit_algoritma.csv
  - Parazit algoritmasının çalışması sonucu üretilmiş özet/çıktılar.

- parazit_schedule_ns3_senaryo2_agresif.csv
  - NS-3 için hazırlanmış, senaryo2/agresif parametreli parazit zamanlama dosyası.

- parazit_schedule_ns3_v2.csv
  - NS-3 için hazırlanmış başka bir parazit schedule sürümü.

- preds.csv
  - Modelin ürettiği tahminlerin (predictions) CSV kaydı.

- results.pkl
  - Eğitime/analize ait seri hale getirilmiş (pickle) sonuç nesneleri.

- schedule.csv
  - Simülasyon/algoritma için kullanılan zamanlama/schedule girdisi veya çıktısı.


Not

Bu dosya yalnızca depodaki dosyaların kısa işlev açıklamalarını içerir. Daha ayrıntılı belgeleme veya dosya başlıkları için belirli bir dosyanın içeriğini inceleyebilirim.