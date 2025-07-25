document.addEventListener('DOMContentLoaded', () => {
  const mainPhoto = document.getElementById('main-photo');
  const thumbnails = document.querySelectorAll('.thumbnail-photo');

  const modal = document.getElementById('customModal');
  const modalOverlay = modal.querySelector('.custom-modal-overlay');
  const modalContent = modal.querySelector('.custom-modal-content');
  const modalImage = document.getElementById('customModalImage');
  const modalDescription = document.getElementById('customModalDescription');
  const btnClose = modal.querySelector('.custom-close');
  const btnPrev = modal.querySelector('.custom-prev');
  const btnNext = modal.querySelector('.custom-next');

  if (!mainPhoto) {
    console.warn('Main photo element with id="main-photo" not found.');
    return;
  }

  if (!modal) {
    console.warn('Modal element with id="customModal" not found.');
    return;
  }

  // Собираем фотографии (источники, alt и описание) из галереи
  const photos = [];

  // Если есть главное фото, добавляем его первым
  photos.push({
    full: mainPhoto.src,
    alt: mainPhoto.alt || '',
    description: ''
  });

  thumbnails.forEach(thumb => {
    photos.push({
      full: thumb.getAttribute('data-full'),
      alt: thumb.alt || '',
      description: thumb.getAttribute('data-description') || ''
    });
  });

  // Убираем повторы фото, если главное фото совпадает с миниатюрой
  // Для этого создадим уникальный массив:
  const uniquePhotos = [];
  const srcSet = new Set();
  photos.forEach(photo => {
    if (!srcSet.has(photo.full)) {
      srcSet.add(photo.full);
      uniquePhotos.push(photo);
    }
  });

  // Для корректной работы главное фото имеет индекс 0 (если уникально)
  // Но нам нужно уметь менять главное фото на миниатюру и обратно
  // Сделаем выделение рамкой для выбранной миниатюры
  function clearThumbnailBorders() {
    thumbnails.forEach(t => t.style.borderColor = 'transparent');
  }

  // Найдем индекс выбранного фото по src
  function findPhotoIndexBySrc(src) {
    return uniquePhotos.findIndex(photo => photo.full === src);
  }

  // Состояние
  let currentIndex = 0;

  // Устанавливаем главное фото и выделяем миниатюру
  function setMainPhotoByIndex(index) {
    if (index < 0 || index >= uniquePhotos.length) return;
    currentIndex = index;
    mainPhoto.src = uniquePhotos[index].full;
    mainPhoto.alt = uniquePhotos[index].alt;
    clearThumbnailBorders();

    // Выделяем миниатюру, соответствующую mainPhoto
    thumbnails.forEach((thumb, i) => {
      if (thumb.getAttribute('data-full') === uniquePhotos[index].full) {
        thumb.style.borderColor = '#5a3f99'; // фиолетовая рамка
      }
    });
  }

  // Начальная установка — если совпадает, выделяем рамку
  setMainPhotoByIndex(findPhotoIndexBySrc(mainPhoto.src));

  // При клике по миниатюре меняем главное фото
  thumbnails.forEach(thumb => {
    thumb.style.cursor = 'pointer';

    thumb.addEventListener('click', () => {
      const src = thumb.getAttribute('data-full');
      const index = findPhotoIndexBySrc(src);
      if (index !== -1) {
        setMainPhotoByIndex(index);
      }
    });
  });

  // Открываем модальное окно по клику на главное фото
  mainPhoto.style.cursor = 'pointer';
  mainPhoto.addEventListener('click', () => {
    openModal(currentIndex);
  });

  // Открыть модал и показать фото по индексу
  function openModal(index) {
    if (index < 0 || index >= uniquePhotos.length) return;
    currentIndex = index;
    updateModalPhoto();
    modal.classList.remove('hidden');
    modal.setAttribute('aria-hidden', 'false');
    modalContent.focus();
    document.body.style.overflow = 'hidden'; // запрет прокрутки
  }

  // Закрыть модал
  function closeModal() {
    modal.classList.add('hidden');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  // Обновить фото в модальном окне
  function updateModalPhoto() {
    const photo = uniquePhotos[currentIndex];
    modalImage.src = photo.full;
    modalImage.alt = photo.alt || '';
    modalDescription.textContent = photo.description || '';
  }

  // Листать вперед
  function nextPhoto() {
    currentIndex = (currentIndex + 1) % uniquePhotos.length;
    updateModalPhoto();
  }

  // Листать назад
  function prevPhoto() {
    currentIndex = (currentIndex - 1 + uniquePhotos.length) % uniquePhotos.length;
    updateModalPhoto();
  }

  // Обработчики кнопок и оверлея
  btnClose.addEventListener('click', closeModal);
  modalOverlay.addEventListener('click', closeModal);
  btnPrev.addEventListener('click', prevPhoto);
  btnNext.addEventListener('click', nextPhoto);

  // Клавиатура — Esc закрыть, стрелки листать
  document.addEventListener('keydown', (event) => {
    if (modal.classList.contains('hidden')) return;

    if (event.key === 'Escape') {
      closeModal();
    } else if (event.key === 'ArrowLeft') {
      prevPhoto();
    } else if (event.key === 'ArrowRight') {
      nextPhoto();
    }
  });
});
