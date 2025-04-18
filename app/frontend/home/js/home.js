document.addEventListener('DOMContentLoaded', () => {
    const filmGrid = document.getElementById('filmGrid');
    const filmTemplate = document.getElementById('filmTemplate');
    const menuLinks = document.querySelectorAll('.menu__link');
    
    loadContent('all');
    
    // Обработчики для меню
    menuLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const type = e.target.dataset.type;
            loadContent(type);
            
            // Обновление активной ссылки
            menuLinks.forEach(item => item.classList.remove('menu__link_active'));
            e.target.classList.add('menu__link_active');
        });
    });
    
    async function loadContent(type) {
        try {
            const response = await fetch(`/api/content?type=${type}`);
            const films = await response.json();
            
            filmGrid.innerHTML = '';
            
            films.forEach(film => {
                const card = filmTemplate.content.cloneNode(true);
                const filmCard = card.querySelector('.film-card');
                
                card.querySelector('.film-poster').src = film.poster;
                card.querySelector('.film-poster').alt = film.title;
                
                filmCard.addEventListener('click', () => {
                    window.location.href = `/movie/${film.id}`;
                });
                
                filmGrid.appendChild(card);
            });
        } catch (error) {
            console.error('Ошибка загрузки:', error);
        }
    }
});
