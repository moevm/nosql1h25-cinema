document.addEventListener("DOMContentLoaded", function () {
    fetchFilms();

    // Обработчик клика по кнопке "Добавить фильм"
    const addMovieBtn = document.getElementById("addMovieBtn");
    const modalOverlay = document.getElementById("add-new-film-modal");
    const cancelEditBtn = document.getElementById("new_cancel-edit");

    // Открытие модального окна
    addMovieBtn.addEventListener("click", function () {
        // modalOverlay.style.display = "block";
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
        console.log("Клик по заголовку жанров");
        genreOptions.classList.toggle("hidden"); 
    });

    // Обработчик кликов по жанрам
    const genreElements = document.querySelectorAll(".genre-option");
    genreElements.forEach(function (genreElement) {
        genreElement.addEventListener("click", function () {
            genreElement.classList.toggle("selected");
            updateSelectedGenres();
        });
    });

    const saveBtn = document.getElementById("new_save-changes");

    saveBtn.addEventListener("click", async function (e) {
        e.preventDefault();

        const title = document.getElementById("new_film").value.trim();
        const year = parseInt(document.getElementById("year").value);
        const directorsRaw = document.getElementById("director").value.trim();
        const actorsRaw = document.getElementById("actors").value.trim();
        const country = document.getElementById("country").value.trim();
        const duration = parseInt(document.getElementById("duration").value);
        const budget = parseFloat(document.getElementById("budget").value);
        const description = document.getElementById("description").value.trim();
        const genres = document.getElementById("selectedGenres").value
            .split(",")
            .map(g => g.trim())
            .filter(Boolean);
        const posterFile = document.getElementById("poster").files[0];
        const videoFile = document.getElementById("video").files[0];

        // Валидация
        let valid = true;

        document.querySelectorAll(".input-error").forEach((el) => el.classList.remove("input-error"));
        document.querySelectorAll(".file-error").forEach((el) => el.classList.remove("file-error"));


        if (!title) {
            valid = false;
            document.getElementById("title-error").textContent = "Введите название фильма";
            document.getElementById("new_film").classList.add("input-error");
        }

        if (!year || year < 1895 || year > new Date().getFullYear()) {
            valid = false;
            document.getElementById("year-error").textContent = "Введите корректный год фильма (1895- текущий год)";
            document.getElementById("year").classList.add("input-error");
        }

        if (!directorsRaw) {
            valid = false;
            document.getElementById("director-error").textContent = "Введите режиссёра/ов";
            document.getElementById("director").classList.add("input-error");
        }

        if (!actorsRaw) {
            valid = false;
            document.getElementById("actors-error").textContent = "Введите актёра/ов";
            document.getElementById("actors").classList.add("input-error");
        }

        if (!country) {
            valid = false;
            document.getElementById("country-error").textContent = "Введите страну";
            document.getElementById("country").classList.add("input-error");
        }

        if (genres.length === 0) {
            valid = false;
            document.getElementById("genres-error").textContent = "Выберите хотя бы один жанр";
            document.getElementById("genreHeader").classList.add("input-error");
        }

        if (isNaN(duration) || duration <= 0) {
            valid = false;
            document.getElementById("duration-error").textContent = "Введите корректную длительность фильма в минутах";
            document.getElementById("duration").classList.add("input-error");
        }

        if (isNaN(budget) || budget < 0) {
            valid = false;
            document.getElementById("budget-error").textContent = "Введите бюджет";
            document.getElementById("budget").classList.add("input-error");
        }

        if (!posterFile) {
            valid = false;
            document.getElementById("poster-error").textContent = "Пожалуйста, загрузите постер";
            document.getElementById("poster").closest(".form-group").classList.add("input-error");
        }

        if (!videoFile) {
            valid = false;
            document.getElementById("video-error").textContent = "Пожалуйста, загрузите видео";
            document.getElementById("video").closest(".form-group").classList.add("input-error");
        }

        if (!valid) {
            return;
        }

        const formData = new FormData();
        formData.append("title", title);
        formData.append("year", year);
        formData.append("description", description);
        formData.append("country", country);
        formData.append("duration", duration);
        formData.append("budget", budget);
        formData.append("genres", JSON.stringify(genres));

        const directors = directorsRaw.split(",").map(name => name.trim()).filter(Boolean);
        const actors = actorsRaw.split(",").map(name => name.trim()).filter(Boolean);
        formData.append("directors", JSON.stringify(directors));
        formData.append("actors", JSON.stringify(actors));

        if (posterFile) {
            formData.append("poster", posterFile);
        }
        if (videoFile) {
            formData.append("video", videoFile);
        }

        try {
            let response;
            if (editingFilmId) {
                // Если редактируем фильм, отправляем PUT запрос
                response = await fetch(`http://localhost:5000/api/films/${editingFilmId}`, {
                    method: "PUT",
                    body: formData
                });
            } else {
                // Если добавляем новый фильм, отправляем POST запрос
                response = await fetch("http://localhost:5000/api/films/upload", {
                    method: "POST",
                    body: formData
                });
            }

            const result = await response.json();

            if (response.ok) {
                alert("Фильм успешно " + (editingFilmId ? "обновлён" : "добавлен") + "!");
                modalOverlay.style.display = "none";
                fetchFilms(); // Обновляем список фильмов
            } else {
                alert("Ошибка: " + result.error);
            }

        } catch (error) {
            console.error("Ошибка при загрузке:", error);
            alert("Произошла ошибка при отправке данных.");
        }
    });

    // Поиск фильмов
    const movieSearchInput = document.getElementById("movieSearch");

    async function searchFilmsByTitle() {
        const query = movieSearchInput.value.trim();

        // Если поиск пустой — показать все фильмы
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

            if (!response.ok) {
                throw new Error("Ошибка при поиске");
            }

            const films = await response.json();
            displayFilms(films);
        } catch (error) {
            console.error("Ошибка поиска:", error);
            document.getElementById("films-container").innerHTML = "<p>Ошибка при поиске фильмов</p>";
        }
    }

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

    function clearErrorOnInput(inputId, errorId, className = "input-error") {
        const input = document.getElementById(inputId);
        const error = document.getElementById(errorId);
        input.addEventListener("input", () => {
            input.classList.remove(className);
            if (error) error.textContent = "";
        });
    }

    function clearErrorOnFileChange(fileId, errorId) {
        const input = document.getElementById(fileId);
        const error = document.getElementById(errorId);
        input.addEventListener("change", () => {
            input.closest(".form-group").classList.remove("input-error");
            if (error) error.textContent = "";
        });
    }

    clearErrorOnInput("new_film", "title-error");
    clearErrorOnInput("year", "year-error");
    clearErrorOnInput("director", "director-error");
    clearErrorOnInput("actors", "actors-error");
    clearErrorOnInput("country", "country-error");
    clearErrorOnInput("duration", "duration-error");
    clearErrorOnInput("budget", "budget-error");

    clearErrorOnFileChange("poster", "poster-error");
    clearErrorOnFileChange("video", "video-error");

    document.getElementById("genreHeader").addEventListener("click", () => {
        document.getElementById("genreHeader").classList.remove("input-error");
        document.getElementById("genres-error").textContent = "";
    });
});

// Функция для обновления скрытого поля с выбранными жанрами
function updateSelectedGenres() {
    const selectedGenres = [];
    const selectedGenreElements = document.querySelectorAll(".genre-option.selected");
    selectedGenreElements.forEach(function (genreElement) {
        selectedGenres.push(genreElement.textContent.trim());
    });
    
    document.getElementById("selectedGenres").value = selectedGenres.join(", ");
}

async function fetchFilms(){
    try{
        const response = await fetch('http://localhost:5000/api/films');
        if (!response.ok){
            throw new Error("Сервер не отвечает");
        }
        const films = await response.json();
        displayFilms(films);
    } catch (error){
        console.log("Ошибка загрузки фильмов:", error);
        document.getElementById('films-container').innerHTML= '<p>Ошибка загрузки фильмов</p>';
    }
}

function displayFilms(films) {
    const container = document.getElementById('films-container');

    if (films.length === 0) {
        container.innerHTML = '<p>No films found.</p>';
        return;
    }

    container.innerHTML = films.map(film => `
                <div class="film-card" data-id="${film._id}">
                    <div class="film-header">
                        <p class="film-title-year">${film.title} (${film.year})</p>
                        <div class="film-actions">
                            <button class="btn btn-edit" onclick="editFilm('${film._id.$oid}')">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-delete" onclick="deleteFilm('${film._id.$oid}')" title="Delete">
                                <i class="fas fa-trash-alt"></i>
                            </button>
                        </div>
                    </div>
                </div>
            `).join('');
}

async function deleteFilm(filmId) {
    if (!confirm("Are you sure you want to delete this film?")) return;

    try {
        console.log("Deleting film:", filmId);

        const response = await fetch(`http://localhost:5000/api/films/${filmId}`, {
            method: 'DELETE',
        });

        const contentType = response.headers.get("content-type");

        let result;
        if (contentType && contentType.includes("application/json")) {
            result = await response.json();
        } else {
            throw new Error("Server returned non-JSON response");
        }

        if (response.ok) {
            alert(result.message);
            fetchFilms();
        } else {
            alert(`Error: ${result.error || "Unknown error"}`);
        }

    } catch (error) {
        alert(`Request failed: ${error.message}`);
        console.error("Full error:", error);
    }
}

async function editFilm(filmId) {
    console.log('Editing film with ID:', filmId);
    const response = await fetch(`http://localhost:5000/api/films/${filmId}`);
    const filmData = await response.json();

    openFilmModal(true, filmData);
    editingFilmId = filmId; // Сохраняем ID редактируемого фильма
}

function clearFilmForm() {
    document.getElementById("new_film").value = "";
    document.getElementById("year").value = "";
    document.getElementById("director").value = "";
    document.getElementById("actors").value = "";
    document.getElementById("country").value = "";
    document.getElementById("duration").value = "";
    document.getElementById("budget").value = "";
    document.getElementById("description").value = "";
    document.getElementById("selectedGenres").value = "";
    document.querySelectorAll(".genre-option.selected").forEach(el => el.classList.remove("selected"));
    document.getElementById("poster").value = "";
    document.getElementById("video").value = "";
    document.querySelectorAll(".input-error").forEach((el) => el.classList.remove("input-error"));
    document.querySelectorAll(".file-error").forEach((el) => el.classList.remove("file-error"));
    document.querySelectorAll(".error-message").forEach((el) => el.textContent = "");
}

function openFilmModal(isEditMode, filmData = null) {
    const modalOverlay = document.getElementById("add-new-film-modal");
    modalOverlay.style.display = "block";

    if (!isEditMode) {
        clearFilmForm();


        document.getElementById("new_save-changes").textContent = "Добавить фильм";
        console.log('Film Data:', filmData);
    } else if (filmData) {

        document.getElementById("new_save-changes").textContent = "Сохранить изменения";
        console.log('Film Data:', filmData);
        document.getElementById("new_film").value = filmData.title || "";
        document.getElementById("year").value = filmData.year || "";
        document.getElementById("director").value = (filmData.directors || []).join(", ");
        document.getElementById("actors").value = (filmData.actors || []).join(", ");
        document.getElementById("country").value = filmData.country || "";
        document.getElementById("duration").value = filmData.duration || "";
        document.getElementById("budget").value = filmData.budget || "";
        document.getElementById("description").value = filmData.description || "";

        // Заполнить жанры
        const selectedGenres = filmData.genres || [];
        document.getElementById("selectedGenres").value = selectedGenres.join(", ");
        document.querySelectorAll(".genre-option").forEach(el => {
            if (selectedGenres.includes(el.textContent.trim())) {
                el.classList.add("selected");
            } else {
                el.classList.remove("selected");
            }
        });

    }
}
