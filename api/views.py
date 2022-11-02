from http.client import responses
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from api.serializers import *
from django.conf import settings
import requests
## Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


## User SignUp
class UserSignUpGenerics(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSignUpSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                context = {'status': True,'message': 'You have been registered successfully','data':serializer.data}
                return Response(context, status=status.HTTP_200_OK)
                
            context = {'status': False,'message': serializer.errors}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            context = {'status': False, 'message': {"error": ["Something went wrong."]}}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

## User Login Views.
class UserLoginGenerics(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                context = {'status': True,'message': 'Login Successfully','data':serializer.data}
                return Response(context, status=status.HTTP_200_OK)
                
            context = {'status': False,'message': serializer.errors}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            context = {'status': False, 'message': 'Something went wrong'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


### Search City Via Weather Report Get.
class UserSearchCityWeatherReport(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    search_city_param_config = openapi.Parameter('search_city',in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[search_city_param_config])
    def get(self, request, *args, **kwargs):
        try:
            city = self.request.query_params.get('search_city', None)
            if city is None:
                context = {'status': False,'message': 'Please enter city name',}
            else:
                loc_api = f"http://dataservice.accuweather.com/locations/v1/cities/IN/search?apikey={settings.ACCUWEATHER_KEY}&q={city}&details=true&offset=0"
                response = requests.get(loc_api)
                responses = response.json()
                if responses == []:
                    context = {'status': True,'message': 'No Record found','data':[]}
                else:
                    location_key = responses[0]['Key']
                    forecast_api = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}?apikey={settings.ACCUWEATHER_KEY}&details=true"
                    forecast_response = requests.get(forecast_api)
                    forecast_data = forecast_response.json()

                    # for key1 in forecast_data['DailyForecasts']:
                    #     print('Weather date'+key1['Date'])

                    ### Search forecast data store in db.
                    store_forecast = UserForecastStore()
                    store_forecast.user_id = request.user.id
                    store_forecast.search_city = city
                    store_forecast.search_data = forecast_data['DailyForecasts']
                    store_forecast.save()

                    context = {'status': True,'message': 'Record found Successfully','data':forecast_data['DailyForecasts']}
                    
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context = {'status': False, 'message': 'Something went wrong'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


### Search Location Based Forecast Data List.
class UserSearchLocBasedForecastDataList(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserForecastStoreSearializer

    def get(self, request, *args, **kwargs):
        try:
            listsearchdata = UserForecastStore.objects.all().order_by('created_on')
            serializer = self.serializer_class(listsearchdata, many=True)
            context = {'status': True,'message': 'Record found Successfully','data':serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context = {'status': False, 'message': 'Something went wrong'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)