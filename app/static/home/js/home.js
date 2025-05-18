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
    const prevButton = document.querySelector('.sheets__prev-button');
    const nextButton = document.querySelector('.sheets__next-button');

    let currentPage = 1;
    let itemsPerPage = 15;

    let currentFilms = [];
    const uniqueGenres = new Set();
    const uniqueCountries = new Set();
    
    loadContent('all');
    
    prevButton.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            renderPage(currentFilms);
        }
    });

    nextButton.addEventListener('click', () => {
        const maxPage = Math.ceil(currentFilms.length / itemsPerPage);
        if (currentPage < maxPage) {
            currentPage++;
            renderPage(currentFilms);
        }
    });

    // Обработчики для меню
    menuLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const href = link.getAttribute('href');

            clearFilters();
            
            // Обновление активной ссылки
            menuLinks.forEach(item => item.classList.remove('menu__link_active'));
            link.classList.add('menu__link_active');
            
            // Переключение между фильмами и сериалами
            if (link.textContent.trim() === 'Фильмы') {
                loadContent('films');
            } else if (link.textContent.trim() === 'Сериалы') {
                loadContent('series');
            } else if (href === "#") {
                loadContent('all');
            } else {
                window.location.href = href;
            }
        });
    });


    async function loadContent(type) {
        try {
            const response = await fetch(`/api/films?type=${type}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
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
            });

            currentPage = 1;
            renderPage(currentFilms);

            updateSelectOptions(genreSelect, uniqueGenres, genreTemplate);
            updateSelectOptions(countrySelect, uniqueCountries, countryTemplate);
        } catch (error) {
            console.error('Ошибка загрузки:', error);
            noResultsMessage.classList.remove('hidden');
            filmGrid.innerHTML = '';
        }
    }

    // Функция для отрисовки конкретной страницы
    function renderPage(films) {
        const start = (currentPage - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        const pageFilms = films.slice(start, end);

        filmGrid.innerHTML = '';
        noResultsMessage.classList.toggle('hidden', pageFilms.length !== 0);

        pageFilms.forEach(film => {
            const card = filmTemplate.content.cloneNode(true);
            const filmCard = card.querySelector('.film-card');

            card.querySelector('.film-poster').src = film.poster;
            card.querySelector('.film-poster').alt = film.title;

            filmCard.addEventListener('click', () => {
                const filmId = film._id?.$oid || film._id;
                if (filmId) window.location.href = `/movie/${filmId}`;
            });

            filmGrid.appendChild(card);
        });
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
    const descriptionInput = document.querySelector('.filter-form__input--description');
    const durationMinInput = document.querySelector('.filter-form__input--duration-min');
    const durationMaxInput = document.querySelector('.filter-form__input--duration-max');
    const budgetMinInput = document.querySelector('.filter-form__input--budget-min');
    const budgetMaxInput = document.querySelector('.filter-form__input--budget-max');
    const seriesTitleInput = document.querySelector('.filter-form__input--series-title');
    
    const applyFilterButton = document.querySelector('.filter-form__apply-button');

    applyFilterButton.addEventListener('click', async () => {
        const query = {
            genre: genreSelect.value || null,
            description: descriptionInput.value.trim(),
            seriesTitle: seriesTitleInput.value.trim(),
            country: countrySelect.value || null,
            director: directorInput.value.trim(),
            actor: actorInput.value.trim(),
            yearMin: yearMinInput.value.trim(),
            yearMax: yearMaxInput.value.trim(),
            ratingMin: ratingMinInput.value.trim() || 1,
            ratingMax: ratingMaxInput.value.trim() || 10,
            durationMin: durationMinInput.value.trim(),
            durationMax: durationMaxInput.value.trim(),
            budgetMin: budgetMinInput.value.trim(),
            budgetMax: budgetMaxInput.value.trim(),
            addedMin: addedMinInput.value.trim() || null,
            addedMax: addedMaxInput.value.trim() || null,
            editedMin: editedMinInput.value.trim() || null,
            editedMax: editedMaxInput.value.trim() || null,
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
        clearFilters();
        loadContent('all');
    });

    function clearFilters() {
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
        descriptionInput.value = '';
        durationMinInput.value = '';
        durationMaxInput.value = '';
        budgetMinInput.value = '';
        budgetMaxInput.value = '';
        seriesTitleInput.value = '';

        // Сброс сортировки
        sortRadios.forEach(radio => {
            radio.checked = false;
        });

        // Закрытие панелей фильтра и сортировки
        filterPanel.classList.add('hidden');
        sortingPanel.classList.add('hidden');
    }

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
        currentPage = 1;
        renderPage(sortedFilms);
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
