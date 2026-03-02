from django.contrib import admin
from .models import Maqola, Kitob, Shogird, Video, Fotogalereya, Xotira


@admin.register(Maqola)
class MaqolaAdmin(admin.ModelAdmin):
    list_display = ['tartib', 'title', 'author', 'category', 'journal', 'year', 'views', 'is_featured', 'created_at']
    list_filter = ['category', 'year', 'is_featured', 'created_at']
    search_fields = ['title', 'author', 'journal', 'keywords']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['tartib']
    list_display_links = ['title']
    readonly_fields = [
        'total_pages', 'total_words', 'total_characters', 
        'total_characters_no_spaces', 'total_sentences', 
        'total_paragraphs', 'unique_words', 'views', 'downloads',
        'created_at', 'updated_at'
    ]
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'category', 'author', 'journal', 'year', 'tartib')
        }),
        ('Fayllar', {
            'fields': ('pdf_file',)
        }),
        ('Avtomatik statistika (faqat ko\'rish)', {
            'classes': ('collapse',),
            'fields': (
                'total_pages', 'total_words', 'total_characters',
                'total_characters_no_spaces', 'total_sentences',
                'total_paragraphs', 'unique_words'
            ),
            'description': 'Bu ma\'lumotlar PDF yuklangandan keyin avtomatik hisoblanadi'
        }),
        ('Qo\'shimcha', {
            'fields': ('is_featured', 'views', 'downloads', 'created_at', 'updated_at')
        }),
    )


@admin.register(Kitob)
class KitobAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publisher', 'year', 'views', 'is_featured', 'created_at']
    list_filter = ['year', 'is_featured', 'created_at']
    search_fields = ['title', 'author', 'publisher', 'isbn']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = [
        'total_pages', 'total_words', 'total_characters',
        'total_characters_no_spaces', 'total_sentences',
        'total_paragraphs', 'unique_words', 'views', 'downloads',
        'created_at', 'updated_at'
    ]
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'author', 'publisher', 'year', 'isbn', 'edition')
        }),
        ('Tavsif', {
            'fields': ('description',)
        }),
        ('Fayllar', {
            'fields': ('pdf_file', 'cover_image')
        }),
        ('Avtomatik statistika (faqat ko\'rish)', {
            'classes': ('collapse',),
            'fields': (
                'total_pages', 'total_words', 'total_characters',
                'total_characters_no_spaces', 'total_sentences',
                'total_paragraphs', 'unique_words'
            ),
            'description': 'Bu ma\'lumotlar PDF yuklangandan keyin avtomatik hisoblanadi'
        }),
        ('Qo\'shimcha', {
            'fields': ('is_featured', 'views', 'downloads', 'created_at', 'updated_at')
        }),
    )


@admin.register(Shogird)
class ShogirdAdmin(admin.ModelAdmin):
    list_display = ['tartib', 'full_name', 'degree', 'defense_year', 'supervisor', 'views', 'created_at']
    list_filter = ['defense_year', 'degree', 'created_at']
    search_fields = ['full_name', 'dissertation_title', 'supervisor', 'specialty_name']
    prepopulated_fields = {'slug': ('full_name',)}
    list_editable = ['tartib']
    list_display_links = ['full_name']
    readonly_fields = ['views', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Shaxsiy ma\'lumotlar', {
            'fields': ('full_name', 'slug', 'photo', 'current_position', 'email', 'tartib')
        }),
        ('Dissertatsiya ma\'lumotlari', {
            'fields': (
                'dissertation_title', 'degree', 'specialty_code', 'specialty_name',
                'supervisor', 'defense_year', 'defense_organization'
            )
        }),
        ('Tavsif va yutuqlar', {
            'fields': ('abstract', 'achievements'),
            'description': 'Yutuqlar: Har bir yutuqni vergul bilan ajrating. Masalan: 15+ ilmiy maqola, 2 ta monografiya, O\'qituvchi-mentor'
        }),
        ('Fayllar', {
            'fields': ('pdf_file',),
            'description': 'Avtoreferat PDF faylini yuklash (ixtiyoriy, faqat yuklab olish uchun)'
        }),
        ('Qo\'shimcha', {
            'fields': ('views', 'created_at', 'updated_at')
        }),
    )


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published_date', 'views', 'is_featured', 'created_at']
    list_filter = ['category', 'is_featured', 'published_date', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'youtube_url', 'category', 'published_date')
        }),
        ('Tavsif', {
            'fields': ('description',)
        }),
        ('Qo\'shimcha', {
            'fields': ('is_featured', 'views', 'created_at', 'updated_at')
        }),
    )


@admin.register(Fotogalereya)
class FotogalereyaAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'views', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'date', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'image', 'date')
        }),
        ('Tavsif', {
            'fields': ('description',)
        }),
        ('Qo\'shimcha', {
            'fields': ('is_featured', 'views', 'created_at', 'updated_at')
        }),
    )


@admin.register(Xotira)
class XotiraAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'location', 'is_featured', 'views', 'created_at']
    list_filter = ['year', 'is_featured', 'created_at']
    search_fields = ['title', 'location', 'full_text', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'date', 'year', 'location')
        }),
        ('Rasm', {
            'fields': ('image',),
            'classes': ('collapse',),
        }),
        ('Matn', {
            'fields': ('full_text',),
            'description': 'HTML taglar ishlatish mumkin: <p>, <strong>, <em>, <br>'
        }),
        ('Teglar', {
            'fields': ('tags',),
            'description': 'Vergul bilan ajratib yozing. Masalan: ta\'lim, aspirantura, ma\'ruza'
        }),
        ('Qo\'shimcha', {
            'fields': ('is_featured', 'views', 'created_at', 'updated_at')
        }),
    )
