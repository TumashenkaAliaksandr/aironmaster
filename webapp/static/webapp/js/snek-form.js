document.getElementById('open-order-form').onclick = function() {
    document.getElementById('order-modal').classList.add('active');
};
document.getElementById('close-order-form').onclick = function() {
    document.getElementById('order-modal').classList.remove('active');
};
// Закрытие по клику вне формы
document.getElementById('order-modal').onclick = function(e) {
    if (e.target === this) this.classList.remove('active');
};
