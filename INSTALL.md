# 🚀 UzLingCorpus - Server O'rnatish Qo'llanmasi

## 📦 Barcha kutubxonalarni o'rnatish

### 1️⃣ Virtual environment yaratish
```bash
python -m venv uzlingcorpus_env
source uzlingcorpus_env/bin/activate  # Linux/Mac
# yoki
uzlingcorpus_env\Scripts\activate     # Windows
```

### 2️⃣ Barcha kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3️⃣ Database sozlash
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4️⃣ Superuser yaratish
```bash
python manage.py createsuperuser
```

### 5️⃣ Static fayllarni yig'ish
```bash
python manage.py collectstatic
```

### 6️⃣ Serverni ishga tushirish

**Development:**
```bash
python manage.py runserver
```

**Production (Gunicorn bilan):**
```bash
gunicorn --bind 0.0.0.0:8000 mysite.wsgi:application
```

## 🔧 Muhit o'zgaruvchilari (.env fayl)

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost:5432/uzlingcorpus
REDIS_URL=redis://localhost:6379/1
```

## 📋 Kutubxonalar ro'yxati

✅ **Asosiy:** Django, Pillow, PyPDF2, openpyxl
✅ **Admin:** django-jazzmin  
✅ **Database:** psycopg2-binary
✅ **Server:** gunicorn, whitenoise
✅ **Performance:** redis, django-redis
✅ **Security:** django-cors-headers
✅ **Development:** debug-toolbar, extensions
✅ **Testing:** pytest, coverage
✅ **Quality:** flake8, black, isort
✅ **Monitoring:** sentry-sdk

## 🎯 Bitta buyruq bilan hammasi:
```bash
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```