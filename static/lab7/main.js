function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(function (data) {
            return data.json();
        })
        .then(function (films) {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = ''; // Очищаем таблицу перед заполнением
            for (let i = 0; i < films.length; i++) {
                let tr = document.createElement('tr');

                let tdTitleRus = document.createElement('td'); // Русское название
                let tdTitle = document.createElement('td'); // Оригинальное название
                let tdYear = document.createElement('td'); // Год
                let tdActions = document.createElement('td'); // Действия

                // Заполняем русское название
                tdTitleRus.innerText = films[i].title_ru || '';

                // Заполняем оригинальное название курсивом в скобках
                if (films[i].title && films[i].title !== films[i].title_ru) {
                    tdTitle.innerHTML = `<i>(${films[i].title})</i>`;
                } else {
                    tdTitle.innerHTML = ''; // Если оригинальное название совпадает с русским или пустое
                }

                // Заполняем год
                tdYear.innerText = films[i].year || '';

                // Кнопки действий
                let editButton = document.createElement('button');
                editButton.innerText = 'редактировать';
                editButton.onclick = function () {
                    editFilm(i);
                };

                let delButton = document.createElement('button');
                delButton.innerText = 'удалить';
                delButton.onclick = function () {
                    deleteFilm(i, films[i].title_ru);
                };

                tdActions.append(editButton);
                tdActions.append(delButton);

                // Добавляем ячейки в строку
                tr.append(tdTitleRus);
                tr.append(tdTitle);
                tr.append(tdYear);
                tr.append(tdActions);

                // Добавляем строку в таблицу
                tbody.append(tr);
            }
        });
}



function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, { method: 'DELETE' })
        .then(function () {
            fillFilmList(); // Обновляем список фильмов
        });
}

function showModal() {
    document.getElementById('description-error').innerText = ''; // Очищаем сообщение об ошибке
    document.querySelector('div.modal').style.display = 'block';
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('title').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal();
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    };

    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(film)
    })
        .then(function (resp) {
            if (resp.ok) {
                fillFilmList(); // Обновляем список фильмов
                hideModal();
                return {};
            }
            return resp.json();
        })
        .then(function (errors) {
            if (errors.description) {
                document.getElementById('description-error').innerText = errors.description;
            }
        });
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
        .then(function (data) {
            return data.json();
        })
        .then(function (film) {
            document.getElementById('id').value = id;
            document.getElementById('title-ru').value = film.title_ru;
            document.getElementById('title').value = film.title;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
            showModal();
        });
}

// Заполняем список фильмов при загрузке страницы
fillFilmList();