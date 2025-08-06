document.addEventListener('DOMContentLoaded', () => {
    const slider = document.getElementById('photoSlider');
    if (!slider) return;

    const wrapper = slider.querySelector('.slider-inner-wrapper');
    const slides = wrapper.children;

    let slidesToShow = window.innerWidth < 768 ? 1 : 3; // адаптив: 1 на мобиле, 3 на десктопе
    let currentIndex = 0;
    let slideWidth = 0; // ширина слайда вместе с margin
    let totalSlides = slides.length;

    // Получаем кнопки переключения слайдов из слайдера (предполагаем, что они есть в DOM)
    const prevBtn = slider.querySelector('.slider-prev');
    const nextBtn = slider.querySelector('.slider-next');

    // Получаем кнопки навигации внутри модального окна
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const modalPrevBtn = modal.querySelector('#modalPrev');
    const modalNextBtn = modal.querySelector('#modalNext');

    // Индекс текущего фото в модальном окне
    let modalCurrentIndex = 0;

    function calculateSlideWidth() {
        if (slides.length === 0) return 0;
        const style = getComputedStyle(slides[0]);
        const width = slides[0].getBoundingClientRect().width;
        const marginLeft = parseFloat(style.marginLeft) || 0;
        const marginRight = parseFloat(style.marginRight) || 0;
        return width + marginLeft + marginRight;
    }

    function updateSlider() {
        const translateX = -currentIndex * slideWidth;
        wrapper.style.transform = `translateX(${translateX}px)`;
    }

    function nextSlide() {
        if (currentIndex >= totalSlides - slidesToShow) {
            currentIndex = 0;
        } else {
            currentIndex++;
        }
        updateSlider();
    }

    function prevSlide() {
        if (currentIndex <= 0) {
            currentIndex = totalSlides - slidesToShow;
        } else {
            currentIndex--;
        }
        updateSlider();
    }

    // Навигация в модальном окне
    function showModalImage(index) {
        if (index < 0) {
            modalCurrentIndex = totalSlides - 1;
        } else if (index >= totalSlides) {
            modalCurrentIndex = 0;
        } else {
            modalCurrentIndex = index;
        }

        const imgSrc = slides[modalCurrentIndex].querySelector('img').src;
        const imgAlt = slides[modalCurrentIndex].querySelector('img').alt || '';
        modalImg.src = imgSrc;
        modalImg.alt = imgAlt;
    }

    if (modalPrevBtn) {
        modalPrevBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            showModalImage(modalCurrentIndex - 1);
        });
    }
    if (modalNextBtn) {
        modalNextBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            showModalImage(modalCurrentIndex + 1);
        });
    }

    // Открываем модалку по клику на миниатюру и назначаем текущий индекс
    slider.querySelectorAll('.slide img').forEach((img, idx) => {
        img.addEventListener('click', (e) => {
            modalCurrentIndex = idx;
            showModalImage(modalCurrentIndex);
            modal.style.display = 'flex';
        });
    });

    // Закрытие модалки по клику вне изображения
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
            modalImg.src = '';
            modalImg.alt = '';
        }
    });

    // Закрытие по клавише ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.style.display === 'flex') {
            modal.style.display = 'none';
            modalImg.src = '';
            modalImg.alt = '';
        }
    });

    // Автопрокрутка слайдера с паузой
    let autoPlayInterval = null;

    function startAutoPlay() {
        stopAutoPlay();
        autoPlayInterval = setInterval(nextSlide, 3000);
    }

    function stopAutoPlay() {
        if (autoPlayInterval) {
            clearInterval(autoPlayInterval);
            autoPlayInterval = null;
        }
    }

    slider.addEventListener('mouseenter', stopAutoPlay);
    slider.addEventListener('mouseleave', startAutoPlay);

    function init() {
        slidesToShow = window.innerWidth < 768 ? 1 : 3;
        currentIndex = 0;

        wrapper.style.transition = 'none';
        wrapper.style.transform = 'translateX(0)';

        slideWidth = calculateSlideWidth();

        setTimeout(() => {
            wrapper.style.transition = 'transform 0.5s ease';
        }, 50);

        updateSlider();
        startAutoPlay();
    }

    window.addEventListener('resize', init);

    init();
});
