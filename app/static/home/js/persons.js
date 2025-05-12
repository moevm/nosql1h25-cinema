function getFilmIdFromPath() {
    const pathParts = window.location.pathname.split('/');
    const filmIndex = pathParts.indexOf('movie');
    if (filmIndex !== -1 && pathParts.length > filmIndex + 1) {
      return pathParts[filmIndex + 1];
    }
    return null;
  }
  
  async function loadPersons() {
    const filmId = getFilmIdFromPath();
  
    if (!filmId) {
      console.error('film_id не найден в URL');
      showError('Некорректный адрес страницы. Пожалуйста, проверьте URL.');
      return;
    }
  
    try {
      const response = await fetch(`/api/${filmId}/persons`);
      if (!response.ok) {
        if (response.status === 404) {
          showError('Информация о фильме не найдена.');
        } else {
          showError('Ошибка при загрузке данных с сервера.');
        }
        throw new Error(`Ошибка: ${response.status}`);
      }
  
      const data = await response.json();
      renderPersons(data.directors, 'directors');
      renderPersons(data.actors, 'actors');
    } catch (error) {
      console.error('Ошибка при получении данных:', error);
      showError('Не удалось загрузить данные. Попробуйте позже.');
    }
  }
  
  function renderPersons(persons, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
  
    if (!persons || persons.length === 0) {
      container.innerHTML = '<p>Нет данных.</p>';
      return;
    }
  
    persons.forEach(person => {
      const card = document.createElement('div');
      card.className = 'person-card';
  
      card.innerHTML = `
        <img src="${person.photo_url || 'https://via.placeholder.com/80'}" alt="${person.name}">
        <div class="person-info">
          <div class="person-name">${person.name}</div>
          <div class="person-details">
            Дата рождения: ${person.birth_date ? new Date(person.birth_date).toLocaleDateString('ru-RU') : '—'}<br>
            Место рождения: ${person.birth_place || '—'}<br>
            ${person.wiki_link ? `<a href="${person.wiki_link}" target="_blank" style="color: #ccc;">Wikipedia</a>` : ''}
          </div>
        </div>
      `;
  
      container.appendChild(card);
    });
  }
  
  function showError(message) {
    const container = document.querySelector('.container');
    container.innerHTML = `<p style="color: #ffcccc; font-size: 1.2rem;">${message}</p>`;
  }
  
  document.addEventListener('DOMContentLoaded', loadPersons);
  