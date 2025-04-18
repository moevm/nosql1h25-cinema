document.addEventListener("DOMContentLoaded", function () {
    fetchFilms();

    // Обработчик клика по кнопке "Добавить фильм"
    const addMovieBtn = document.getElementById("addMovieBtn");
    const modalOverlay = document.getElementById("add-new-film-modal");
    const cancelEditBtn = document.getElementById("new_cancel-edit");

    // Открытие модального окна
    addMovieBtn.addEventListener("click", function () {
        modalOverlay.style.display = "block";
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

        if (!title || !year || !directorsRaw) {
            alert("Пожалуйста, заполните обязательные поля");
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
            const response = await fetch("http://localhost:5000/api/films/upload", {
                method: "POST",
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                alert("Фильм успешно добавлен!");
                modalOverlay.style.display = "none";
                fetchFilms();
            } else {
                alert("Ошибка при добавлении фильма: " + result.error);
            }

        } catch (error) {
            console.error("Ошибка при загрузке:", error);
            alert("Произошла ошибка при отправке данных.");
        }
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
                            <button class="btn btn-edit" onclick="editFilm('${film._id}')">
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

