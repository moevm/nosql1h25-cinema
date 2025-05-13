document.addEventListener('DOMContentLoaded', async () => {
    const movieId = window.location.pathname.split('/')[2];
    if (!movieId) return redirectToHome();

    try {
        const movie = await loadMovieData(movieId);
        if (!movie) return redirectToHome();

        renderMoviePage(movie, movieId);

        // Инициализация рейтинга
        initRatingSystem(movieId);

    } catch (error) {
        console.error('Error:', error);
        redirectToHome();
    }
});

async function loadMovieData(movieId) {
    const response = await fetch(`/api/movies/${movieId}`);
    if (!response.ok) throw new Error('Failed to fetch movie');
    return await response.json();
}

function renderMoviePage(movie, movieId) {
    document.title = `${movie.title}`;

    // Постер и заголовок
    document.getElementById('moviePoster').src = movie.poster;
    document.getElementById('moviePoster').alt = movie.title;
    document.getElementById('movieTitleYear').textContent = `${movie.title} (${movie.year})`;

    // Рейтинг
    document.getElementById('movieRating').textContent =
        movie.avg_rating !== null && movie.avg_rating !== undefined
            ? movie.avg_rating.toFixed(1)
            : '—';

    // Продолжительность, описание, жанры, страна, бюджет
    document.getElementById('movieDuration').textContent = `${movie.duration} мин`;
    document.getElementById('movieDescription').textContent = movie.description;
    document.getElementById('movieGenres').textContent = movie.genres?.join(', ') || '—';
    document.getElementById('movieCountry').textContent = movie.country || '—';
    document.getElementById('movieBudget').textContent = movie.budget
        ? `${movie.budget.toLocaleString()} $`
        : '—';

    // Режиссёры
    document.getElementById('movieDirector').textContent =
        movie.directors?.map(d => d.name).join(', ') || '—';

    // Актёры
    const actorsElement = document.getElementById('movieActors');
    const viewAllLink = document.getElementById('viewAllActors');
    const displayedActors = movie.actors?.slice(0, 2) || [];
    actorsElement.textContent = displayedActors.map(a => a.name).join(', ') || '—';
    viewAllLink.textContent = 'Подробнее →';

    viewAllLink.addEventListener('mouseenter', () => {
        viewAllLink.style.textDecoration = 'underline';
        viewAllLink.style.color = '#023370';
    });
    viewAllLink.addEventListener('mouseleave', () => {
        viewAllLink.style.textDecoration = 'none';
        viewAllLink.style.color = '#d0ddff';
    });
    viewAllLink.addEventListener('click', () => {
        window.location.href = `/movie/${movieId}/persons`;
    });

    // Сериалы
    const seriesSelector = document.querySelector('.series-selector');
    const seriesSelect = document.getElementById('seriesSelect');

    if (movie.type === 'series' && Array.isArray(movie.episodes) && movie.episodes.length > 0) {
        seriesSelector.style.display = 'block';

        // Очистка предыдущих опций
        seriesSelect.innerHTML = '';

        // Заполнение опций
        movie.episodes.forEach((episode, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = `Сезон ${episode.season}, Серия ${episode.episode}: ${episode.title}`;
            seriesSelect.appendChild(option);
        });

        // Автоматическое воспроизведение первой серии
        const firstEpisode = movie.episodes[0];
        const videoElement = document.getElementById('movieVideo');
        videoElement.src = firstEpisode.url;

        // Обработчик изменения выбранной серии
        seriesSelect.addEventListener('change', (e) => {
            const selectedIndex = parseInt(e.target.value);
            const selectedEpisode = movie.episodes[selectedIndex];

            if (selectedEpisode) {
                videoElement.src = selectedEpisode.url;
                document.getElementById('movieTitleYear').textContent = 
                    `${movie.title} - Сезон ${selectedEpisode.season}, Серия ${selectedEpisode.episode}: ${selectedEpisode.title}`;
            }
        });

    } else {
        seriesSelector.style.display = 'none';
        // Видео
        const videoElement = document.getElementById('movieVideo');
        const placeholder = document.getElementById('videoPlaceholder');

        if (movie.video) {
            videoElement.src = movie.video;
            videoElement.classList.remove('hidden');
            placeholder.classList.add('hidden');
            videoElement.addEventListener('error', () => {
                videoElement.classList.add('hidden');
                placeholder.classList.remove('hidden');
            });
            videoElement.addEventListener('canplay', () => {
                videoElement.classList.remove('hidden');
                placeholder.classList.add('hidden');
            });
        } else {
            videoElement.classList.add('hidden');
            placeholder.classList.remove('hidden');
        }
    }

    // Даты создания и обновления
    const options = {
        timeZone: 'Europe/Moscow',
        dateStyle: 'short',
        timeStyle: 'short',
    };
    const createdDate = new Date(movie.created_at);
    const updatedDate = new Date(movie.updated_at);
    document.getElementById('movieCreatedAt').textContent =
        createdDate.toLocaleString('ru-RU', options);
    document.getElementById('movieUpdatedAt').textContent =
        updatedDate.toLocaleString('ru-RU', options);
}

function redirectToHome() {
    window.location.href = '/';
}

// функция для инициализации системы рейтинга
function initRatingSystem(movieId) {
    const ratingGroup = document.querySelector('.rating-group');
    const inputs = ratingGroup.querySelectorAll('input[name="fst"]');

    // Проверяем, есть ли сохраненная оценка в LocalStorage
    const savedRating = localStorage.getItem(`movieRating_${movieId}`);
    if (savedRating) {
        const savedInput = ratingGroup.querySelector(`#fst-${savedRating}`);
        if (savedInput) {
            savedInput.checked = true;
        }
    }

    // Добавляем обработчики событий для всех элементов рейтинга
    inputs.forEach(input => {
        input.addEventListener('change', async (e) => {
            if (e.target.value === '0') return; // Пропускаем значение по умолчанию

            const ratingValue = parseInt(e.target.value);

            try {
                // Отправляем оценку на сервер
                const response = await submitRating(movieId, ratingValue);

                if (response.success) {
                    // Сохраняем оценку в LocalStorage
                    localStorage.setItem(`movieRating_${movieId}`, ratingValue);

                    // Обновляем отображение среднего рейтинга
                    document.getElementById('movieRating').textContent =
                        response.newAvgRating.toFixed(1);

                    console.log('Рейтинг успешно сохранен');
                } else {
                    console.error('Ошибка при сохранении рейтинга:', response.message);
                }
            } catch (error) {
                console.error('Ошибка при отправке рейтинга:', error);
            }
        });
    });
}

// Функция для отправки рейтинга на сервер
async function submitRating(movieId, rating) {
    localStorage.setItem(`movieRating_${movieId}`, rating);
    try {
        const response = await fetch(`/api/films/${movieId}/rate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ rating })
        });

        if (!response.ok) {
            throw new Error('Ошибка сети');
        }

        return await response.json();
    } catch (error) {
        console.error('Ошибка отправки рейтинга:', error);
        throw error;
    }
}