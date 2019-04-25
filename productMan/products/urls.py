from django.conf.urls import url
from .views import GetAllSkuAPI, UserLoginAPI, SyncData, SaveAllData, SaveImage

urlpatterns = [
    url(r'^login/', UserLoginAPI.as_view(), name='user_login'),
    url(r'^get_all_skus/', GetAllSkuAPI.as_view()),
    url(r'^sync_data/', SyncData.as_view()),
    url(r'^save_all_data/', SaveAllData.as_view()),
    url(r'^save_image/', SaveImage.as_view()),

]
