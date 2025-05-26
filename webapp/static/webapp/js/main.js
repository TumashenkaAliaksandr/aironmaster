document.addEventListener('DOMContentLoaded', () => {
  // --- Активная ссылка меню при скролле ---
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('nav .nav-link');

  function onScroll() {
    const scrollPos = window.scrollY + 150; // поправка для шапки
    let currentSectionId = '';

    sections.forEach(section => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      if (scrollPos >= top && scrollPos < top + height) {
        currentSectionId = section.id;
      }
    });

    if (scrollPos < sections[0].offsetTop) {
      currentSectionId = sections[0].id;
    }

    navLinks.forEach(link => {
      link.classList.toggle('active', link.getAttribute('href') === '#' + currentSectionId);
    });
  }

  window.addEventListener('scroll', onScroll);
  onScroll(); // вызов при загрузке страницы

  // --- Кнопка "Наверх" ---
  const scrollBtn = document.getElementById('scrollToTopBtn');

  if (scrollBtn) {
    window.addEventListener('scroll', () => {
      scrollBtn.classList.toggle('show', window.scrollY > 300);
    });

    scrollBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // --- Плавный скролл по клику на ссылки в nav ---
  navLinks.forEach(link => {
    link.addEventListener('click', e => {
      e.preventDefault();
      const targetId = link.getAttribute('href');
      const targetElem = document.querySelector(targetId);
      if (targetElem) {
        targetElem.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // --- Кастомное мобильное меню ---
  const burgerBtn = document.getElementById('burgerBtn');
  const mobileMenu = document.getElementById('mobileMenu');

  if (burgerBtn && mobileMenu) {
    burgerBtn.addEventListener('click', () => {
      console.log('Burger clicked');
      const expanded = burgerBtn.getAttribute('aria-expanded') === 'true';
      burgerBtn.setAttribute('aria-expanded', String(!expanded));
      burgerBtn.classList.toggle('open');
      mobileMenu.classList.toggle('show');
      mobileMenu.setAttribute('aria-hidden', String(expanded));
      console.log('Menu shown:', mobileMenu.classList.contains('show'));
    });



    mobileMenu.querySelectorAll('a.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        burgerBtn.classList.remove('open');
        burgerBtn.setAttribute('aria-expanded', false);
        mobileMenu.classList.remove('show');
        mobileMenu.setAttribute('aria-hidden', true);
      });
    });
  }
});
