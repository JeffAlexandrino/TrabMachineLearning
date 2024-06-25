// script.js

document.getElementById('weatherForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const country = document.getElementById('countrySelect').value;
    const date = document.getElementById('dateInput').value;
    getWeather(country, date);
});

function getWeather(country, date) {
    const apiKey = 'SUA_API_KEY_AQUI';  // Insira sua chave de API do OpenWeatherMap
    const city = getCityByCountry(country);
    const url = `https://api.openweathermap.org/data/2.5/forecast?q=${city}&units=metric&lang=pt_br&appid=${apiKey}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const weatherResult = document.getElementById('weatherResult');
            const forecast = data.list.find(item => item.dt_txt.startsWith(date));
            
            if (forecast) {
                weatherResult.innerHTML = `
                    <h2>${data.city.name}, ${data.city.country}</h2>
                    <p><strong>Data:</strong> ${forecast.dt_txt.split(' ')[0]}</p>
                    <p><strong>Temperatura:</strong> ${forecast.main.temp}°C</p>
                    <p><strong>Humidade:</strong> ${forecast.main.humidity}%</p>
                    <p><strong>Condições:</strong> ${forecast.weather[0].description}</p>
                `;
            } else {
                weatherResult.innerHTML = `<p>Não há dados disponíveis para a data selecionada.</p>`;
            }
        })
        .catch(error => {
            console.error('Erro ao obter os dados:', error);
            alert('Ocorreu um erro ao obter os dados. Por favor, tente novamente mais tarde.');
        });
}

function getCityByCountry(country) {
    const cities = {
        "Brazil": "Brasilia",
        "United States": "Washington",
        "Canada": "Ottawa",
        "United Kingdom": "London",
        "Australia": "Canberra"
    };
    return cities[country];
}
