# 🚀 ERENCP - Linux Dosya & Veritabanı Taşıma Aracı

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-Private-green)
![Platform](https://img.shields.io/badge/platform-linux-yellowgreen)

---

## 📌 Proje Hakkında

**ERENCP**, Linux sistemlerde uzaktaki bir sunucudan dosya ve MySQL veritabanı taşımanızı sağlayan,  
**komut satırı tabanlı, kolay ve otomatik çalışan** bir araçtır.

- Uzak sunucudaki dizinin **içeriğini zipler, indirir ve açar**.  
- İstersen MySQL veritabanını otomatik olarak **yedekler, indirir ve yerelde yeni veritabanı oluşturarak import eder**.  
- **SSH şifreli bağlantı (sshpass) destekli**.  
- Renkli ve kullanıcı dostu terminal arayüzü ile kolay kullanım.  
- Minimum bağımlılık ve hızlı kurulum.

---

## ⚙️ Özellikler

| Özellik                     | Açıklama                                         |
|----------------------------|-------------------------------------------------|
| Dosya taşıma               | Klasör içeriğini zipleyip, indirir ve açar      |
| Veritabanı taşıma          | Mysqldump ile dump alıp yerelde import eder      |
| SSH şifre desteği          | `sshpass` ile kolay şifreli bağlantı             |
| Otomatik bağımlılık kontrolü| Python3, sshpass, unzip yüklü değilse kurar    |
| Renkli ve interaktif arayüz| Kolay ve anlaşılır terminal soruları             |

---

## 🚀 Kurulum

```bash
git clone https://github.com/erenakkus/erencp.git
cd erencp
sudo bash install.sh
```  


---
##  🎯 Kullanım

```bash
erencp
```  
Sonrasında:

İstenilen bilgiler sorulacak (uzak sunucu IP, kullanıcı, şifre, dizin vs.)

Dosya ve veritabanı taşıma seçenekleri sunulacak

Veritabanı taşımak istemezsen hayır diyebilirsin

İşlem tamamlanınca başarılı mesajı alacaksın


---
## 💡 İpuçları
Python 3.6+ yüklü olmalı (install.sh otomatik kontrol eder)

sshpass ve unzip yoksa kurar

Taşınacak uzak dizin doğru yazılmalı (örnek: /var/www/html/site ya da /home/user/public_html)

Yerel hedef dizin yoksa script sorar, onay verirsen oluşturur

MySQL erişim bilgilerini doğru ver, yetki sorunlarına dikkat et

Dump dosyası /tmp/erencp_db.sql olarak geçici uzak sunucuda tutulur, işlem sonunda silinmez (istersen manuel temizle)

---

## 📜 Lisans
ErenCP - Lisans Dosyası

Telif Hakkı (c) 2025 Eren Akkuş

Bu yazılım ve kaynak kodları Eren Akkuş'a aittir.

- Kullanımı ve geliştirilmesi **ücretsizdir**.
- Yazılımın veya türevlerinin **satışı kesinlikle yasaktır**.
- Yazılımı kullanırken veya dağıtırken bu lisansın belirtilmesi zorunludur.

Her türlü sorunuz için geliştirici ile iletişime geçiniz.


---

## 🤝 Katkıda Bulunma
Projeye katkı yapmak, öneri veya hata bildirimi için GitHub üzerinden pull request açabilirsiniz.


---
## 📞 İletişim
github: erenakkus
mail: eren@erenakkus.tr
