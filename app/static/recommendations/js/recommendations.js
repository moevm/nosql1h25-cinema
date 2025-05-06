const questions = [
    {
        title: "Вопрос 1",
        text: "Если бы твоя жизнь сейчас была фильмом, в каком жанре бы её сняли?",
        answers: ["🎭 Умная драма с внезапными откровениями", "😂 Безумная комедия с недосказанным финалом", "🌧 Мрачный триллер с паранойей и дождём", "✨ Волшебная история с намёком на ностальгию"]
    },
    {
        title: "Вопрос 2",
        text: "Какой вкус должен быть у идеального фильма?",
        answers: ["🌶 Острый и дерзкий — пусть обжигает", "🍫 Сладко-горький — с послевкусием", "🍋 Лёгкий, как лимонад — не грузит", "🍷 Густой, как вино — насыщает"]
    },
    {
        title: "Вопрос 3",
        text: "Что тебе ближе?",
        answers: ["🌍 Грязная реальность, как она есть", "🌀 Сюр, где неясно, что сон, а что нет", "🚀 Чистая фантастика, где всё возможно", "❤️ Что-то тёплое и человеческое"]
    }
];

let currentIndex = 0;

const titleEl = document.getElementById("question-title");
const textEl = document.getElementById("question-text");
const answersContainer = document.getElementById("answers-container");

function loadQuestion(index) {
    const q = questions[index];
    titleEl.textContent = q.title;
    textEl.textContent = q.text;
    answersContainer.innerHTML = "";

    q.answers.forEach((answer, i) => {
        const div = document.createElement("div");
        div.classList.add("answer");
        div.textContent = String.fromCharCode(65 + i) + ". " + answer;
        div.onclick = () => {
            currentIndex++;
            if (currentIndex < questions.length) {
                loadQuestion(currentIndex);
            } else {
                showThanks();
            }
        };
        answersContainer.appendChild(div);
    });
}

function showThanks() {
    titleEl.textContent = "Спасибо за прохождение!";
    textEl.textContent = "";
    answersContainer.innerHTML = "";
}

loadQuestion(currentIndex);
