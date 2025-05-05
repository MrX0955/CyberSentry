# CyberSentry - Gelişmiş Ağ İstihbarat Aracı

![Sürüm](https://img.shields.io/badge/sürüm-1.0.0-blue)
![Lisans](https://img.shields.io/badge/lisans-MIT-green)

CyberSentry (eski adıyla PySecurity), ağ güvenliği ve adli bilişim alanında çeşitli işlevler sunan komut satırı tabanlı bir siber güvenlik aracıdır. Güvenlik profesyonelleri, ağ yöneticileri ve siber güvenlik meraklıları için tasarlanmıştır.

## Özellikler

CyberSentry, modern ve kullanıcı dostu bir arayüz ile aşağıdaki özellikleri sunar:

### DNS İşlemleri
- **Ters DNS Araması:** IP adresine karşılık gelen domain adlarını sorgulama
- **DNS Sorgulama:** Domain adına karşılık gelen IP adreslerini sorgulama
- **Zone Transfer:** DNS bölge transferini test etme
- **DNS Host Kayıtları:** Domain için DNS host kayıtlarını listeleme
- **DNS Kayıtları:** Tüm DNS kayıtlarını görüntüleme
- **DNS Güvenlik Kontrolü:** DNSSEC doğrulaması yapma

### Ağ İşlemleri
- **IP Coğrafi Konum:** IP adresinin coğrafi konumunu tespit etme
- **Ters IP Sorgulama:** IP adresine bağlı domainleri listeleme
- **ASN Sorgulama:** Otonom Sistem Numarası bilgilerini sorgulama
- **Gizlilik API:** IP gizlilik bilgilerini kontrol etme
- **IPv6 Proxy Kontrolü:** IPv6 adreslerinin proxy olup olmadığını kontrol etme
- **Port Tarayıcı:** Hedef sistemde açık portları tarama

### Güvenlik Kontrolleri
- **Email Doğrulayıcı:** Email adreslerinin geçerliliğini kontrol etme
- **Veri Sızıntısı Kontrolü:** Email adresinin veri sızıntılarında yer alıp almadığını kontrol etme
- **DMARC Sorgulama:** Domain DMARC kayıtlarını kontrol etme
- **TLS Tarama:** TLS/SSL yapılandırmasını analiz etme
- **JS Güvenlik Tarayıcı:** JavaScript güvenlik sorunlarını kontrol etme
- **URL Bypasser:** Kısaltılmış URL'lerin gerçek hedeflerini tespit etme
- **SSL Sertifika Bilgisi:** SSL sertifikalarının detaylarını kontrol etme

### Ek Özellikler
- **Toplu Tarama:** Birden fazla hedefi tek seferde tarama
- **Zamanlanmış Görevler:** Taramaları belirli zaman aralıklarında otomatik olarak gerçekleştirme
- **Geçmiş:** Önceki taramaların sonuçlarını görüntüleme
- **Veri Dışa Aktarma:** Sonuçları HTML, JSON veya TXT formatında dışa aktarma
- **Güncellemeleri Kontrol Etme:** En son sürüm kontrolü

### Sistem Özellikleri
- Modern, ok tuşlarıyla gezinilebilen menü sistemi
- Çoklu dil desteği (İngilizce ve Türkçe)
- Tamamen özelleştirilebilir konfigürasyon sistemi
- HTML, JSON ve TXT formatlarında rapor oluşturma
- Eşzamanlı tarama desteği

## Kurulum

### Gereksinimler
- Python 3.6 veya üzeri

### Kurulum Adımları

1. Repo'yu klonlayın:
```
git clone https://github.com/raventrk/CyberSentry.git
cd CyberSentry
```

2. Gerekli kütüphaneleri yükleyin:
```
pip install -r config/requirements.txt
```

3. Uygulamayı başlatın:
```
python PySecurity.py
```

Windows kullanıcıları için `start.bat` dosyasını çalıştırarak da uygulamayı başlatabilirsiniz.

## Kullanım

Uygulama çalıştırıldığında, ok tuşları ve Enter tuşu ile menüde gezinebilirsiniz:

1. Ana menüden bir kategori seçin (DNS İşlemleri, Ağ İşlemleri, vb.)
2. Alt menüden istediğiniz işlevi seçin
3. İstenilen bilgileri girin (IP, domain, vb.)
4. Sonuçlarınızı görüntüleyin ve gerekirse raporlayın

### API Anahtarları

Bazı işlevler için API anahtarları gerekebilir:
- `hackertarget`
- `ipinfo`
- `hibp` (Have I Been Pwned)

Bu API anahtarlarını `config/config.json` dosyasında ilgili alanlara ekleyebilirsiniz.

## Konfigürasyon

`config/config.json` dosyası aracılığıyla aşağıdaki ayarları özelleştirebilirsiniz:

- Dil seçimi (en, tr)
- Rapor kaydetme seçenekleri
- Rapor formatı (HTML, JSON, TXT)
- Otomatik güncelleme kontrolü
- Eşzamanlı görev limiti
- İstek zaman aşımı süresi

## Desteklenen Diller

- İngilizce (English)
- Türkçe

Yeni dil eklemek için `config/languages.json` dosyasına çeviri ekleyebilirsiniz.

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## Katkıda Bulunanlar

- [GitHub Kullanıcı Adı](https://github.com/kullaniciadi)

## İletişim

Sorularınız veya geri bildirimleriniz için [e-posta adresi] adresine e-posta gönderebilirsiniz.

---

**Not**: CyberSentry (PySecurity) eğitim ve test amaçlı tasarlanmıştır. Kötü amaçlı kullanımdan veya yanlış kullanımdan doğabilecek sonuçlardan kullanıcı sorumludur. Her zaman yasal sınırlar içerisinde ve gerekli izinleri alarak kullanınız. 