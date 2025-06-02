const modal = document.getElementById('order-modal');
const openBtn = document.getElementById('open-order-form');
const closeBtn = document.getElementById('close-order-form');

openBtn.onclick = function() {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden'; // Запрет прокрутки страницы
};

closeBtn.onclick = function() {
    modal.classList.remove('active');
    document.body.style.overflow = ''; // Восстановление прокрутки страницы
};

modal.onclick = function(e) {
    if (e.target === modal) {
        modal.classList.remove('active');
        document.body.style.overflow = ''; // Восстановление прокрутки страницы
    }
};
