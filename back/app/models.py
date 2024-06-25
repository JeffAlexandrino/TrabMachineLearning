import os
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.arima.model import ARIMA

def correct_anomalous_values(value):
    if isinstance(value, str):
        try:
            value = float(value)
        except ValueError:
            return np.nan
    if isinstance(value, (int, float)):
        if value > 100:
            return value / 1000
        return value
    return np.nan

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'GlobalLandTemperaturesByCountryV2.csv')

data = pd.read_csv(CSV_PATH)
data['dt'] = pd.to_datetime(data['dt'])

data_cleaned = data.dropna(subset=['AverageTemperature'])
data_cleaned['AverageTemperature'] = data_cleaned['AverageTemperature'].apply(correct_anomalous_values)
data_cleaned = data_cleaned.dropna(subset=['AverageTemperature'])
data_cleaned['Year'] = data_cleaned['dt'].dt.year
data_cleaned['Month'] = data_cleaned['dt'].dt.month

monthly_avg_temp = data_cleaned.groupby(['Country','Year', 'Month'])['AverageTemperature'].mean().reset_index()

p = range(0,3) # Ordem da parte auto-regressiva
d = range(0,2) # Ordem de diferenciação
q = range(0,3) # Ordem da média móvel
parameters = {'order': [(x, y, z) for x in p for y in d for z in q]}

def get_country_info(country_name, prediction_date):
    country_data = monthly_avg_temp[monthly_avg_temp['Country'] == country_name]

    train_data = country_data[country_data['Year'] <= 2000]['AverageTemperature']
    test_data = country_data[((country_data['Year'] > 2000) & (country_data['Year'] < 2013)) | ((country_data['Year'] == 2013) & (country_data['Month'] <= 9))]['AverageTemperature']

    best_mse = float('inf')
    best_order = None
    mae = None
    for order in parameters['order']:
        try:
            model = ARIMA(train_data, order=order)
            model_fit = model.fit()

            forecast = model_fit.forecast(steps=len(test_data))
            mse = mean_squared_error(test_data, forecast)

            if mse < best_mse:
                mae = mean_absolute_error(test_data, forecast)
                best_mse = mse
                best_order = order
        except Exception as e:
            #print(e)
            continue

    final_model = ARIMA(country_data['AverageTemperature'], order=best_order)
    final_model_fit = final_model.fit()

    months_diff = (pd.to_datetime(prediction_date).year - 2013) * 12 + pd.to_datetime(prediction_date).month - 9
    forecast_all = final_model_fit.forecast(steps=months_diff)

    return {
        'test_data': test_data,
        'rmse': float(np.sqrt(best_mse)),
        'mae': float(mae),
        'best_order': str(best_order),
        'forecast': forecast_all
    }
