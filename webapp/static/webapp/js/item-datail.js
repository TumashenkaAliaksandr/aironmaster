// Скрипт для переключения главного фото по клику на миниатюры
document.addEventListener('DOMContentLoaded', function () {
    const mainPhoto = document.getElementById('main-photo');
    const thumbnails = document.querySelectorAll('.thumbnail-photo');

    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', function () {
            // Меняем источник главного фото
            mainPhoto.src = this.dataset.full;

            // Убираем рамку у всех миниатюр
            thumbnails.forEach(t => t.style.borderColor = 'transparent');

            // Добавляем рамку выбранной миниатюре
            this.style.borderColor = '#5a3f99'; // фиолетовый цвет рамки
        });
    });

    // По умолчанию выделяем первую миниатюру, если есть
    if (thumbnails.length > 0) {
        thumbnails[0].style.borderColor = '#5a3f99';
    }
});