document.addEventListener('DOMContentLoaded', () => {
  // --- Активная ссылка меню при скролле ---
  // Получаем все секции с id и все ссылки меню внутри nav
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('nav .nav-link');

  // Функция, которая подсвечивает активную ссылку меню в зависимости от прокрутки
  function onScroll() {
    const scrollPos = window.scrollY + 150; // поправка для фиксированной шапки
    let currentSectionId = '';

    if (sections.length > 0) {
      // Перебираем все секции и определяем, в какой сейчас скролл
      sections.forEach(section => {
        const top = section.offsetTop;
        const height = section.offsetHeight;
        if (scrollPos >= top && scrollPos < top + height) {
          currentSectionId = section.id;
        }
      });

      // Если скролл выше первой секции — выделяем первую секцию
      if (scrollPos < sections[0].offsetTop) {
        currentSectionId = sections[0].id;
      }
    }

    // Перебираем все ссылки меню и ставим класс active у той, href которой совпадает с текущей секцией
    navLinks.forEach(link => {
      link.classList.toggle('active', link.getAttribute('href') === '#' + currentSectionId);
    });
  }

  // Навешиваем обработчик скролла только если есть секции
  if (sections.length > 0) {
    window.addEventListener('scroll', onScroll);
    onScroll(); // вызываем один раз при загрузке страницы, чтобы сразу подсветить активный пункт
  }


  // --- Кнопка "Наверх" ---
  const scrollBtn = document.getElementById('scrollToTopBtn');

  if (scrollBtn) {
    // Показываем кнопку "Наверх" при прокрутке вниз более чем на 300px
    window.addEventListener('scroll', () => {
      scrollBtn.classList.toggle('show', window.scrollY > 300);
    });

    // При клике плавно скроллим вверх
    scrollBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }


  // --- Плавный скролл по якорям в меню ---
  navLinks.forEach(link => {
    link.addEventListener('click', e => {
      const href = link.getAttribute('href');

      if (!href) return;

      // Обрабатываем только ссылки, начинающиеся с #
      if (href.startsWith('#')) {
        e.preventDefault();

        const targetId = href.substring(1);
        const targetElem = document.getElementById(targetId);

        if (targetElem) {
          targetElem.scrollIntoView({ behavior: 'smooth' });
          history.pushState(null, '', href);
        }
      }
      // Для остальных ссылок переход происходит как обычно
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

      // При открытии меню закрываем все открытые дропдауны
      if (!expanded) {
        mobileMenu.querySelectorAll('.dropdown.open').forEach(drop => drop.classList.remove('open'));
      }
    });

    // Закрытие меню при клике на ссылку внутри меню
    mobileMenu.querySelectorAll('a.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        closeMobileMenu();
      });
    });

    // Закрытие меню и дропдаунов при клике вне меню и кнопки
    document.addEventListener('click', (e) => {
      const target = e.target;
      if (!mobileMenu.contains(target) && !burgerBtn.contains(target)) {
        closeMobileMenu();
      }
    });

    // Функция закрытия меню и всех дропдаунов
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

        // Переключаем состояние текущего дропдауна
        if (isOpen) {
          parentDropdown.classList.remove('open');
        } else {
          parentDropdown.classList.add('open');
        }
      });
    });
  }


  // --- Подёргивание иконок соцсетей ---
  const icons = document.querySelectorAll('.social-icon');
  let isShaking = false;

  function triggerShake() {
    if (isShaking) return; // предотвращаем наложение анимаций
    isShaking = true;

    icons.forEach(icon => {
      icon.classList.add('shake');
      icon.addEventListener('animationend', () => {
        icon.classList.remove('shake');
        isShaking = false;
      }, { once: true });
    });
  }

  // Запускаем подёргивание через 1 секунду после загрузки, затем каждые 10 секунд
  setTimeout(() => {
    triggerShake();
    setInterval(triggerShake, 10000);
  }, 1000);
});


window.addEventListener('load', function () {
  document.getElementById('preloader').style.display = 'none';
});


document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('requestModal');

    const openButton = document.getElementById('openRequestModal');
    const mobileOpenButton = document.getElementById('openRequestModalmobile');

    if (!modal) {
        return;
    }

    const closeButtons = modal.querySelectorAll('[data-close-modal]');
    let previousFocus = null;

    function openModal() {
        previousFocus = document.activeElement;

        modal.classList.add('is-open');
        modal.setAttribute('aria-hidden', 'false');
        document.body.classList.add('request-modal-open');

        const firstInput = modal.querySelector(
            'input:not([type="hidden"]), textarea, select'
        );

        if (firstInput) {
            firstInput.focus();
        }
    }

    function closeModal() {
        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('request-modal-open');

        if (previousFocus) {
            previousFocus.focus();
        }
    }

    if (openButton) {
        openButton.addEventListener('click', openModal);
    }

    if (mobileOpenButton) {
        mobileOpenButton.addEventListener('click', openModal);
    }

    closeButtons.forEach(function (button) {
        button.addEventListener('click', closeModal);
    });

    document.addEventListener('keydown', function (event) {
        if (
            event.key === 'Escape' &&
            modal.classList.contains('is-open')
        ) {
            closeModal();
        }
    });
});
