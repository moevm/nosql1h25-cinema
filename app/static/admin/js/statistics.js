const ctx = document.getElementById('statsChart').getContext('2d');
let chart;
let currentData = [];
let allGenres = [];
let allCountries = [];

document.addEventListener('DOMContentLoaded', () => {
    initControls();
    loadInitialData();
    loadFilterOptions();
});

function initControls() {
    // Инициализация фильтров
    document.querySelector('.filter-button--apply').addEventListener('click', applyFilters);
    document.querySelector('.filter-button--clear').addEventListener('click', clearFilters);

    // Инициализация настроек графика
    document.getElementById('chartSettingsBtn').addEventListener('click', () => {
        document.getElementById('chartSettingsPanel').classList.toggle('hidden');
    });

    document.getElementById('applyChartSettings').addEventListener('click', updateChart);
}

async function loadInitialData() {
    try {
        const response = await fetch('/api/films');
        currentData = await response.json();
        updateChart();
    } catch (error) {
        console.error('Ошибка загрузки данных:', error);
    }
}

async function loadFilterOptions() {
    try {
        const filmsResponse = await fetch('/api/films');
        const films = await filmsResponse.json();

        const genresSet = new Set();
        films.forEach(film => {
            if (film.genres && Array.isArray(film.genres)) {
                film.genres.forEach(genre => genresSet.add(genre));
            }
        });
        allGenres = Array.from(genresSet).sort();

        const countriesSet = new Set();
        films.forEach(film => {
            if (film.country) {
                countriesSet.add(film.country);
            }
        });
        allCountries = Array.from(countriesSet).filter(Boolean).sort();

        const genreSelect = document.querySelector('.filter-select--genre');
        allGenres.forEach(genre => {
            const option = document.createElement('option');
            option.value = genre;
            option.textContent = genre;
            genreSelect.appendChild(option);
        });

        const countrySelect = document.querySelector('.filter-select--country');
        allCountries.forEach(country => {
            const option = document.createElement('option');
            option.value = country;
            option.textContent = country;
            countrySelect.appendChild(option);
        });

    } catch (error) {
        console.error('Ошибка загрузки опций фильтров:', error);
    }
}

async function applyFilters() {
    const filters = {
        genre: document.querySelector('.filter-select--genre').value,
        yearMin: document.querySelector('.filter-input--year-min').value,
        yearMax: document.querySelector('.filter-input--year-max').value,
        country: document.querySelector('.filter-select--country').value,
        ratingMin: document.querySelector('.filter-input--rating-min').value,
        ratingMax: document.querySelector('.filter-input--rating-max').value,
        director: document.querySelector('.filter-input--director').value,
        actor: document.querySelector('.filter-input--actor').value,
        durationMin: document.querySelector('.filter-input--duration-min').value,
        durationMax: document.querySelector('.filter-input--duration-max').value,
        budgetMin: document.querySelector('.filter-input--budget-min').value,
        budgetMax: document.querySelector('.filter-input--budget-max').value,
        addedMin: document.querySelector('.filter-input--added-min').value,
        addedMax: document.querySelector('.filter-input--added-max').value,
        editedMin: document.querySelector('.filter-input--edited-min').value,
        editedMax: document.querySelector('.filter-input--edited-max').value
    };

    Object.keys(filters).forEach(key => {
        if (filters[key] === '' || filters[key] === undefined) {
            delete filters[key];
        }
    });

    try {
        const response = await fetch('/api/films/filter', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(filters)
        });
        currentData = await response.json();
        updateChart();
    } catch (error) {
        console.error('Ошибка фильтрации:', error);
    }
}

function clearFilters() {
    document.querySelectorAll('.filter-select').forEach(select => {
        select.value = '';
    });
    document.querySelectorAll('.filter-input').forEach(input => {
        input.value = '';
    });

    loadInitialData();
}

function updateChart() {
    if (!currentData.length) {
        if (chart) chart.destroy();
        return;
    }

    const xAxis = document.getElementById('xAxis').value;
    const yAxis = document.getElementById('yAxis').value;
    const chartType = document.getElementById('chartType').value;

    const { labels, datasets } = prepareChartData(xAxis, yAxis);
    renderChart(labels, datasets, xAxis, yAxis, chartType);
}

function prepareChartData(xKey, yKey) {
    const groups = {};

    currentData.forEach(film => {
        // Обработка группировки по оси X
        let xValues = [];

        if (xKey === 'genres' && film.genres) {
            xValues = film.genres;
        } else if (xKey === 'year') {
            xValues = [film.year];
        } else if (xKey === 'country') {
            xValues = [film.country || 'Не указана'];
        } else if (xKey === 'directors') {
            xValues = film.directors.map(id => id.toString());
        } else if (xKey === 'actors') {
            xValues = film.actors.map(id => id.toString());
        } else {
            xValues = [film[xKey]];
        }

        xValues.forEach(xValue => {
            if (!xValue && xValue !== 0) return;

            if (!groups[xValue]) {
                groups[xValue] = { count: 0, ratingSum: 0, items: 0 };
            }

            groups[xValue].count++;

            if (film.ratings?.length) {
                const avgRating = film.ratings.reduce((sum, r) => sum + r, 0) / film.ratings.length;
                groups[xValue].ratingSum += avgRating;
                groups[xValue].items++;
            }
        });
    });

    const sortedGroups = Object.entries(groups).sort((a, b) => {
        if (xKey === 'year') return a[0] - b[0];
        if (xKey === 'country') return a[0].localeCompare(b[0]);
        if (xKey === 'genres') return a[0].localeCompare(b[0]);
        return a[1].count - b[1].count;
    });

    const labels = sortedGroups.map(item => item[0]);
    const data = sortedGroups.map(item => {
        switch(yKey) {
            case 'rating':
                return item[1].items > 0 ? item[1].ratingSum / item[1].items : 0;
            default:
                return item[1].count;
        }
    });

    return {
        labels,
        datasets: [{
            label: getAxisLabel(yKey),
            data,
            backgroundColor: labels.map((_, i) => getChartColor(i)),
            borderColor: labels.map((_, i) => getChartColor(i)),
            borderWidth: 1
        }]
    };
}

function renderChart(labels, datasets, xLabel, yLabel, chartType) {
    if (chart) chart.destroy();

    // Для круговой диаграммы используем только первый dataset
    const chartData = {
        labels,
        datasets: chartType === 'pie' ? [datasets[0]] : datasets
    };

    chart = new Chart(ctx, {
        type: chartType,
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: `Статистика фильмов по ${getAxisLabel(xLabel)}`
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (yLabel === 'rating') {
                                label += Math.round(context.raw * 10) / 10;
                            } else {
                                label += context.raw;
                            }
                            return label;
                        }
                    }
                }
            },
            scales: chartType !== 'pie' ? {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: getAxisLabel(yLabel)
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: getAxisLabel(xLabel)
                    }
                }
            } : {}
        }
    });
}

function getChartColor(index) {
    const colors = [
        '#002B5B', '#4CAF50', '#FF5722', '#607D8B', '#9C27B0',
        '#3F51B5', '#FF9800', '#795548', '#E91E63', '#00BCD4',
        '#8BC34A', '#CDDC39', '#673AB7', '#2196F3', '#F44336'
    ];
    return colors[index % colors.length];
}

function getAxisLabel(key) {
    const labels = {
        year: 'Год',
        country: 'Страна',
        genres: 'Жанр',
        count: 'Количество',
        rating: 'Средний рейтинг',
        directors: 'Режиссёр',
        actors: 'Актёр'
    };
    return labels[key] || key;
}