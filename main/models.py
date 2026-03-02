import re
from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from .utils import extract_text_from_pdf, analyze_text, get_pdf_page_count
import os
import re


class Maqola(models.Model):
    """
    Ilmiy maqolalar modeli
    """
    # Kategoriya tanlovi
    CATEGORY_CHOICES = [
        ('uslubshunoslik', 'Uslubshunoslik va nutq madaniyati'),
        ('matn_lingvistikasi', 'Matn lingvistikasi'),
        ('alisher_navoiy', 'Alisher Navoiy ijodi'),
        ('fonetika', 'Fonetika va fonologiya'),
        ('sadriddin_ayniy', 'Sadriddin Ayniy maqolalari'),
        ('leksikologiya', 'Leksikologiya'),
        ('ustoz_haqida', 'Ustoz haqida (maxsus)'),
    ]
    
    # Asosiy ma'lumotlar
    title = models.CharField(
        max_length=500, 
        verbose_name="Maqola sarlavhasi",
        help_text="To'liq sarlavhani kiriting"
    )
    slug = models.SlugField(
        max_length=500, 
        unique=True, 
        blank=True,
        verbose_name="URL slug"
    )
    
    # Kategoriya
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='uslubshunoslik',
        verbose_name="Turkum",
        help_text="Maqola turkumini tanlang"
    )
    
    # Muallif va nashr ma'lumotlari
    author = models.CharField(
        max_length=200, 
        verbose_name="Muallif",
        help_text="Masalan: Prof. Anvar Mahmudov"
    )
    journal = models.CharField(
        max_length=300, 
        verbose_name="Manba",
        help_text="Qaysi jurnalda yoki nashrda chop etilgan"
    )
    year = models.IntegerField(
        verbose_name="Yil",
        help_text="Nashr yili (masalan: 2024)"
    )
    
    # Fayllar
    pdf_file = models.FileField(
        upload_to='documents/maqolalar/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        verbose_name="PDF fayl",
        help_text="Maqolaning to'liq matni (PDF formatda)"
    )
    
    # Avtomatik hisoblanadigan statistika
    total_pages = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="Sahifalar soni"
    )
    total_words = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="So'zlar soni"
    )
    total_characters = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="Belgilar soni"
    )
    total_characters_no_spaces = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="Belgilar (bo'sh joysiz)"
    )
    total_sentences = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="Gaplar soni"
    )
    total_paragraphs = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="Paragraflar soni"
    )
    unique_words = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="Noyob so'zlar soni"
    )
    
    # Qo'shimcha
    views = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="Ko'rishlar soni"
    )
    downloads = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="Yuklab olishlar soni"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Asosiy sahifada ko'rsatish"
    )
    tartib = models.IntegerField(
        default=0,
        verbose_name="Tartib raqami",
        help_text="Sahifada ko'rsatish tartibi (kichik raqam birinchi)"
    )
    
    # Vaqt
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan sana"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="O'zgartirilgan sana"
    )

    class Meta:
        verbose_name = "Maqola"
        verbose_name_plural = "Maqolalar"
        ordering = ['-year', '-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.year})"
    
    def save(self, *args, **kwargs):
        # Slug yaratish
        if not self.slug:
            self.slug = slugify(self.title[:100])
        
        # Faylni saqlash
        super().save(*args, **kwargs)
        
        # PDF tahlil qilish
        if self.pdf_file:
            self.analyze_pdf()
    
    def analyze_pdf(self):
        """
        PDF faylni tahlil qilish va statistikani yangilash
        """
        pdf_path = self.pdf_file.path
        
        # Sahifalar soni
        self.total_pages = get_pdf_page_count(pdf_path)
        
        # Matnni ajratish
        text = extract_text_from_pdf(pdf_path)
        
        # Tahlil qilish
        stats = analyze_text(text)
        
        # Statistikani saqlash
        self.total_words = stats['total_words']
        self.total_characters = stats['total_characters']
        self.total_characters_no_spaces = stats['total_characters_no_spaces']
        self.total_sentences = stats['total_sentences']
        self.total_paragraphs = stats['total_paragraphs']
        self.unique_words = stats['unique_words']
        
        # Qayta saqlash (recursive chaqiruvdan qochish uchun update ishlatamiz)
        Maqola.objects.filter(pk=self.pk).update(
            total_pages=self.total_pages,
            total_words=self.total_words,
            total_characters=self.total_characters,
            total_characters_no_spaces=self.total_characters_no_spaces,
            total_sentences=self.total_sentences,
            total_paragraphs=self.total_paragraphs,
            unique_words=self.unique_words
        )


class Kitob(models.Model):
    """
    Kitoblar modeli
    """
    # Asosiy ma'lumotlar
    title = models.CharField(
        max_length=500, 
        verbose_name="Kitob nomi",
        help_text="Kitobning to'liq nomi"
    )
    slug = models.SlugField(
        max_length=500, 
        unique=True, 
        blank=True,
        verbose_name="URL slug"
    )
    
    # Muallif va nashriyot
    author = models.CharField(
        max_length=200, 
        verbose_name="Muallif",
        help_text="Asosiy muallif yoki mualliflar"
    )
    publisher = models.CharField(
        max_length=300, 
        verbose_name="Nashriyot",
        help_text="Nashriyot nomi va joyi"
    )
    year = models.IntegerField(
        verbose_name="Nashr yili",
        help_text="Birinchi nashr yili"
    )
    isbn = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name="ISBN",
        help_text="Masalan: 978-5-12345-678-9"
    )
    edition = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Nashr (edition)",
        help_text="Masalan: 2-nashr, qayta ko'rilgan"
    )
    
    # Tavsif
    description = models.TextField(
        verbose_name="Tavsif",
        help_text="Kitob haqida to'liq ma'lumot"
    )
    
    # Fayllar
    pdf_file = models.FileField(
        upload_to='documents/kitoblar/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        verbose_name="PDF fayl",
        help_text="Kitobning to'liq matni (PDF formatda)"
    )
    cover_image = models.ImageField(
        upload_to='images/kitoblar/',
        verbose_name="Muqova rasmi",
        help_text="Kitob muqovasi (tavsiya: 600x800px)"
    )
    
    # Avtomatik statistika
    total_pages = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="Sahifalar soni"
    )
    total_words = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="So'zlar soni"
    )
    total_characters = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="Belgilar soni"
    )
    total_characters_no_spaces = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="Belgilar (bo'sh joysiz)"
    )
    total_sentences = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="Gaplar soni"
    )
    total_paragraphs = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="Paragraflar soni"
    )
    unique_words = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="Noyob so'zlar soni"
    )
    
    # Qo'shimcha
    views = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="Ko'rishlar soni"
    )
    downloads = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="Yuklab olishlar soni"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Asosiy sahifada ko'rsatish"
    )
    
    # Vaqt
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan sana"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="O'zgartirilgan sana"
    )
    
    class Meta:
        verbose_name = "Kitob"
        verbose_name_plural = "Kitoblar"
        ordering = ['-year', '-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.author}, {self.year})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title[:100])
        
        super().save(*args, **kwargs)
        
        if self.pdf_file:
            self.analyze_pdf()
    
    def analyze_pdf(self):
        """
        PDF faylni tahlil qilish
        """
        pdf_path = self.pdf_file.path
        
        self.total_pages = get_pdf_page_count(pdf_path)
        text = extract_text_from_pdf(pdf_path)
        stats = analyze_text(text)
        
        self.total_words = stats['total_words']
        self.total_characters = stats['total_characters']
        self.total_characters_no_spaces = stats['total_characters_no_spaces']
        self.total_sentences = stats['total_sentences']
        self.total_paragraphs = stats['total_paragraphs']
        self.unique_words = stats['unique_words']
        
        Kitob.objects.filter(pk=self.pk).update(
            total_pages=self.total_pages,
            total_words=self.total_words,
            total_characters=self.total_characters,
            total_characters_no_spaces=self.total_characters_no_spaces,
            total_sentences=self.total_sentences,
            total_paragraphs=self.total_paragraphs,
            unique_words=self.unique_words
        )


class Shogird(models.Model):
    """
    Shogirdlar (Dissertatsiyalar) modeli
    """
    # Shaxsiy ma'lumotlar
    full_name = models.CharField(
        max_length=200, 
        verbose_name="To'liq ismi",
        help_text="Masalan: Dr. Nodira Rahimova"
    )
    slug = models.SlugField(
        max_length=200, 
        unique=True, 
        blank=True,
        verbose_name="URL slug"
    )
    photo = models.ImageField(
        upload_to='images/shogirdlar/',
        blank=True, 
        null=True,
        verbose_name="Foto",
        help_text="Shogird fotosurati (400x400px tavsiya)"
    )
    
    # Dissertatsiya ma'lumotlari
    dissertation_title = models.CharField(
        max_length=500, 
        verbose_name="Dissertatsiya mavzusi",
        help_text="To'liq mavzu sarlavhasi"
    )
    degree = models.CharField(
        max_length=200, 
        verbose_name="Ilmiy daraja",
        help_text="Masalan: Filologiya fanlari nomzodi"
    )
    specialty_code = models.CharField(
        max_length=50, 
        verbose_name="Mutaxassislik kodi",
        help_text="Masalan: 10.02.01"
    )
    specialty_name = models.CharField(
        max_length=200, 
        verbose_name="Mutaxassislik nomi",
        help_text="Masalan: O'zbek tili"
    )
    
    # Ilmiy rahbar
    supervisor = models.CharField(
        max_length=200, 
        verbose_name="Ilmiy rahbar",
        help_text="Masalan: Prof. A. Mahmudov"
    )
    
    # Himoya ma'lumotlari
    defense_year = models.IntegerField(
        verbose_name="Himoya yili",
        help_text="Masalan: 2020"
    )
    defense_organization = models.CharField(
        max_length=300, 
        verbose_name="Himoya qilingan muassasa",
        help_text="To'liq nomi va joyi"
    )
    
    # Qisqacha ma'lumot
    abstract = models.TextField(
        verbose_name="Qisqacha tavsif",
        help_text="Dissertatsiya mavzusi haqida (3-5 gap)"
    )
    
    # Tartib
    tartib = models.IntegerField(
        default=0,
        verbose_name="Tartib raqami",
        help_text="Sahifada ko'rsatish tartibi (kichik raqam birinchi)"
    )
    
    # Yutuqlar (vergul bilan ajratilgan)
    achievements = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Asosiy yutuqlar",
        help_text="Har bir yutuqni vergul bilan ajrating. Masalan: 15+ ilmiy maqola, 2 ta monografiya, O'qituvchi-mentor"
    )
    
    # Fayllar
    pdf_file = models.FileField(
        upload_to='documents/dissertatsiyalar/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        blank=True, 
        null=True,
        verbose_name="Avtoreferat PDF",
        help_text="Dissertatsiya avtoreferati (ixtiyoriy)"
    )
    
    # Qo'shimcha
    current_position = models.CharField(
        max_length=300, 
        blank=True, 
        null=True,
        verbose_name="Hozirgi lavozimi",
        help_text="Masalan: Katta o'qituvchi, TDU"
    )
    email = models.EmailField(
        blank=True, 
        null=True,
        verbose_name="Email"
    )
    views = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="Ko'rishlar soni"
    )
    
    # Vaqt
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan sana"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="O'zgartirilgan sana"
    )
    
    class Meta:
        verbose_name = "Shogird"
        verbose_name_plural = "Shogirdlar"
        ordering = ['-defense_year', 'full_name']
    
    def __str__(self):
        return f"{self.full_name} ({self.defense_year})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)


class Video(models.Model):
    """
    Videomateriallar modeli
    """
    CATEGORY_CHOICES = [
        ('lectures', 'Ma\'ruzalar'),
        ('lessons', 'Darsliklar'),
        ('interviews', 'Suhbatlar'),
        ('ustoz_haqida', 'Ustoz haqida (maxsus)'),
    ]
    
    title = models.CharField(
        max_length=300, 
        verbose_name="Video nomi",
        help_text="Qisqa va tushunarli sarlavha"
    )
    slug = models.SlugField(
        max_length=300, 
        unique=True, 
        blank=True,
        verbose_name="URL slug"
    )
    
    # Video ma'lumotlari
    youtube_url = models.URLField(
        max_length=500,
        verbose_name="YouTube link",
        help_text="To'liq YouTube video linki. Masalan: https://www.youtube.com/watch?v=jNQXAC9IVRw"
    )
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='lectures',
        verbose_name="Turkum"
    )
    duration = models.CharField(
        max_length=20, 
        verbose_name="Davomiyligi",
        help_text="Masalan: 45:30"
    )
    
    # Tavsif
    description = models.TextField(
        verbose_name="Tavsif",
        help_text="Video haqida to'liq ma'lumot"
    )
    
    # Qo'shimcha
    published_date = models.DateField(
        verbose_name="Nashr sanasi",
        help_text="Video yuklangan sana"
    )
    views = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="Ko'rishlar soni"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Asosiy sahifada ko'rsatish"
    )
    
    # Vaqt
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan sana"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="O'zgartirilgan sana"
    )
    
    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videolar"
        ordering = ['-published_date', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title[:100])
        super().save(*args, **kwargs)
    
    

    def get_youtube_id(self):
        """
        YouTube linkdan video ID ni olish
        """
        url = self.youtube_url

        # youtu.be/ID
        match = re.search(r'youtu\.be/([^?&]+)', url)
        if match:
            return match.group(1)

        # youtube.com/watch?v=ID
        match = re.search(r'v=([^?&]+)', url)
        if match:
            return match.group(1)

        # youtube.com/embed/ID
        match = re.search(r'embed/([^?&]+)', url)
        if match:
            return match.group(1)

        return None

    @property
    def thumbnail_url(self):
        """
        YouTube thumbnail URL
        """
        video_id = self.get_youtube_id()
        if video_id:
            return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        return None


class Fotogalereya(models.Model):
    """
    Fotogalereya modeli
    """
    title = models.CharField(
        max_length=300, 
        verbose_name="Tadbir nomi",
        help_text="Masalan: Xalqaro tilshunoslik konferensiyasi"
    )
    slug = models.SlugField(
        max_length=300, 
        unique=True, 
        blank=True,
        verbose_name="URL slug"
    )
    
    # Rasm
    image = models.ImageField(
        upload_to='images/fotogalereya/',
        verbose_name="Rasm",
        help_text="Professional sifatli rasm (tavsiya: 1200x800px)"
    )
    
    # Ma'lumotlar
    date = models.DateField(
        verbose_name="Tadbir sanasi",
        help_text="Tadbir o'tkazilgan sana"
    )
    description = models.TextField(
        verbose_name="Tavsif",
        help_text="Tadbir haqida batafsil ma'lumot (3-5 gap)"
    )
    
    # Qo'shimcha
    views = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="Ko'rishlar soni"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Asosiy sahifada ko'rsatish"
    )
    
    # Vaqt
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan sana"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="O'zgartirilgan sana"
    )
    
    class Meta:
        verbose_name = "Foto"
        verbose_name_plural = "Fotogalereya"
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.date.year})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title[:100])
        super().save(*args, **kwargs)


class Xotira(models.Model):
    """
    Xotiralar modeli - shaxsiy xotiralar va voqealar
    """
    # Asosiy ma'lumotlar
    title = models.CharField(
        max_length=300, 
        verbose_name="Sarlavha",
        help_text="Qisqa va mazmunli sarlavha. Masalan: 'Birinchi ma'ruzam'"
    )
    slug = models.SlugField(
        max_length=300, 
        unique=True, 
        blank=True,
        verbose_name="URL slug"
    )
    
    # Sana va joy
    date = models.CharField(
        max_length=100,
        verbose_name="Sana",
        help_text="Masalan: '1982-yil 15-sentabr' yoki 'Kuz fasli, 1990-yil'"
    )
    year = models.IntegerField(
        verbose_name="Yil",
        help_text="Asosiy yil (tartibga solish uchun). Masalan: 1982"
    )
    location = models.CharField(
        max_length=200,
        verbose_name="Joy",
        help_text="Voqea sodir bo'lgan joy. Masalan: 'Toshkent Davlat Universiteti'"
    )
    
    # Rasm
    image = models.ImageField(
        upload_to='images/xotiralar/',
        blank=True,
        null=True,
        verbose_name="Rasm",
        help_text="Voqeaga oid rasm (1200x800px tavsiya). Ixtiyoriy"
    )
    
    # Matn
    full_text = models.TextField(
        verbose_name="To'liq matn",
        help_text="Xotira haqida batafsil hikoya. HTML taglar ishlatish mumkin (<p>, <strong>, <em>)"
    )
    
    # Teglar
    tags = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Teglar",
        help_text="Vergul bilan ajratib yozing. Masalan: ta'lim, aspirantura, ma'ruza, birinchi kun"
    )
    
    # Qo'shimcha
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Muhim xotira",
        help_text="Asosiy sahifada ko'rsatish uchun belgilash"
    )
    views = models.IntegerField(
        default=0, 
        editable=False,
        verbose_name="Ko'rishlar soni"
    )
    
    # Vaqt
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan sana"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="O'zgartirilgan sana"
    )
    
    class Meta:
        verbose_name = "Xotira"
        verbose_name_plural = "Xotiralar"
        ordering = ['-year', '-id']
    
    def __str__(self):
        return f"{self.title} ({self.year})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title[:100])
        super().save(*args, **kwargs)
    
    @property
    def short_text(self):
        """
        Qisqacha matn - birinchi 120 ta belgi
        """
        import re
        # HTML taglarni olib tashlash
        clean_text = re.sub(r'<[^>]+>', '', self.full_text)
        if len(clean_text) <= 120:
            return clean_text
        return clean_text[:120] + "..."
    
    @property
    def tag_list(self):
        """
        Teglarni ro'yxat ko'rinishida qaytarish
        """
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []

