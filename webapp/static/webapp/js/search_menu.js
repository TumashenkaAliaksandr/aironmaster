document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('searchToggle');
  const searchForm = document.getElementById('searchForm');
  const searchInput = document.getElementById('searchInput');
  const searchResults = document.getElementById('searchResults');
  let debounceTimeout = null;

  if (!toggleBtn || !searchForm || !searchInput || !searchResults) {
    console.warn('Search menu initialization aborted - required elements not found.');
    return;
  }

  // Показ / скрытие формы поиска по кнопке с лупой
  toggleBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    if (searchForm.style.display === 'block') {
      searchForm.style.display = 'none';
      clearResults();
    } else {
      searchForm.style.display = 'block';
      searchInput.focus();
    }
  });

  // Очистка результатов
  function clearResults() {
    searchResults.innerHTML = '';
    searchResults.style.display = 'none';
  }

  // Рендер результатов в выпадающем списке
  function renderResults(results) {
    if (!results || !Array.isArray(results) || results.length === 0) {
      clearResults();
      return;
    }

    searchResults.innerHTML = '';

    results.forEach(result => {
      const a = document.createElement('a');
      a.href = result.url || '#';
      a.className = 'search-result-item';
      a.style.display = 'block';
      a.style.padding = '8px 12px';
      a.style.borderBottom = '1px solid #eee';
      a.style.color = '#333';
      a.style.textDecoration = 'none';

      const title = document.createElement('div');
      title.textContent = result.title;  // без (item) и типа
      title.style.fontWeight = 'bold';
      a.appendChild(title);

      if (result.description) {
        const desc = document.createElement('div');
        desc.textContent = result.description;
        desc.style.fontSize = '0.85em';
        desc.style.color = '#666';
        a.appendChild(desc);
      }

      a.addEventListener('mouseover', () => { a.style.backgroundColor = '#f0f0f0'; });
      a.addEventListener('mouseout', () => { a.style.backgroundColor = 'transparent'; });

      searchResults.appendChild(a);
    });

    searchResults.style.display = 'block';
  }

  // AJAX запрос с debounce
  function performSearch(query) {
    if (!query) {
      clearResults();
      return;
    }

    fetch(`/ajax/search/?q=${encodeURIComponent(query)}`)
      .then(response => {
        if (!response.ok) throw new Error('Network response was not OK');
        return response.json();
      })
      .then(data => {
        if (data && Array.isArray(data.results)) {
          renderResults(data.results);
        } else {
          clearResults();
        }
      })
      .catch(() => {
        clearResults();
      });
  }

  // Обработчик ввода с задержкой
  searchInput.addEventListener('input', () => {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(() => {
      performSearch(searchInput.value.trim());
    }, 300);
  });

  // Скрыть поиск при клике вне формы и кнопки
  document.addEventListener('click', (e) => {
    if (!searchForm.contains(e.target) && !toggleBtn.contains(e.target)) {
      searchForm.style.display = 'none';
      clearResults();
    }
  });

  // Закрывать поиск по Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      searchForm.style.display = 'none';
      clearResults();
    }
  });
});
