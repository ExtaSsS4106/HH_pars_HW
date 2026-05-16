let params = {};

function get_params() {
    const timeOutFirstCircle = document.getElementById('timeOutFirstCircle').value;
    const timeOut = document.getElementById('timeOut').value;
    const countPages = document.getElementById('countPages').value;
    const delayFrom = document.getElementById('delayFrom').value;
    const delayTo = document.getElementById('delayTo').value;
    const vacancyId = document.getElementById('vacancyId').value;

    if (!timeOutFirstCircle || !timeOut || !countPages || !delayFrom || !delayTo) {
        console.error('Один или несколько элементов не найдены');
        return null;
    }

    params = {
        time_out_first_circle: parseInt(timeOutFirstCircle),  //改名 под Django
        time_out: parseInt(timeOut),
        pages: parseInt(countPages),
        delay_from: parseInt(delayFrom),
        delay_to: parseInt(delayTo),
        vacancy_id: vacancyId ? parseInt(vacancyId) : null
    };
    console.log('Параметры сохранены:', params);
    return params;
}

function reset() {
    document.getElementById('timeOutFirstCircle').value = '500';
    document.getElementById('timeOut').value = '150';
    document.getElementById('countPages').value = '0';
    document.getElementById('delayFrom').value = '40';
    document.getElementById('delayTo').value = '120';
    document.getElementById('vacancyId').value = '';
    get_params();
}

function startParsing() {
    const params = get_params();
    if (!params) {
        alert('Заполните все поля');
        return;
    }
    
    fetch('/api/start-parsing/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(params)
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            console.log('✅ Парсинг запущен', data.status);
            alert('Парсинг запущен');
        } else {
            alert('Ошибка: ' + (data.error || 'неизвестная ошибка'));
        }
    })
    .catch(err => console.error('Ошибка:', err));
}

function parsVacancy() {
    const vacancyInput = document.getElementById('vacancyIdInput');
    if (vacancyInput.style.display === 'none') {
        vacancyInput.style.display = 'block';
    } else {
        const params = get_params();
        if (params && params.vacancy_id) {
            fetch('/api/parse-single/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({vacancy_id: params.vacancy_id})
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    console.log('✅ Вакансия найдена', data.data);
                    alert('Вакансия найдена');
                } else {
                    alert('Ошибка: вакансия не найдена');
                }
            });
        } else {
            alert('Введите ID вакансии');
        }
    }
}

function stopParsing() {
    fetch('/api/stop-parsing/', {method: 'POST'})
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            console.log('⏹️ Парсинг остановлен');
            alert('Парсинг остановлен');
        }
    });
}

// Обновление статуса (опционально)
setInterval(() => {
    fetch('/api/parsing-status/')
    .then(res => res.json())
    .then(status => {
        const statusSpan = document.querySelector('#parsingStatus span');
        if (statusSpan) {
            statusSpan.textContent = status.status === 'running' ? '🟢 Выполняется' : '🔴 Остановлен';
            statusSpan.className = `status-badge status-${status.status}`;
        }
    });
}, 3000);