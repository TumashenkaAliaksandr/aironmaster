document.addEventListener('DOMContentLoaded', () => {
  const track = document.querySelector('.news-carousel__track');
  const prevBtn = document.querySelector('.news-carousel__nav--prev');
  const nextBtn = document.querySelector('.news-carousel__nav--next');

  const slidesToShow = 4;

  // Клонируем первые slidesToShow слайдов в конец для бесконечности
  const slides = Array.from(track.children);
  for(let i = 0; i < slidesToShow; i++) {
    const clone = slides[i].cloneNode(true);
    track.appendChild(clone);
  }

  // Пересчитываем все слайды
  const allSlides = Array.from(track.children);

  function getSlideWidth(slide) {
    const style = window.getComputedStyle(slide);
    const width = slide.getBoundingClientRect().width;
    const marginLeft = parseFloat(style.marginLeft);
    const marginRight = parseFloat(style.marginRight);
    return width + marginLeft + marginRight;
  }

  const slideWidth = getSlideWidth(allSlides[0]);  // учитывается width + marginLeft + marginRight
  const totalSlides = allSlides.length;

  let currentIndex = 0;
  let isTransitioning = false;

  function moveToIndex(index) {
    if (isTransitioning) return;

    isTransitioning = true;
    track.style.transition = 'transform 0.5s ease';

    if (index >= totalSlides - slidesToShow) {
      // Сдвиг к клонам
      currentIndex = index;
      track.style.transform = `translateX(${-slideWidth * currentIndex}px)`;

      // После перехода сброс в начало без анимации
      track.addEventListener('transitionend', onTransitionEndLoop);
    } else if (index < 0) {
      // Можно доработать прокрутку назад (пока просто сбрасываем)
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
});
