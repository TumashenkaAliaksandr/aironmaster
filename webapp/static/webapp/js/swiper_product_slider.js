$(document).ready(function() {
    $('.second-product-slider').owlCarousel({
        loop: true,
        nav: true,
        dots: true,
        autoplay: true,
        autoplayTimeout: 3000,
        autoplayHoverPause: false,
        margin: 19,
        navText: ['<span class="arrow-left">&#10094;</span>', '<span class="arrow-right">&#10095;</span>'],
        autoWidth: false,  // Отключаем автоопределение ширины
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
    owl.trigger('refresh.owl.carousel');
});
