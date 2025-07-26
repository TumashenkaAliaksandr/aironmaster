document.addEventListener('DOMContentLoaded', () => {
    const swiper = new Swiper('.second-product-slider', {
        slidesPerView: 4,          // Показываем по 4 слайда на больших экранах
        spaceBetween: 20,
        freeMode: false,           // Отключаем свободный режим для корректного перелистывания
        loop: false,               // Можно включить, если нужно бесконечное зацикливание
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        breakpoints: {
            320: {
                slidesPerView: 1,
                spaceBetween: 10,
            },
            640: {
                slidesPerView: 2,
                spaceBetween: 15,
            },
            768: {
                slidesPerView: 3,
                spaceBetween: 15,
            },
            1024: {
                slidesPerView: 4,
                spaceBetween: 20,
            },
        },
    });
});
