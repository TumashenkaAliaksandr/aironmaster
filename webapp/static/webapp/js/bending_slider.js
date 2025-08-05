/*!
 * Простой js слайдер для двух слайдов в строке,
 * с циклической прокруткой и овальной каруселью.
 * Не требует jQuery.
 */

class SimpleSlider {
  constructor(selector, options = {}) {
    this.container = document.querySelector(selector);
    if (!this.container) {
      console.warn(`SimpleSlider: контейнер ${selector} не найден`);
      return;
    }
    this.slides = this.container.children;
    this.totalSlides = this.slides.length;
    this.currentIndex = 0;
    this.options = Object.assign({
      slidesToShow: 2,
      slideWidth: 50,       // в процентах, 2 слайда => 50%
      transitionDuration: 500,
      autoPlay: true,
      autoPlayInterval: 3000,
      loop: true,
      pauseOnHover: false,
    }, options);

    this.init();
  }

  init() {
    // Устанавливаем стили контейнера
    this.container.style.display = 'flex';
    this.container.style.overflow = 'hidden';
    this.container.style.position = 'relative';

    // Оболочка для слайдов
    this.innerWrapper = document.createElement('div');
    this.innerWrapper.classList.add('slider-inner-wrapper');
    this.innerWrapper.style.display = 'flex';
    this.innerWrapper.style.width = `${(this.totalSlides / this.options.slidesToShow) * 100}%`;
    this.innerWrapper.style.transition = `transform ${this.options.transitionDuration}ms ease`;

    // Переносим слайды внутрь wrapper
    while (this.container.firstChild) {
      this.innerWrapper.appendChild(this.container.firstChild);
    }
    this.container.appendChild(this.innerWrapper);

    // Установка ширины каждого слайда
    Array.from(this.slides).forEach(slide => {
      slide.style.flex = `0 0 ${this.options.slideWidth}%`;
      slide.style.boxSizing = 'border-box';
      slide.style.padding = '10px';  // отступы между слайдами
      slide.style.transition = 'transform 0.5s ease';
      slide.style.borderRadius = '12px'; // овал по краям
      slide.style.background = '#f7f7f7';
      slide.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
    });

    if (this.options.autoPlay) {
      this.startAutoPlay();
    }
    if (this.options.pauseOnHover) {
      this.container.addEventListener('mouseenter', () => this.stopAutoPlay());
      this.container.addEventListener('mouseleave', () => this.startAutoPlay());
    }
  }

  startAutoPlay() {
    this.stopAutoPlay();
    this.autoPlayTimer = setInterval(() => {
      this.next();
    }, this.options.autoPlayInterval);
  }

  stopAutoPlay() {
    if (this.autoPlayTimer) {
      clearInterval(this.autoPlayTimer);
    }
  }

  next() {
    this.currentIndex++;
    if (this.currentIndex > this.totalSlides - this.options.slidesToShow) {
      if (this.options.loop) this.currentIndex = 0;
      else this.currentIndex = this.totalSlides - this.options.slidesToShow;
    }
    this.update();
  }

  prev() {
    this.currentIndex--;
    if (this.currentIndex < 0) {
      if (this.options.loop) this.currentIndex = this.totalSlides - this.options.slidesToShow;
      else this.currentIndex = 0;
    }
    this.update();
  }

  update() {
    const translateX = -(this.currentIndex * this.options.slideWidth);
    this.innerWrapper.style.transform = `translateX(${translateX}%)`;

    // Добавим эффект овала при прокрутке - немного уменьшаем масштаб центральных слайдов
    Array.from(this.slides).forEach((slide, i) => {
      // выделяем видимые слайды
      if (i >= this.currentIndex && i < this.currentIndex + this.options.slidesToShow) {
        slide.style.transform = 'scale(1)';
      } else {
        slide.style.transform = 'scale(0.85)';
        slide.style.filter = 'brightness(0.85)';
      }
    });
  }
}
