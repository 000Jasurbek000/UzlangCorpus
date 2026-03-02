# UzLingKorpus - O'zbek Tilshunosi

Modern O'zbek milliy mavzusidagi akademik korpus veb-sayti.

## ✨ Xususiyatlar

- 🎨 **Milliy dizayn** - O'zbek naqshlari va zamonaviy UI
- 📚 **Kutubxona bo'limi** - Kitoblar katalogi
- 🔍 **Konkordans qidiruv** - KWIC formatida natijalar
- 👨‍🏫 **Tarjimai hol** - Professor biografiyasi
- 📹 **Videomateriallar** - Ta'lim videolari
- ⏱️ **Timeline** - Muhim voqealar tarixi
- 📱 **Responsive** - Barcha qurilmalarda ishlaydi

## 🎨 Rang palitra

- **Turquoise**: #40E0D0 - Asosiy rang
- **Navy Blue**: #2D5F7F - Header va aksent
- **Gold**: #F4A460 - Ornament va badges
- **Sky Blue**: #87CEEB - Gradient
- **Emerald**: #50C878 - Aksent

## 🚀 Ishga tushirish

### 1. Virtual environment yaratish (ixtiyoriy)

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 3. Migratsiya

```bash
python manage.py migrate
```

### 4. Serverni ishga tushirish

```bash
python manage.py runserver
```

Brauzerni oching: **http://127.0.0.1:8000/**

## 📁 Loyiha strukturasi

```
UzLingCorpus/
├── mysite/              # Django asosiy sozlamalar
├── main/                # Asosiy app
│   ├── views.py        # View funksiyalari
│   └── urls.py         # URL routing
├── templates/           # HTML shablonlar
│   ├── index.html      # Bosh sahifa
│   ├── konkordans.html # Qidiruv sahifasi
│   └── tarjimai-hol.html # Biografiya
├── static/              # Statik fayllar
│   ├── css/
│   │   ├── style.css         # Asosiy CSS
│   │   ├── search.css        # Qidiruv CSS
│   │   └── biography.css     # Biografiya CSS
│   ├── js/
│   │   ├── main.js           # Asosiy JS
│   │   └── search.js         # Qidiruv JS
│   └── images/          # Rasmlar
├── requirements.txt     # Python kutubxonalari
└── README.md           # Bu fayl
```

## 🌐 Sahifalar

- **/** - Bosh sahifa
- **/konkordans/** - Konkordans qidiruv
- **/tarjimai-hol/** - Profesor biografiyasi

## 🛠️ Texnologiyalar

- **Backend**: Django 5.0+
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Shriftlar**: Merriweather (serif), Inter (sans-serif)
- **Ma'lumotlar bazasi**: SQLite (development)

## 📝 Keyingi qadamlar

1. **Ma'lumotlar bazasi** - Korpus uchun model yaratish
2. **API** - REST API (Django REST Framework)
3. **Qidiruv backend** - Haqiqiy korpus qidiruv funksiyasi
4. **Admin panel** - Kontent boshqaruvi
5. **Autentifikatsiya** - Foydalanuvchi tizimi
6. **Deploy** - Production serverga joylashtirish

## 👨‍💻 Ishlab chiquvchi

Django + Modern CSS dizayni

## 📄 Litsenziya

© 2024 UzLingKorpus. Barcha huquqlar himoyalangan.
