from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('zhanna-admin/', admin.site.urls),
    path('', include('main.urls')),
    # url('sberbank/', include('sberbank.urls'))

]
