from django.contrib import admin
from django.urls import path
from scrape.views import get_html_response_indeed, get_job_title_and_location, get_results, get_starred

urlpatterns = [
    path('admin/', admin.site.urls),
    path('results/', get_results),
    path('starred/', get_starred),
    path('', get_job_title_and_location, name ='scrape-data'),
]
