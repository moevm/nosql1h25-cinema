let allFilms = []; // Будем хранить все фильмы для фильтрации

// Инициализация фильтров
async function initFilters() {
    try {
        const response = await fetch('/api/films_filter');
        allFilms = await response.json();
        
        // Получаем уникальные значения
        const genres = [...new Set(allFilms.flatMap(f => f.genres))].filter(Boolean);
        const countries = [...new Set(allFilms.map(f => f.country))].filter(Boolean);

        fillSelect(genreFilter, genres);
        fillSelect(countryFilter, countries);
    } catch (error) {
        console.error('Ошибка инициализации фильтров:', error);
    }
}

function fillSelect(select, values) {
    values.sort().forEach(value => {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = value;
        select.appendChild(option);
    });
}

// Функция фильтрации
function applyFilters() {
    const genre = genreFilter.value;
    const country = countryFilter.value;
    const yearMinVal = parseInt(yearMin.value) || 1900;
    const yearMaxVal = parseInt(yearMax.value) || new Date().getFullYear();

    return allFilms.filter(film => {
        return (!genre || film.genres?.includes(genre)) &&
               (!country || film.country === country) &&
               film.year >= yearMinVal &&
               film.year <= yearMaxVal;
    });
}

// Обновленная функция отрисовки
function fetchDataAndRender() {
    const filteredData = applyFilters();
    const selectedKey = document.getElementById('keySelector').value;
    const counts = countByKey(filteredData, selectedKey);
    renderChart(counts, selectedKey);
}

// Обработчики событий
document.getElementById('applyFilters').addEventListener('click', fetchDataAndRender);
document.getElementById('clearFilters').addEventListener('click', () => {
    genreFilter.value = '';
    countryFilter.value = '';
    yearMin.value = '';
    yearMax.value = '';
    fetchDataAndRender();
});

// Инициализация
initFilters().then(fetchDataAndRender);