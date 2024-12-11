function fillFilmList() {
    fetch('/lab7/rest-api/films/') 
    .then(function (response) {
        return response.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        films.forEach(function (film) {
            let tr = document.createElement('tr');

            let tdTitleRus = document.createElement('td');
            let tdTitle = document.createElement('td'); // Оригинальное название
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            tdTitleRus.innerText = film.title_ru; // Русское название
            tdTitle.innerHTML = film.title ? `<i>(${film.title})</i>` : ''; // Оригинальное название в курсиве и в скобках
            tdYear.innerText = film.year;

            let editButton = document.createElement('button');
            editButton.innerText = 'Редактировать';
            editButton.onclick = function()  {
                editFilm(film.id); // Используем film.id
            }

            let delButton = document.createElement('button');
            delButton.innerText = 'Удалить';
            delButton.onclick = function() {
                deleteFilm(film.id, film.title_ru); // Используем film.id
            }
            
            tdActions.append(editButton);
            tdActions.append(delButton);

            tr.append(tdTitleRus);
            tr.append(tdTitle); 
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        });
    })
    .catch(error => console.error('Ошибка при загрузке списка фильмов:', error));
}

function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, { method: 'DELETE' })
        .then(function (response) {
            if (response.ok) {
                fillFilmList();
            } else {
                console.error('Ошибка при удалении фильма:', response.statusText);
            }
        })
        .catch(error => console.error('Ошибка:', error));
}

function showModal() {
    document.querySelector('div.modal').style.display = 'block';
    document.getElementById('description-error').innerText = ''; 
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title_ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal();
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title_ru').value,
        year: parseInt(document.getElementById('year').value), // Преобразуем в число
        description: document.getElementById('description').value
    };

    const url = id ? `/lab7/rest-api/films/${id}` : '/lab7/rest-api/films/';
    const method = id ? 'PUT' : 'POST';

    fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if (resp.ok) {
            fillFilmList();
            hideModal();
        } else {
            return resp.json().then(errors => {
                console.error('Ошибка сервера:', errors); // Логируем ошибку сервера
                displayErrors(errors);
            });
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}

function displayErrors(errors) {
    if (errors.error) {
        document.getElementById('description-error').innerText = errors.error;
    }
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (response) {
        return response.json();
    })
    .then(function (film) {
        document.getElementById('id').value = film.id;
        document.getElementById('title').value = film .title;
        document.getElementById('title_ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        showModal();
    })
    .catch(error => console.error('Ошибка при загрузке фильма для редактирования:', error));
}
