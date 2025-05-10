const questions = [
    {
        title: "Вопрос 1",
        text: "Если бы твоя жизнь сейчас была фильмом, в каком жанре бы её сняли?",
        answers: [
            { label: "🎭 Умная драма с внезапными откровениями", value: { genre: "drama" } },
            { label: "😂 Безумная комедия с недосказанным финалом", value: { genre: "comedy" } },
            { label: "🌧 Мрачный триллер с паранойей и дождём", value: { genre: "thriller", ratingMin: "6" } },
            { label: "✨ Волшебная история с намёком на ностальгию", value: { genre: "fantasy", country: "France" } }
        ]
    },
    {
        title: "Вопрос 2",
        text: "Какой вкус должен быть у идеального фильма?",
        answers: [
            { label: "🌶 Острый и дерзкий — пусть обжигает", value: { ratingMin: "7", ratingMax: "10" } },
            { label: "🍫 Сладко-горький — с послевкусием", value: { ratingMin: "5", ratingMax: "8" } },
            { label: "🍋 Лёгкий, как лимонад — не грузит", value: { ratingMax: "6" } },
            { label: "🍷 Густой, как вино — насыщает", value: { ratingMin: "1" } }
        ]
    },
    {
        title: "Вопрос 3",
        text: "Что тебе ближе?",
        answers: [
            { label: "🌍 Грязная реальность, как она есть", value: { genre: "drama", country: "USA" } },
            { label: "🌀 Сюр, где неясно, что сон, а что нет", value: { genre: "surreal" } },
            { label: "🚀 Чистая фантастика, где всё возможно", value: { genre: "sci-fi" } },
            { label: "❤️ Что-то тёплое и человеческое", value: { genre: "romance" } }
        ]
    }
];

//несколько жанров?

const query = {};
let currentIndex = 0;

const titleEl = document.getElementById("question-title");
const textEl = document.getElementById("question-text");
const answersContainer = document.getElementById("answers-container");
const resultContainer = document.getElementById("result-films"); // сделай такой div под опросом

function loadQuestion(index) {
    const q = questions[index];
    titleEl.textContent = q.title;
    textEl.textContent = q.text;
    answersContainer.innerHTML = "";

    q.answers.forEach((ans, i) => {
        const div = document.createElement("div");
        div.classList.add("answer");
        div.textContent = ans.label;

        div.onclick = async () => {
            for (const key in ans.value) {
                query[key] = ans.value[key];
            }

            currentIndex++;

            if (currentIndex < questions.length) {
                loadQuestion(currentIndex);
            } else {
                showThanks();
                console.log(query);
                await loadFilmsFromQuery(query);
            }
        };

        answersContainer.appendChild(div);
    });
}

function showThanks() {
    titleEl.textContent = "Готово!";
    textEl.textContent = "Вот фильмы по твоим вкусам:";
    answersContainer.innerHTML = "";
}

async function loadFilmsFromQuery(query) {
    try {
        const response = await fetch('/api/films/filter', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(query)
        });

        const films = await response.json();
        resultContainer.innerHTML = "";
        console.log(films);
        console.log(resultContainer.innerHTML);
        if (!films.length) {
            resultContainer.innerHTML = "<p>Ничего не найдено по твоим вкусам 😔</p>";
            return;
        }

        films.forEach(film => {
            const card = document.createElement("div");
            card.classList.add("film-card");

            card.innerHTML = `
        <img src="${film.poster}" alt="${film.title}" class="film-poster">
      `;

            card.onclick = () => {
                window.location.href = `/movie/${film.id}`;
            };

            resultContainer.appendChild(card);
        });
    } catch (error) {
        resultContainer.innerHTML = "<p>Произошла ошибка при загрузке фильмов.</p>";
        console.error(error);
    }
}

loadQuestion(currentIndex);

