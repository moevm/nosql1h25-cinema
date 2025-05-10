const questions = [
    {
        text: "Если бы твоя жизнь сейчас была фильмом, в каком жанре бы её сняли?",
        answers: [
            { label: "🎭 Умная драма с внезапными откровениями", value: { genre: "drama" } },
            { label: "😂 Безумная комедия с недосказанным финалом", value: { genre: "comedy" } },
            { label: "🌧 Мрачный триллер с паранойей и дождём", value: { genre: "thriller", ratingMin: "6" } },
            { label: "✨ Волшебная история с намёком на ностальгию", value: { genre: "fantasy", country: "France" } }
        ]
    },
    {
        text: "Какой вкус должен быть у идеального фильма?",
        answers: [
            { label: "🌶 Острый и дерзкий — пусть обжигает", value: { ratingMin: "7", ratingMax: "10" } },
            { label: "🍫 Сладко-горький — с послевкусием", value: { ratingMin: "5", ratingMax: "8" } },
            { label: "🍋 Лёгкий, как лимонад — не грузит", value: { ratingMax: "6", durationMax: "100" } },
            { label: "🍷 Густой, как вино — насыщает", value: { ratingMin: "1", durationMin: "120" } }
        ]
    },
    {
        text: "Что тебе ближе?",
        answers: [
            { label: "🌍 Грязная реальность, как она есть", value: { genre: "drama", country: "USA" } },
            { label: "🌀 Сюр, где неясно, что сон, а что нет", value: { genre: "surreal", ratingMin: "6" } },
            { label: "🚀 Чистая фантастика, где всё возможно", value: { genre: "sci-fi" } },
            { label: "❤️ Что-то тёплое и человеческое", value: { genre: "romance", ratingMax: "8" } }
        ]
    },
    {
        text: "После фильма тебе больше нравится:",
        answers: [
            { label: "🤫 Сидеть в тишине и переваривать увиденное", value: { genre: "thriller" } },
            { label: "🧠 Обсуждать детали и строить теории", value: { genre: "mystery", ratingMin: "7" } },
            { label: "🌫 Просто кайфовать от атмосферы", value: { description: "атмосферный" } },
            { label: "😄 Быть в хорошем настроении, не грузиться", value: { genre: "comedy", ratingMax: "7" } }
        ]
    },
    {
        text: "Что ты точно не хочешь видеть в фильме сегодня?",
        answers: [
            { label: "🐌 Медлительность и философские паузы", value: { durationMax: "100" } },
            { label: "💔 Душераздирающие драмы", value: { genre: 'thriller' } },
            { label: "🤡 Слишком странные и непонятные штуки", value: { genre: "action" } },
            { label: "🤖 Куча спецэффектов и ничего живого", value: { description: "живой" } }
        ]
    },
    {
        text: "Если бы фильм был путешествием, ты бы выбрал(а):",
        answers: [
            { label: "🚂 Медленный поезд в никуда, но красиво", value: { durationMin: "120", description: "визуальный" } },
            { label: "🛸 Прыжок в другую реальность", value: { genre: "sci-fi", ratingMin: "6" } },
            { label: "🏙 Прогулку по знакомому городу, но с неожиданным маршрутом", value: { genre: "drama", country: "Europe" } },
            { label: "🏖 Короткий отпуск для души", value: { genre: "romance", ratingMax: "7" } }
        ]
    },
    {
        text: "Что важнее всего в фильме?",
        answers: [
            { label: "🧠 Смысл и идеи", value: { ratingMin: "7" } },
            { label: "🎭 Персонажи и диалоги", value: { description: "персонажи", genre: "drama" } },
            { label: "👀 Атмосфера и визуал", value: { description: "атмосфера" } },
            { label: "🏎 Темп — чтоб не зевать ни секунды", value: { durationMax: "100" } }
        ]
    },
    {
        text: "Что ты чувствуешь после хорошего фильма?",
        answers: [
            { label: "🎯 Желание что-то изменить в себе или мире", value: { description: "вдохновляющий", ratingMin: "7" } },
            { label: "🔁 Мысли крутятся ещё пару дней", value: { genre: "psychological" } },
            { label: "😌 Улыбку и лёгкость", value: { mood: "uplifting", ratingMax: "7" } },
            { label: "🎬 Желание сразу включить следующий", value: { durationMax: "90" } }
        ]
    },
    {
        text: "С каким временем суток ты бы хотел(а) смотреть фильм?",
        answers: [
            { label: "🌅 Раннее утро — когда ещё всё впереди", value: { mood: "светлый" } },
            { label: "🌤 День — лёгкий и активный", value: { durationMax: "100" } },
            { label: "🌇 Закат — немного мечтательный", value: { description: "меланхоличный" } },
            { label: "🌌 Ночь — для глубоких ощущений и странных историй", value: { ratingMin: "7", genre: "psychological" } }
        ]
    },
    {
        text: "Какой финал тебе ближе?",
        answers: [
            { label: "🔒 Закрытый, когда всё объяснено", value: { description: "чёткий сюжет" } },
            { label: "❓Открытый — люблю додумывать", value: { genre: "surreal" } },
            { label: "💥 Неожиданный — пусть выбивает из колеи", value: { genre: "thriller", ratingMin: "6" } },
            { label: "😊 Добрый — пусть оставит надежду", value: { description: "оптимистичный" } }
        ]
    },
    {
        text: "Кто должен быть главным героем?",
        answers: [
            { label: "👩‍💼 Обычный человек с внутренней борьбой", value: { genre: "drama" } },
            { label: "🦸 Кто-то необычный — супергерой, андроид, ведьма", value: { genre: "sci-fi" } },
            { label: "👨‍👦 Герой на фоне семьи, отношений, дружбы", value: { genre: "romance", ratingMax: "8" } },
            { label: "👥 Антигерой с тёмной стороной", value: { genre: "crime", ratingMin: "7" } }
        ]
    },
    {
        text: "Какую эпоху ты хочешь почувствовать?",
        answers: [
            { label: "🕰 Прошлое — от древности до XX века", value: { yearMax: "1990" } },
            { label: "📺 Что-то из 80–90-х", value: { yearMin: "1980", yearMax: "1999" } },
            { label: "🏙 Современность — как сейчас", value: { yearMin: "2015" } },
            { label: "🚀 Будущее или альтернативные миры", value: { genre: "sci-fi", yearMin: "2020" } }
        ]
    },
    {
        text: "Какой тип саундтрека тебя цепляет больше всего?",
        answers: [
            { label: "🎻 Оркестровый, эпический", value: { description: "эпичный" } },
            { label: "🎧 Электроника, синтвейв", value: { description: "неоновый" } },
            { label: "🎸 Что-то живое и меланхоличное", value: { description: "инди"} },
            { label: "🔇 Минимум музыки — пусть будет тишина и звуки", value: { description: "натуральный звук" } }
        ]
    },
    {
        text: "Как ты относишься к «странным» фильмам?",
        answers: [
            { label: "😵 Обожаю — чем страннее, тем лучше", value: { genre: "surreal", ratingMin: "7" } },
            { label: "🤔 Нравится, если есть смысл", value: { ratingMin: "6" } },
            { label: "😐 Терплю — если красиво снято", value: { ratingMin: "5", ratingMax: "7" } },
            { label: "🚫 Нет, мне нужно чётко и понятно", value: { excludeGenre: "surreal" } }
        ]
    },
    {
        text: "Какой формат тебе сейчас ближе?",
        answers: [
            { label: "🎞 Короткий фильм — на один вечер", value: { durationMax: "90" } },
            { label: "📽 Эпическая история — можно и 3 часа", value: { durationMin: "150" } },
            { label: "📺 Мини-сериал — атмосферный и с погружением", value: { description: "сериал" } },
            { label: "🔁 Что-то из подборки — чтобы смотреть подряд", value: { ratingMin: "6", durationMax: "100" } }
        ]
    }
];


//несколько жанров?
const getRandomQuestions = (arr, n) => arr.sort(() => Math.random() - 0.5).slice(0, n);
const query = {};
let currentIndex = 0;

const titleEl = document.getElementById("question-title");
const textEl = document.getElementById("question-text");
const answersContainer = document.getElementById("answers-container");
const resultContainer = document.getElementById("result-films"); // сделай такой div под опросом

function loadQuestion(index) {
    const q = getRandomQuestions(questions, 5)[index];
    titleEl.textContent = 'Вопрос ' + (currentIndex + 1);
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

            if (currentIndex < 5) {
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
            console.log(film)
            card.classList.add("film-card");

            card.innerHTML = `
        <img src="${film.poster}" alt="${film.title}" class="film-poster">
      `;

            card.addEventListener('click', () => {
                const filmId = film._id?.$oid || film._id;
                if (filmId) window.location.href = `/movie/${filmId}`;
            });

            resultContainer.appendChild(card);
        });
    } catch (error) {
        resultContainer.innerHTML = "<p>Произошла ошибка при загрузке фильмов.</p>";
        console.error(error);
    }
}

loadQuestion(currentIndex);

