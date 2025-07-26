document.addEventListener('DOMContentLoaded', () => {
    const swiper = new Swiper('.second-product-slider', {
        slidesPerView: 4,
        spaceBetween: 20,
        loop: true,

        autoplay: {
            delay: 3000,
            disableOnInteraction: false,
            pauseOnMouseEnter: false,
        },

        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },

        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },

        freeMode: false,

        breakpoints: {
            320: {slidesPerView: 1, spaceBetween: 10},
            640: {slidesPerView: 2, spaceBetween: 15},
            768: {slidesPerView: 3, spaceBetween: 15},
            1024: {slidesPerView: 4, spaceBetween: 20},
        },
    });
});
