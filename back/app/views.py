import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ForecastRequestSerializer
from .models import get_country_info

class ForecastView(APIView):
    def get(self, request, format=None):
        serializer = ForecastRequestSerializer(data=request.query_params)
        if serializer.is_valid():
            country = serializer.validated_data['country']
            prediction_date = serializer.validated_data['prediction_date']
            print('prediction_date', prediction_date)
            try:
                prediction = get_country_info(country, prediction_date)

                
                response = {
                    'prediction_temp': prediction['forecast'].tolist()[-1],
                    'prediction_date': prediction_date,
                    'prediciont_country': country,
                    'mae': prediction['mae'],
                    'rmse': prediction['rmse'],
                }
                return Response(response, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
