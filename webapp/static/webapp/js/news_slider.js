document.addEventListener('DOMContentLoaded', () => {
  const track = document.querySelector('.news-carousel__track');
  const prevBtn = document.querySelector('.news-carousel__nav--prev');
  const nextBtn = document.querySelector('.news-carousel__nav--next');

  let slidesToShow = window.innerWidth < 768 ? 1 : 4;

  // Клонирование и сброс слайдов будем делать в функции initCarousel, можно вызвать повторно при ресайзе
  function initCarousel() {
    // Очистим трек от клонированных слайдов, если есть
    [...track.querySelectorAll('.clone')].forEach(clone => clone.remove());

    const slides = Array.from(track.children).filter(slide => !slide.classList.contains('clone'));

    // Клонируем первые slidesToShow слайдов для бесконечной прокрутки
    for(let i = 0; i < slidesToShow; i++) {
      const clone = slides[i].cloneNode(true);
      clone.classList.add('clone');
      track.appendChild(clone);
    }

    currentIndex = 0;

    // Рассчитаем ширину слайда с margin
    const allSlides = Array.from(track.children);
    slideWidth = getSlideWidth(allSlides[0]);
    totalSlides = allSlides.length;

    moveToIndex(0);
  }

  function getSlideWidth(slide) {
    const style = window.getComputedStyle(slide);
    const width = slide.getBoundingClientRect().width;
    const marginLeft = parseFloat(style.marginLeft);
    const marginRight = parseFloat(style.marginRight);
    return width + marginLeft + marginRight;
  }

  let currentIndex = 0;
  let slideWidth = 0;
  let totalSlides = 0;
  let isTransitioning = false;

  function moveToIndex(index) {
    if (isTransitioning) return;

    isTransitioning = true;
    track.style.transition = 'transform 0.5s ease';

    if (index >= totalSlides - slidesToShow) {
      currentIndex = index;
      track.style.transform = `translateX(${-slideWidth * currentIndex}px)`;
      track.addEventListener('transitionend', onTransitionEndLoop);
    } else if (index < 0) {
      currentIndex = 0;
      track.style.transition = 'none';
      track.style.transform = 'translateX(0)';
      isTransitioning = false;
    } else {
      currentIndex = index;
      track.style.transform = `translateX(${-slideWidth * currentIndex}px)`;
      track.addEventListener('transitionend', onTransitionEndSimple);
    }
  }

  function onTransitionEndLoop() {
    track.style.transition = 'none';
    currentIndex = 0;
    track.style.transform = 'translateX(0)';
    track.removeEventListener('transitionend', onTransitionEndLoop);
    isTransitioning = false;
  }

  function onTransitionEndSimple() {
    track.removeEventListener('transitionend', onTransitionEndSimple);
    isTransitioning = false;
  }

  prevBtn.addEventListener('click', () => {
    moveToIndex(currentIndex - 1);
  });

  nextBtn.addEventListener('click', () => {
    moveToIndex(currentIndex + 1);
  });

  // Автопролистка
  let autoSlideInterval = setInterval(() => {
    moveToIndex(currentIndex + 1);
  }, 3000);

  const carouselWrapper = document.querySelector('.news-carousel__wrapper');
  carouselWrapper.addEventListener('mouseenter', () => clearInterval(autoSlideInterval));
  carouselWrapper.addEventListener('mouseleave', () => {
    autoSlideInterval = setInterval(() => {
      moveToIndex(currentIndex + 1);
    }, 3000);
  });

  // Инициализация карусели при загрузке
  initCarousel();

  // Обработка ресайза - пересчитываем slidesToShow и реинициализируем
  window.addEventListener('resize', () => {
    const newSlidesToShow = window.innerWidth < 768 ? 1 : 4;
    if (newSlidesToShow !== slidesToShow) {
      slidesToShow = newSlidesToShow;
      initCarousel();
    }
  });
});
