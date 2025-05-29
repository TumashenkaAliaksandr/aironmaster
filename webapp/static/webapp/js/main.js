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

  navLinks.forEach(link => {
    link.addEventListener('click', e => {
      const href = link.getAttribute('href');

      if (!href) return;

      // Обрабатываем только ссылки, которые начинаются с #
      if (href.startsWith('#')) {
        e.preventDefault();

        const targetId = href.substring(1);
        const targetElem = document.getElementById(targetId);

        if (targetElem) {
          targetElem.scrollIntoView({behavior: 'smooth'});
          history.pushState(null, '', href);
        }
      }
      // Для всех остальных ссылок переход происходит как обычно, без preventDefault
    });
  });



  // --- Кастомное мобильное меню ---
  const burgerBtn = document.getElementById('burgerBtn');
const mobileMenu = document.getElementById('mobileMenu');

if (burgerBtn && mobileMenu) {
  // Открытие/закрытие мобильного меню по кнопке
  burgerBtn.addEventListener('click', () => {
    const expanded = burgerBtn.getAttribute('aria-expanded') === 'true';
    burgerBtn.setAttribute('aria-expanded', String(!expanded));
    burgerBtn.classList.toggle('open');
    mobileMenu.classList.toggle('show');
    mobileMenu.setAttribute('aria-hidden', String(expanded));

    // При открытии меню убираем все открытые дропдауны
    if (!expanded) {
      mobileMenu.querySelectorAll('.dropdown.open').forEach(drop => drop.classList.remove('open'));
    }
  });

  // Закрытие меню при клике на ссылку
  mobileMenu.querySelectorAll('a.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      closeMobileMenu();
    });
  });

  // Обработчик клика вне меню и бургера — закрываем меню и дропдауны
  document.addEventListener('click', (e) => {
    const target = e.target;
    if (!mobileMenu.contains(target) && !burgerBtn.contains(target)) {
      closeMobileMenu();
    }
  });

  // Функция закрытия меню и дропдаунов
  function closeMobileMenu() {
    burgerBtn.classList.remove('open');
    burgerBtn.setAttribute('aria-expanded', 'false');
    mobileMenu.classList.remove('show');
    mobileMenu.setAttribute('aria-hidden', 'true');
    mobileMenu.querySelectorAll('.dropdown.open').forEach(drop => drop.classList.remove('open'));
  }
}

// --- Дропдауны в мобильном меню ---
  if (mobileMenu) {
  mobileMenu.querySelectorAll('.dropdown > .dropbtn').forEach(dropBtn => {
    dropBtn.addEventListener('click', function (e) {
      e.preventDefault();

      const parentDropdown = this.closest('.dropdown');
      const isOpen = parentDropdown.classList.contains('open');

      // Закрываем все открытые дропдауны, кроме текущего
      mobileMenu.querySelectorAll('.dropdown.open').forEach(drop => {
        if (drop !== parentDropdown) drop.classList.remove('open');
      });

      // Если текущий открыт — закрываем, иначе открываем
      if (isOpen) {
        parentDropdown.classList.remove('open');
      } else {
        parentDropdown.classList.add('open');
      }
    });
  });
}


});