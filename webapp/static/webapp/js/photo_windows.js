document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('customModal');
  if (!modal) {
    console.error('Модальное окно с id="customModal" не найдено');
    return;
  }
  const overlay = modal.querySelector('.custom-modal-overlay');
  const modalImage = document.getElementById('customModalImage');
  const modalDescription = document.getElementById('customModalDescription');
  const btnClose = modal.querySelector('.custom-close');
  const btnPrev = modal.querySelector('.custom-prev');
  const btnNext = modal.querySelector('.custom-next');

  if (!overlay || !modalImage || !modalDescription || !btnClose || !btnPrev || !btnNext) {
    console.error('Некоторые элементы модального окна не найдены');
    return;
  }

  let galleryImages = [];
  let currentIndex = -1;

  function openModal(index) {
    if (index < 0 || index >= galleryImages.length) {
      console.warn('openModal: индекс вне диапазона', index);
      return;
    }
    currentIndex = index;

    const img = galleryImages[currentIndex];
    const src = img.getAttribute('data-src') || img.src;
    const alt = img.alt || '';

    console.log('Открываем модалку с изображением:', src);

    modalImage.src = src;
    modalImage.alt = alt;
    modalDescription.textContent = alt;

    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    modal.classList.add('hidden');
    modalImage.src = '';
    modalDescription.textContent = '';
    currentIndex = -1;
    galleryImages = [];
    document.body.style.overflow = '';
    console.log('Модальное окно закрыто');
  }

  function showPrev() {
    if (currentIndex === -1) return;
    let newIndex = currentIndex - 1;
    if (newIndex < 0) newIndex = galleryImages.length - 1;
    openModal(newIndex);
  }

  function showNext() {
    if (currentIndex === -1) return;
    let newIndex = currentIndex + 1;
    if (newIndex >= galleryImages.length) newIndex = 0;
    openModal(newIndex);
  }

  const imgs = document.querySelectorAll('.photo-gallery img');
  console.log('Найдено изображений в галереях:', imgs.length);

  imgs.forEach(img => {
    img.style.cursor = 'pointer';
    img.addEventListener('click', (e) => {
      const galleryContainer = e.target.closest('.photo-gallery');
      if (!galleryContainer) {
        console.warn('Родительский контейнер .photo-gallery не найден');
        return;
      }

      galleryImages = Array.from(galleryContainer.querySelectorAll('img'));
      currentIndex = galleryImages.indexOf(e.target);

      console.log('Открываем изображение с индексом:', currentIndex);

      openModal(currentIndex);
    });
  });

  btnClose.addEventListener('click', closeModal);
  overlay.addEventListener('click', closeModal);
  btnPrev.addEventListener('click', showPrev);
  btnNext.addEventListener('click', showNext);

  document.addEventListener('keydown', (e) => {
    if (modal.classList.contains('hidden')) return;

    console.log('Нажата клавиша:', e.key);

    if (e.key === 'Escape') closeModal();
    else if (e.key === 'ArrowLeft') showPrev();
    else if (e.key === 'ArrowRight') showNext();
  });
});

window.addEventListener('error', (event) => {
  console.error('Global error:', event.message, 'at', event.filename + ':' + event.lineno);
});
