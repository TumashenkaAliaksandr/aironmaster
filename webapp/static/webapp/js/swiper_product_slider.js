$(document).ready(function() {
    $('.second-product-slider').owlCarousel({
        loop: true,                   // Бесконечный цикл
        nav: true,                    // Стрелки вперед/назад
        dots: true,                   // Пагинация (точки)
        autoplay: true,               // Автозапуск
        autoplayTimeout: 3000,        // Интервал прокрутки в мс
        autoplayHoverPause: false,    // Не останавливать при наведении
        margin: 20,                   // Отступ между слайдами
        navText: ['<span class="arrow-left">&#10094;</span>', '<span class="arrow-right">&#10095;</span>'], // Можно свои стрелки, или иконки
        responsive: {
            0: {
                items: 1,
                margin: 10
            },
            640: {
                items: 2,
                margin: 15
            },
            768: {
                items: 3,
                margin: 15
            },
            1024: {
                items: 4,
                margin: 20
            }
        }
    });
});
