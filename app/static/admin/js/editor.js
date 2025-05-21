let currentPage = 1;
const itemsPerPage = 5;
let totalPages = 0;
let editingFilmId = null;

document.addEventListener("DOMContentLoaded", function () {
    // Инициализация Tagify для полей
    const directorInput = document.querySelector("#director");
    const tagifyDirector = new Tagify(directorInput);
    const actorsInput = document.querySelector("#actors");
    const tagifyActors = new Tagify(actorsInput);

    // Загрузка фильмов при открытии страницы
    fetchFilms();

    // Элементы управления
    const addMovieBtn = document.getElementById("addMovieBtn");
    const modalOverlay = document.getElementById("add-new-film-modal");
    const cancelEditBtn = document.getElementById("new_cancel-edit");
    const saveBtn = document.getElementById("new_save-changes");
    const movieSearchInput = document.getElementById("movieSearch");

    // Открытие модального окна для добавления фильма
    addMovieBtn.addEventListener("click", function () {
        editingFilmId = null;
        openFilmModal(false);
    });

    // Закрытие модального окна
    cancelEditBtn.addEventListener("click", function () {
        modalOverlay.style.display = "none";
    });

    // Работа с выпадающим списком жанров
    const genreHeader = document.getElementById("genreHeader");
    const genreOptions = document.getElementById("genreOptions");

    genreHeader.addEventListener("click", function () {
        genreOptions.classList.toggle("hidden");
    });

    // Обработчик кликов по жанрам
    document.querySelectorAll(".genre-option").forEach(function (genreElement) {
        genreElement.addEventListener("click", function () {
            genreElement.classList.toggle("selected");
            updateSelectedGenres();
        });
    });

    // Обработчик изменения типа фильма (фильм/сериал)
    document.querySelectorAll('input[name="type"]').forEach(radio => {
        radio.addEventListener('change', function() {
            const episodesSection = document.getElementById('series-episodes');
            const videoUrlField = document.getElementById('video_url').closest('.form-flex');
            if (this.value === 'series') {
                episodesSection.style.display = 'block';
                videoUrlField.style.display = 'none';
            } else {
                episodesSection.style.display = 'none';
                videoUrlField.style.display = 'block';
                document.getElementById('episodes-container').innerHTML = '';
            }
        });
    });

    // Сохранение фильма
    saveBtn.addEventListener("click", async function (e) {
        e.preventDefault();
        await saveFilm();
    });

    // Поиск фильмов
    movieSearchInput.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            e.preventDefault();
            searchFilmsByTitle();
        }
    });

    movieSearchInput.addEventListener("input", function () {
        if (!movieSearchInput.value.trim()) {
            fetchFilms();
        }
    });

    // Очистка ошибок при вводе
    setupInputErrorHandlers();
});

// Функция для обновления скрытого поля с выбранными жанрами
function updateSelectedGenres() {
    const selectedGenres = [];
    document.querySelectorAll(".genre-option.selected").forEach(function (genreElement) {
        selectedGenres.push(genreElement.textContent.trim());
    });
    document.getElementById("selectedGenres").value = selectedGenres.join(", ");
}

// Настройка обработчиков ошибок
function setupInputErrorHandlers() {
    function clearErrorOnInput(inputId, errorId) {
        const input = document.getElementById(inputId);
        const error = document.getElementById(errorId);
        if (input && error) {
            input.addEventListener("input", () => {
                input.classList.remove("input-error");
                error.textContent = "";
            });
        }
    }

    clearErrorOnInput("new_film", "title-error");
    clearErrorOnInput("year", "year-error");
    clearErrorOnInput("director", "director-error");
    clearErrorOnInput("actors", "actors-error");
    clearErrorOnInput("country", "country-error");
    clearErrorOnInput("duration", "duration-error");
    clearErrorOnInput("budget", "budget-error");
    clearErrorOnInput("poster_url", "poster-url-error");
    clearErrorOnInput("video_url", "video-url-error");

    document.getElementById("genreHeader").addEventListener("click", () => {
        document.getElementById("genreHeader").classList.remove("input-error");
        document.getElementById("genres-error").textContent = "";
    });
}

// Загрузка фильмов
async function fetchFilms(page = 1) {
    currentPage = page;
    const spinner = document.getElementById("loadingSpinner");
    spinner.style.display = "block";

    try {
        const response = await fetch(`http://localhost:5000/api/content?page=${currentPage}&limit=${itemsPerPage}`);
        if (!response.ok) throw new Error("Ошибка загрузки фильмов");

        const data = await response.json();
        totalPages = Math.ceil(data.count / itemsPerPage);
        displayFilms(data.films);
        updatePaginationButtons();
    } catch (error) {
        console.error("Ошибка:", error);
        document.getElementById('films-container').innerHTML = '<p>Ошибка загрузки фильмов</p>';
    } finally {
        spinner.style.display = "none";
    }
}

// Отображение фильмов
function displayFilms(films) {
    const container = document.getElementById('films-container');
    container.innerHTML = films.length === 0 
        ? '<p>Фильмы не найдены</p>'
        : films.map(film => `
            <div class="film-card" data-id="${film._id}">
                <div class="film-header">
                    <p class="film-title-year">${film.title} (${film.year})</p>
                    <div class="film-actions">
                        <button class="btn btn-edit" onclick="editFilm('${film._id.$oid}')">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-delete" onclick="deleteFilm('${film._id.$oid}')" title="Удалить">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
}

// Обновление кнопок пагинации
function updatePaginationButtons() {
    const prevBtn = document.querySelector(".sheets__prev-button");
    const nextBtn = document.querySelector(".sheets__next-button");

    if (prevBtn && nextBtn) {
        prevBtn.disabled = currentPage === 1;
        nextBtn.disabled = currentPage === totalPages;

        prevBtn.onclick = () => currentPage > 1 && fetchFilms(currentPage - 1);
        nextBtn.onclick = () => currentPage < totalPages && fetchFilms(currentPage + 1);
    }
}

// Удаление фильма
async function deleteFilm(filmId) {
    if (!confirm("Вы уверены, что хотите удалить этот фильм?")) return;

    try {
        const response = await fetch(`http://localhost:5000/api/films/${filmId}`, {
            method: 'DELETE',
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message);
            fetchFilms();
        } else {
            alert(`Ошибка: ${result.error || "Неизвестная ошибка"}`);
        }
    } catch (error) {
        alert(`Ошибка запроса: ${error.message}`);
        console.error("Полная ошибка:", error);
    }
}

// Редактирование фильма
async function editFilm(filmId) {
    try {
        const response = await fetch(`http://localhost:5000/api/movies/${filmId}`);
        const filmData = await response.json();
        openFilmModal(true, filmData);
        editingFilmId = filmId;
    } catch (error) {
        console.error('Ошибка при загрузке данных фильма:', error);
        alert('Не удалось загрузить данные фильма');
    }
}

// Открытие модального окна
function openFilmModal(isEditMode, filmData = null) {
    const modalOverlay = document.getElementById("add-new-film-modal");
    const videoUrlField = document.getElementById('video_url').closest('.form-flex');
    const episodesSection = document.getElementById('series-episodes');
    
    // Сброс состояния формы
    clearFilmForm();
    document.querySelector('input[name="type"][value="movie"]').checked = true;
    episodesSection.style.display = 'none';
    videoUrlField.style.display = 'block';

    modalOverlay.style.display = "block";
    document.getElementById("new_save-changes").textContent = isEditMode ? "Сохранить изменения" : "Добавить фильм";

    if (isEditMode && filmData) {
        fillFilmForm(filmData);
    }
}

// Заполнение формы данными фильма
function fillFilmForm(filmData) {
    document.getElementById("new_film").value = filmData.title || "";
    document.getElementById("year").value = filmData.year || "";
    document.getElementById("director").value = (filmData.directors || []).map(d => d.name).join(", ");
    document.getElementById("actors").value = (filmData.actors || []).map(a => a.name).join(", ");
    document.getElementById("country").value = filmData.country || "";
    document.getElementById("duration").value = filmData.duration || "";
    document.getElementById("budget").value = filmData.budget || "";
    document.getElementById("description").value = filmData.description || "";
    document.getElementById("poster_url").value = filmData.poster_url || "";
    document.getElementById("video_url").value = filmData.video_url || "";

    // Жанры
    const selectedGenres = filmData.genres || [];
    document.getElementById("selectedGenres").value = selectedGenres.join(", ");
    document.querySelectorAll(".genre-option").forEach(el => {
        el.classList.toggle("selected", selectedGenres.includes(el.textContent.trim()));
    });

    // Тип (фильм/сериал) - исправленная часть
    const type = filmData.type || 'movie';
    const typeRadio = document.querySelector(`input[name="type"][value="${type}"]`);
    
    if (typeRadio) {
        typeRadio.checked = true;
        
        const episodesSection = document.getElementById('series-episodes');
        const videoUrlField = document.getElementById('video_url').closest('.form-flex');
        
        if (type === 'series') {
            episodesSection.style.display = 'block';
            videoUrlField.style.display = 'none';
            
            if (filmData.episodes?.length > 0) {
                document.getElementById('episodes-container').innerHTML = '';
                filmData.episodes.forEach((episode, index) => {
                    addEpisode(episode.season, episode.episode, episode.title, episode.url);
                });
            }
        } else {
            episodesSection.style.display = 'none';
            videoUrlField.style.display = 'block';
        }
    }
}

// Очистка формы
function clearFilmForm() {
    const formFields = [
        "new_film", "year", "country", "duration", "budget", 
        "description", "poster_url", "video_url", "selectedGenres"
    ];
    
    formFields.forEach(id => {
        const element = document.getElementById(id);
        if (element) element.value = "";
    });

    document.querySelectorAll(".genre-option.selected").forEach(el => {
        el.classList.remove("selected");
    });

    document.getElementById('episodes-container').innerHTML = '';
    editingFilmId = null;

    // Очистка ошибок
    document.querySelectorAll(".input-error").forEach(el => el.classList.remove("input-error"));
    document.querySelectorAll(".file-error").forEach(el => el.classList.remove("file-error"));
    document.querySelectorAll(".error").forEach(el => el.textContent = "");

    // Очистка Tagify
    const directorInput = document.querySelector("#director");
    if (directorInput?.tagify) directorInput.tagify.removeAllTags();
    
    const actorsInput = document.querySelector("#actors");
    if (actorsInput?.tagify) actorsInput.tagify.removeAllTags();
}

// Сохранение фильма
async function saveFilm() {
    const saveBtn = document.getElementById("new_save-changes");
    const originalText = saveBtn.textContent;
    saveBtn.textContent = editingFilmId ? "Сохранение..." : "Добавление...";
    saveBtn.disabled = true;

    try {
        const formData = collectFormData();
        const validationResult = validateFormData(formData);
        
        if (!validationResult.valid) {
            showValidationErrors(validationResult.errors);
            return;
        }

        const response = await sendFilmData(formData);
        const result = await response.json();

        if (response.ok) {
            alert(`Фильм успешно ${editingFilmId ? "обновлён" : "добавлен"}!`);
            document.getElementById("add-new-film-modal").style.display = "none";
            fetchFilms();
        } else {
            alert("Ошибка: " + (result.error || "Неизвестная ошибка"));
        }
    } catch (error) {
        console.error("Ошибка при сохранении:", error);
        alert("Произошла ошибка при отправке данных.");
    } finally {
        saveBtn.textContent = originalText;
        saveBtn.disabled = false;
    }
}

// Сбор данных формы
function collectFormData() {
    const type = document.querySelector('input[name="type"]:checked').value;
    const formData = new FormData();

    // Основные данные
    formData.append("title", document.getElementById("new_film").value.trim());
    formData.append("year", parseInt(document.getElementById("year").value));
    formData.append("country", document.getElementById("country").value.trim());
    formData.append("duration", parseInt(document.getElementById("duration").value));
    formData.append("budget", parseFloat(document.getElementById("budget").value));
    formData.append("description", document.getElementById("description").value.trim());
    formData.append("poster_url", document.getElementById("poster_url").value.trim());
    formData.append("type", type);

    // Жанры
    const genres = document.getElementById("selectedGenres").value
        .split(",")
        .map(g => g.trim())
        .filter(Boolean);
    formData.append("genres", JSON.stringify(genres));

    // Tagify поля
    const directorInput = document.querySelector("#director");
    const actorsInput = document.querySelector("#actors");
    
    if (directorInput?.tagify) {
        const directors = directorInput.tagify.value.map(tag => tag.value.trim()).filter(Boolean);
        formData.append("directors", JSON.stringify(directors));
    }

    if (actorsInput?.tagify) {
        const actors = actorsInput.tagify.value.map(tag => tag.value.trim()).filter(Boolean);
        formData.append("actors", JSON.stringify(actors));
    }

    // Для фильмов
    if (type === 'movie') {
        formData.append("video_url", document.getElementById("video_url").value.trim());
    }

    // Для сериалов
    if (type === 'series') {
        const episodes = [];
        document.querySelectorAll('.episode-form').forEach(form => {
            const season = form.querySelector('input[name*="[season]"]').value;
            const episode = form.querySelector('input[name*="[episode]"]').value;
            const title = form.querySelector('input[name*="[title]"]').value;
            const url = form.querySelector('input[name*="[url]"]').value;

            episodes.push({
                season: parseInt(season),
                episode: parseInt(episode),
                title: title.trim(),
                url: url.trim()
            });
        });
        formData.append("episodes", JSON.stringify(episodes));
    }

    return formData;
}

// Валидация данных формы
function validateFormData(formData) {
    const errors = {};
    let valid = true;

    // Проверка обязательных полей
    if (!formData.get("title")) {
        errors.title = "Введите название фильма";
        valid = false;
    }

    const year = parseInt(formData.get("year"));
    if (isNaN(year) || year < 1895 || year > new Date().getFullYear()) {
        errors.year = "Введите корректный год (1895-текущий год)";
        valid = false;
    }

    if (!formData.get("country")) {
        errors.country = "Введите страну";
        valid = false;
    }

    const duration = parseInt(formData.get("duration"));
    if (isNaN(duration) || duration <= 0) {
        errors.duration = "Введите корректную длительность";
        valid = false;
    }

    const budget = parseFloat(formData.get("budget"));
    if (isNaN(budget) || budget < 0) {
        errors.budget = "Введите корректный бюджет";
        valid = false;
    }

    const genres = JSON.parse(formData.get("genres"));
    if (genres.length === 0) {
        errors.genres = "Выберите хотя бы один жанр";
        valid = false;
    }

    const directors = JSON.parse(formData.get("directors"));
    if (directors.length === 0) {
        errors.director = "Введите режиссёра/ов";
        valid = false;
    }

    const actors = JSON.parse(formData.get("actors"));
    if (actors.length === 0) {
        errors.actors = "Введите актёра/ов";
        valid = false;
    }

    if (!editingFilmId) {
        if (!formData.get("poster_url")) {
            errors.poster_url = "Введите ссылку на постер";
            valid = false;
        }

        if (formData.get("type") === 'movie' && !formData.get("video_url")) {
            errors.video_url = "Введите ссылку на видео";
            valid = false;
        }

        if (formData.get("type") === 'series') {
            const episodes = JSON.parse(formData.get("episodes"));
            if (episodes.length === 0) {
                errors.episodes = "Добавьте хотя бы одну серию";
                valid = false;
            }
        }
    }

    return { valid, errors };
}

// Отображение ошибок валидации
function showValidationErrors(errors) {
    // Сначала очищаем все ошибки
    document.querySelectorAll(".input-error").forEach(el => el.classList.remove("input-error"));
    document.querySelectorAll(".error").forEach(el => el.textContent = "");

    // Показываем новые ошибки
    for (const [field, message] of Object.entries(errors)) {
        const errorElement = document.getElementById(`${field}-error`);
        const inputElement = document.getElementById(field) || 
                            document.querySelector(`[name="${field}"]`) ||
                            document.getElementById(field.replace('_', '-'));

        if (errorElement) errorElement.textContent = message;
        if (inputElement) inputElement.classList.add("input-error");
    }
}

// Отправка данных на сервер
async function sendFilmData(formData) {
    const url = editingFilmId 
        ? `http://localhost:5000/api/films/${editingFilmId}`
        : "http://localhost:5000/api/films/upload";

    return await fetch(url, {
        method: editingFilmId ? "PUT" : "POST",
        body: formData
    });
}

// Поиск фильмов
async function searchFilmsByTitle() {
    const query = document.getElementById("movieSearch").value.trim();
    if (!query) {
        fetchFilms();
        return;
    }

    try {
        const response = await fetch("http://localhost:5000/api/films/search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title: query })
        });

        if (response.ok) {
            const films = await response.json();
            displayFilms(films);
        } else {
            throw new Error("Ошибка при поиске");
        }
    } catch (error) {
        console.error("Ошибка поиска:", error);
        document.getElementById("films-container").innerHTML = "<p>Ошибка при поиске фильмов</p>";
    }
}

// Добавление серии
function addEpisode(season = "", episode = "", title = "", url = "") {
    const container = document.getElementById('episodes-container');
    const index = container.children.length;
    
    const div = document.createElement('div');
    div.classList.add('episode-form');
    div.innerHTML = `
        <div class="form-flex">
            <label>Сезон:</label>
            <input type="number" name="episodes[${index}][season]" value="${season}" required>
            <label>Эпизод:</label>
            <input type="number" name="episodes[${index}][episode]" value="${episode}" required>
        </div>
        <div class="form-flex">
            <label>Название серии:</label>
            <input type="text" name="episodes[${index}][title]" value="${title}" required>
        </div>
        <div class="form-flex">
            <label>Ссылка на видео:</label>
            <input type="text" name="episodes[${index}][url]" value="${url}" required>
        </div>
        <button type="button" class="remove-episode" onclick="this.closest('.episode-form').remove()">Удалить серию</button>
        <hr>
    `;
    container.appendChild(div);
}
