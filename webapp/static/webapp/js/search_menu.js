document.addEventListener('DOMContentLoaded', () => {
  // Десктопный поиск
  const searchToggleDesktop = document.getElementById('searchToggleDesktop');
  const searchFormDesktop = document.getElementById('searchFormDesktop');
  const searchInputDesktop = searchFormDesktop.querySelector('input[name="q"]');

  searchToggleDesktop.addEventListener('click', () => {
    if (searchFormDesktop.style.display === 'block') {
      searchFormDesktop.style.display = 'none';
    } else {
      searchFormDesktop.style.display = 'block';
      searchInputDesktop.focus();
    }
  });

  // Мобильный поиск
  const searchToggleMobile = document.getElementById('searchToggleMobile');
  const searchFormMobile = document.getElementById('searchFormMobile');
  const searchInputMobile = searchFormMobile.querySelector('input[name="q"]');

  searchToggleMobile.addEventListener('click', () => {
    if (searchFormMobile.style.display === 'block') {
      searchFormMobile.style.display = 'none';
    } else {
      searchFormMobile.style.display = 'block';
      searchInputMobile.focus();
    }
  });

  // Закрытие при клике вне поиска (общее для обоих)
  document.addEventListener('click', (e) => {
    if (
      !searchFormDesktop.contains(e.target) &&
      !searchToggleDesktop.contains(e.target)
    ) {
      searchFormDesktop.style.display = 'none';
    }
    if (
      !searchFormMobile.contains(e.target) &&
      !searchToggleMobile.contains(e.target)
    ) {
      searchFormMobile.style.display = 'none';
    }
  });
});
