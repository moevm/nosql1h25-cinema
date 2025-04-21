document.addEventListener('DOMContentLoaded', () => {
    const filmGrid = document.getElementById('filmGrid');
    const filmTemplate = document.getElementById('filmTemplate');
    const menuLinks = document.querySelectorAll('.menu__link');
    const noResultsMessage = document.getElementById('noResultsMessage');
    const genreSelect = document.querySelector('.filter-form__select--genre');
    const countrySelect = document.querySelector('.filter-form__select--country');
    const genreTemplate = document.getElementById('genreOptionTemplate');
    const countryTemplate = document.getElementById('countryOptionTemplate');
    const sortRadios = document.querySelectorAll('.sort-form__input');

    let currentFilms = [];
    const uniqueGenres = new Set();
    const uniqueCountries = new Set();
    
    loadContent('all');
    
    // TODO: Добавить в бд параметр с типом (фильм или сериал)
    // Обработчики для меню
    menuLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const type = e.target.dataset.type;
            loadContent(type);
            
            // Обновление активной ссылки
            menuLinks.forEach(item => item.classList.remove('menu__link_active'));
            e.target.classList.add('menu__link_active');
        });
    });
    
    async function loadContent(type) {
        try {
            const response = await fetch(`/api/films?type=${type}`);
            currentFilms = await response.json();
            
            if (currentFilms.length === 0) {
                noResultsMessage.classList.remove('hidden');
            } else {
                filmGrid.innerHTML = '';
            }

            uniqueGenres.clear();
            uniqueCountries.clear();

            currentFilms.forEach(film => {
                if (film.genres) {
                    film.genres.forEach(genre => uniqueGenres.add(genre));
                }
                if (film.country) uniqueCountries.add(film.country);
                const card = filmTemplate.content.cloneNode(true);
                const filmCard = card.querySelector('.film-card');
                
                card.querySelector('.film-poster').src = film.poster;
                card.querySelector('.film-poster').alt = film.title;
                
                filmCard.addEventListener('click', () => {
                    window.location.href = `/movie/${film.id}`;
                });
                
                filmGrid.appendChild(card);
            });

            updateSelectOptions(genreSelect, uniqueGenres, genreTemplate);
            updateSelectOptions(countrySelect, uniqueCountries, countryTemplate);
        } catch (error) {
            console.error('Ошибка загрузки:', error);
        }
    }

    function updateSelectOptions(selectElement, itemsSet, template) {
        // Удалить все, кроме первого элемента ("Любой" / "Любая")
        while (selectElement.options.length > 1) {
            selectElement.remove(1);
        }
    
        itemsSet.forEach(item => {
            const option = template.content.cloneNode(true).querySelector('option');
            option.textContent = item;
            option.value = item;
            selectElement.appendChild(option);
        });
    };   

    // фильтры и сортировка
    const sortingBtn = document.querySelector('.sorting');
    const filterBtn = document.querySelector('.filter');
    const sortingPanel = document.getElementById('sortingPanel');
    const filterPanel = document.getElementById('filterPanel');

    sortingBtn.addEventListener('click', () => {
        sortingPanel.classList.toggle('hidden');
        filterPanel.classList.add('hidden');
    });

    filterBtn.addEventListener('click', () => {
        filterPanel.classList.toggle('hidden');
        sortingPanel.classList.add('hidden');
    });

    document.addEventListener('click', (e) => {
        const isClickInsideFilter = filterPanel.contains(e.target) || filterBtn.contains(e.target);
        const isClickInsideSorting = sortingPanel.contains(e.target) || sortingBtn.contains(e.target);
    
        if (!isClickInsideFilter) {
            filterPanel.classList.add('hidden');
        }
    
        if (!isClickInsideSorting) {
            sortingPanel.classList.add('hidden');
        }
    });

    // обработка фильтрации
    const directorInput = document.querySelector('.filter-form__input--director');
    const actorInput = document.querySelector('.filter-form__input--actor');
    const yearMinInput = document.querySelector('.filter-form__input--year-min');
    const yearMaxInput = document.querySelector('.filter-form__input--year-max');
    const ratingMinInput = document.querySelector('.filter-form__input_rating-min');
    const ratingMaxInput = document.querySelector('.filter-form__input_rating-max');
    const addedMinInput = document.querySelector('.filter-form__input--added-min');
    const addedMaxInput = document.querySelector('.filter-form__input--added-max');
    const editedMinInput = document.querySelector('.filter-form__input--edited-min');
    const editedMaxInput = document.querySelector('.filter-form__input--edited-max');
    
    const applyFilterButton = document.querySelector('.filter-form__apply-button');

    applyFilterButton.addEventListener('click', async () => {
        const query = {
            genre: genreSelect.value || null,
            country: countrySelect.value || null,
            director: directorInput.value.trim(),
            actor: actorInput.value.trim(),
            yearMin: yearMinInput.value.trim(),
            yearMax: yearMaxInput.value.trim(),
            ratingMin: ratingMinInput.value,
            ratingMax: ratingMaxInput.value,
            addedMin: addedMinInput.value,
            addedMax: addedMaxInput.value,
            editedMin: editedMinInput.value,
            editedMax: editedMaxInput.value
        };

        try {
            const response = await fetch('/api/films/filter', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(query)
            });

            currentFilms = await response.json();
            renderSortedFilms(currentFilms);
            filterPanel.classList.add('hidden');
        } catch (error) {
            console.error('Ошибка при применении фильтров:', error);
        }
    });

    const clearFilterButton = document.querySelector('.filter-form__clear-button');

    clearFilterButton.addEventListener('click', () => {
        // Сброс селектов
        genreSelect.selectedIndex = 0;
        countrySelect.selectedIndex = 0;

        // Сброс текстовых и других инпутов
        directorInput.value = '';
        actorInput.value = '';
        ratingMinInput.value = '';
        ratingMaxInput.value = '';
        yearMinInput.value = '';
        yearMaxInput.value = '';
        addedMinInput.value = '';
        addedMaxInput.value = '';
        editedMinInput.value = '';
        editedMaxInput.value = '';

        filterPanel.classList.add('hidden');
        loadContent('all');
    });

    // Функции сортировки
    function sortByPopularity(films) {
        return [...films].sort((a, b) => {
            const viewsA = a.views ? a.views.length : 0;
            const viewsB = b.views ? b.views.length : 0;
            return viewsB - viewsA;
        });
    }

    function sortByNewest(films) {
        return [...films].sort((a, b) => b.year - a.year); // Сортировка по убыванию года
    }

    function sortByRating(films) {
        return [...films].sort((a, b) => {
            const ratingA = a.ratings && a.ratings.length > 0 
                ? a.ratings.reduce((sum, r) => sum + r, 0) / a.ratings.length 
                : 0;
            const ratingB = b.ratings && b.ratings.length > 0 
                ? b.ratings.reduce((sum, r) => sum + r, 0) / b.ratings.length 
                : 0;
            return ratingB - ratingA;
        });
    }

    // Функция для отрисовки отсортированных фильмов
    function renderSortedFilms(sortedFilms) {
        if (!sortedFilms.length) {
            noResultsMessage.classList.add('hidden');
        }
        filmGrid.innerHTML = '';

        sortedFilms.forEach(film => {
            const card = filmTemplate.content.cloneNode(true);
            const filmCard = card.querySelector('.film-card');

            card.querySelector('.film-poster').src = film.poster;
            card.querySelector('.film-poster').alt = film.title;

            filmCard.addEventListener('click', () => {
                window.location.href = `/movie/${film.id}`;
            });

            filmGrid.appendChild(card);
        });
    }

    // Обработчик для кнопок сортировки
    sortRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            if (!currentFilms.length) return;

            let sortedFilms;
            switch(e.target.value) {
                case 'popular':
                    sortedFilms = sortByPopularity(currentFilms);
                    break;
                case 'new':
                    sortedFilms = sortByNewest(currentFilms);
                    break;
                case 'rating':
                    sortedFilms = sortByRating(currentFilms);
                    break;
                default:
                    sortedFilms = currentFilms;
            }
            
            renderSortedFilms(sortedFilms);
        });
    });

    // Поиск по названию фильма
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');

    async function searchFilms() {
        const title = searchInput.value.trim();

        // Если строка поиска пуста — показать все фильмы
        if (!title) {
            await loadContent('all');
            return;
        }

        try {
            const response = await fetch('/api/films/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title })
            });

            const films = await response.json();
            currentFilms = films;
            renderSortedFilms(currentFilms);
        } catch (error) {
            console.error('Ошибка при поиске фильмов:', error);
        }
    }

    searchButton.addEventListener('click', (e) => {
        e.preventDefault();
        searchFilms();
    });

    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            searchFilms();
        }
    });
});
