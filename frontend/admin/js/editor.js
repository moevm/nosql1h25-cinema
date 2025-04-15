document.addEventListener("DOMContentLoaded", function (){
    fetchFilms();
});

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
        document.getElementById('films-container').innerHTML=
            '<p>Ошибка загрузки фильмов</p>'
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


