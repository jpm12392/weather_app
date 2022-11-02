from django.urls import path
from api.views import *



urlpatterns = [
    
    path('sign_up/', UserSignUpGenerics.as_view(),name='sign_up'),
    path('login/', UserLoginGenerics.as_view(),name='login'),
    path('locations/city/', UserSearchCityWeatherReport.as_view(),name='locations_city'),
    path('search_forecast_history/', UserSearchLocBasedForecastDataList.as_view(),name='search_forecast_history'),
]