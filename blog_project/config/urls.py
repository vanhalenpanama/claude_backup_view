from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # 루트 경로('')로 접속하면 바로 claude 앱으로 연결
    path('', include('claude.urls')), 
]

# 미디어 파일 서빙 설정 (개발 모드용)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from django.contrib import admin
# from django.urls import path, include
# # from django.contrib.auth import views as auth_views
# from django.contrib.auth.views import LogoutView
# from django.conf.urls.static import static
# from django.conf import settings



# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('blog.urls')),
#     path('claude/', include('claude.urls')),
#     path('account/', include('account.urls')),
#     # path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
#     path('logout/', LogoutView.as_view(), name='logout'),
# ]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)