document.getElementById('categoryBurger').addEventListener('click', function() {
  this.classList.toggle('active');
  const menu = document.getElementById('categoryMenu');
  const expanded = this.getAttribute('aria-expanded') === 'true';
  this.setAttribute('aria-expanded', String(!expanded));
  if (menu.hasAttribute('hidden')) {
    menu.removeAttribute('hidden');
  } else {
    menu.setAttribute('hidden', '');
  }
});
