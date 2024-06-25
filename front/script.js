// script.js

document.getElementById('weatherForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const country = document.getElementById('countrySelect').value;
    const date = document.getElementById('dateInput').value;
    getWeather(country, date);
});

async function getWeather(country, prediction_date) {
    try{

        const url = `http://127.0.0.1:8000/api/forecast/?country=${country}&prediction_date=${prediction_date}`;
        console.log(url)
        const response = await fetch(url)

        const month_name = getMonthName(prediction_date)
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        const p1 = document.createElement('p');
        const p2 = document.createElement('p');

        p1.textContent = `A previsão de tempepatura média o para o mês de  ${month_name} em ${country} é de: ${data.prediction_temp.toFixed(2)}°C`;
        p2.textContent = `Com margem de erro de ${data.mae.toFixed(2)}°C`;
        document.querySelector('.container').appendChild(p1);
        document.querySelector('.container').appendChild(p2);
    } catch (error) {
        console.error('Erro ao obter os dados:', error);
    }

}

function getMonthName(dateString) {
    const date = new Date(dateString);

    const monthNames = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ];

    // Obtém o nome do mês correspondente
    return monthNames[date.getMonth()];
}


