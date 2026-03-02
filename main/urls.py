from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('konkordans/', views.konkordans, name='konkordans'),
    path('kengaytirilgan/', views.kengaytirilgan, name='kengaytirilgan'),
    path('tarjimai-hol/', views.tarjimai_hol, name='tarjimai_hol'),
    path('xotiralar/', views.xotiralar, name='xotiralar'),
    path('xotiralar/<int:id>/', views.xotira_detail, name='xotira_detail'),
    path('korpus/', views.korpus_haqida, name='korpus_haqida'),
    path('statistika/', views.statistika, name='statistika'),
    path('statistika/export/', views.statistika_export, name='statistika_export'),
    path('videolar/', views.videolar, name='videolar'),
    path('videolar/<int:id>/', views.video_detail, name='video_detail'),
    path('videolar/<int:id>/track/', views.video_track, name='video_track'),
    path('shogirdlar/', views.shogirdlar, name='shogirdlar'),
    path('shogirdlar/<int:id>/', views.shogird_detail, name='shogird_detail'),
    path('maqolalar/', views.maqolalar, name='maqolalar'),
    path('maqolalar/<int:id>/', views.maqola_detail, name='maqola_detail'),
    path('kitoblar/', views.kitoblar, name='kitoblar'),
    path('kitoblar/<int:id>/', views.kitob_detail, name='kitob_detail'),
    path('ustoz-haqida/', views.ustoz_haqida, name='ustoz_haqida'),
]
