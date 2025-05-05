document.addEventListener('DOMContentLoaded', async () => {
    const movieId = window.location.pathname.split('/')[2];
    if (!movieId) return redirectToHome();

    try {
        const movie = await loadMovieData(movieId);
        if (!movie) return redirectToHome();

        renderMoviePage(movie);

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

function renderMoviePage(movie) {
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
    console.log("Рейтинг: ",movie.avg_rating)

// Продолжительность, описание, жанры, страна, бюджет
    document.getElementById('movieDuration').textContent = `${movie.duration} мин`;
    document.getElementById('movieDescription').textContent = movie.description;
    document.getElementById('movieGenres').textContent = movie.genres?.join(', ') || '—';
    document.getElementById('movieCountry').textContent = movie.country || '—';
    document.getElementById('movieBudget').textContent = movie.budget
        ? `${movie.budget.toLocaleString()} ₽`
        : '—';

// Режиссёры
    document.getElementById('movieDirector').textContent =
        movie.directors?.join(', ') || '—';

// Актёры (первые 2 + кнопка "Подробнее")
    const actorsElement = document.getElementById('movieActors');
    const viewAllLink = document.getElementById('viewAllActors');
    const displayedActors = movie.actors?.slice(0, 2) || [];

    actorsElement.textContent = displayedActors.join(', ') || '—';
    viewAllLink.style.display = 'inline';
    viewAllLink.textContent = 'Подробнее';
    viewAllLink.style.cursor = 'pointer';
    viewAllLink.addEventListener('click', () => {
        window.location.href = `/movie/${movie._id}/persons`;
    });

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
