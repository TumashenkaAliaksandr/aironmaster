document.addEventListener('DOMContentLoaded', () => {
    let page = 2;  // в template первая страница уже загружена
    let loading = false;
    const newsList = document.getElementById('news-list');
    const loadingIndicator = document.getElementById('loading');

    window.addEventListener('scroll', () => {
        if (loading) return;

        // Подгрузка за 300px до низа страницы
        if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight - 300) {
            loading = true;
            loadingIndicator.style.display = 'block';

            fetch(`?page=${page}`, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(response => response.json())
            .then(data => {
                loadingIndicator.style.display = 'none';
                if (data.html) {
                    newsList.insertAdjacentHTML('beforeend', data.html);
                }
                if (!data.has_next) {
                    window.removeEventListener('scroll', arguments.callee);
                } else {
                    page++;
                    loading = false;
                }
            })
            .catch(() => {
                loadingIndicator.style.display = 'none';
                loading = false;
            });
        }
    });
});
