document.addEventListener('DOMContentLoaded', () => {
  const swiper = new Swiper('.second-product-slider', {
    slidesPerView: 4,
    spaceBetween: 20,
    freeMode: false,
    loop: true,                  // Всегда включён бесконечный цикл
    autoplay: {
      delay: 3000,               // Интервал автоперелистывания (3 секунды)
      disableOnInteraction: false, // НЕ останавливать автопрокрутку при взаимодействии
      pauseOnMouseEnter: false,     // Не останавливать при наведении мыши (опционально)
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
    breakpoints: {
      320: { slidesPerView: 1, spaceBetween: 10 },
      640: { slidesPerView: 2, spaceBetween: 15 },
      768: { slidesPerView: 3, spaceBetween: 15 },
      1024: { slidesPerView: 4, spaceBetween: 20 },
    },
  });
});
