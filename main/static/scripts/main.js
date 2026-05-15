const ctx = document.getElementById('myChart');
let currentInterval = null;
let currentData = { data: [], vacancies_list: [] };
let currentPage = 1;
let currentCity = 'Все города';
let currentProfession = 'Все профессии';

let myChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: [],
    datasets: [{
      label: 'Количество вакансий',
      data: [],
      backgroundColor: [
        'rgba(255, 99, 132, 0.7)',
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 206, 86, 0.7)',
        'rgba(75, 192, 192, 0.7)',
        'rgba(153, 102, 255, 0.7)',
        'rgba(255, 159, 64, 0.7)'
      ],
      borderColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 206, 86)',
        'rgb(75, 192, 192)',
        'rgb(153, 102, 255)',
        'rgb(255, 159, 64)'
      ],
      borderWidth: 1
    }]
  },
  options: {
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#333'
        }
      }
    },
    scales: {
      x: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Количество вакансий',
          color: '#666'
        }
      },
      y: {
        title: {
          display: true,
          text: 'Категории',
          color: '#666'
        }
      }
    }
  }
});

function stopAnimation() {
  if (currentInterval) {
    clearInterval(currentInterval);
    currentInterval = null;
  }
}

function animateChart(items, text = 'Количество вакансий') {
  if (!items || items.length === 0) return;
  
  stopAnimation();
  
  myChart.data.labels = [];
  myChart.data.datasets[0].data = [];
  myChart.data.datasets[0].label = text;
  myChart.update();
  
  let step = 0;
  currentInterval = setInterval(() => {
    if (step < items.length) {
      myChart.data.labels.push(items[step].name);
      myChart.data.datasets[0].data.push(items[step].value);
      myChart.update();
      step++;
    } else {
      clearInterval(currentInterval);
      currentInterval = null;
    }
  }, 40);
}

function updateVacancyCards(vacancies) {
  const container = document.getElementById('vacancyContainer');
  container.innerHTML = '';
  
  if (!vacancies || vacancies.length === 0) {
    container.innerHTML = `
      <div class="card-holder">
        <div class="card mb-2 bg-dark text-white border-secondary w-100">
          <div class="card-body text-center">
            <h5 class="card-title">Нет вакансий</h5>
            <p class="card-text">По вашему запросу ничего не найдено</p>
          </div>
        </div>
      </div>
    `;
    return;
  }
  
  vacancies.forEach(vac => {
    const cardHolder = document.createElement('div');
    cardHolder.className = 'card-holder';
    cardHolder.innerHTML = `
      <div class="card mb-2 bg-dark text-white border-secondary w-100">
        <div class="card-body">
          <h5 class="card-title">${vac.title || 'Без названия'}</h5>
          <p class="card-text">Компания: ${vac.company || 'Не указана'}  
            <span class="badge text-bg-success">Зарплата: ${vac.salary || 'Не указана'}</span>  
            <span class="badge text-bg-danger">${vac.location || 'Не указан'}</span>
          </p>
          <div class="d-flex flex-row justify-content-between align-items-center mb-2">
            <a href="${vac.link}" target="_blank" class="btn btn-sm btn-outline-primary">Подробнее</a>
            <span class="text-secondary" style="font-weight: 300; font-size: 11px;">${vac.publicationTime}</span>
          </div>
        </div>
      </div>
    `;
    container.appendChild(cardHolder);
  });
  const spinner = document.getElementById('spinner__');
  spinner.innerHTML = ``;
}

function insertLoading() {
  const spinner = document.getElementById('spinner__');
  const container = document.getElementById('vacancyContainer');
  spinner.innerHTML = `          <div class="spinner-border text-secondary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>`;
  container.innerHTML = `        
    <div class="card mb-2 bg-dark text-white border-secondary" style="width: 90%;">
      <div class="card-body">
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 75%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
      </div>
    </div>
    <div class="card mb-2 bg-dark text-white border-secondary" style="width: 90%;">
      <div class="card-body">
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 75%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
      </div>
    </div>
    <div class="card mb-2 bg-dark text-white border-secondary" style="width: 90%;">
      <div class="card-body">
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 75%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
      </div>
    </div>
    <div class="card mb-2 bg-dark text-white border-secondary" style="width: 90%;">
      <div class="card-body">
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 75%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
      </div>
    </div>
    <div class="card mb-2 bg-dark text-white border-secondary" style="width: 90%;">
      <div class="card-body">
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 75%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
      </div>
    </div>
    <div class="card mb-2 bg-dark text-white border-secondary" style="width: 90%;">
      <div class="card-body">
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 75%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
      </div>
    </div>
    <div class="card mb-2 bg-dark text-white border-secondary" style="width: 90%;">
      <div class="card-body">
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 75%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
      </div>
    </div>
    <div class="card mb-2 bg-dark text-white border-secondary" style="width: 90%;">
      <div class="card-body">
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 75%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
      </div>
    </div>
    <div class="card mb-2 bg-dark text-white border-secondary" style="width: 90%;">
      <div class="card-body">
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 75%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
      </div>
    </div>
    <div class="card mb-2 bg-dark text-white border-secondary" style="width: 90%;">
      <div class="card-body">
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 75%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
      </div>
    </div>
    <div class="card mb-2 bg-dark text-white border-secondary" style="width: 90%;">
      <div class="card-body">
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 75%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
      </div>
    </div>
    <div class="card mb-2 bg-dark text-white border-secondary" style="width: 90%;">
      <div class="card-body">
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 75%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
        <p class="placeholder-glow">
          <span class="placeholder" style="width: 25%;"></span>
        </p>
      </div>
    </div>
    `;
}

function updatePaginationControls(pagination) {
  const paginationContainer = document.getElementById('paginationControls');
  if (!paginationContainer) return;
  
  if (!pagination || pagination.total_pages <= 1) {
    paginationContainer.innerHTML = '';
    return;
  }
  
  let html = `
    <nav aria-label="Page navigation">
      <ul class="pagination justify-content-center">
  `;
  
  // Кнопка "Назад"
  if (pagination.has_previous) {
    html += `
      <li class="page-item">
        <a class="page-link" href="#" onclick="goToPage(${pagination.current_page - 1}); return false;">
          ← Назад
        </a>
      </li>
    `;
  } else {
    html += `
      <li class="page-item disabled">
        <a class="page-link" href="#">← Назад</a>
      </li>
    `;
  }
  
  // Номера страниц
  const startPage = Math.max(1, pagination.current_page - 2);
  const endPage = Math.min(pagination.total_pages, pagination.current_page + 2);
  
  if (startPage > 1) {
    html += `
      <li class="page-item">
        <a class="page-link" href="#" onclick="goToPage(1); return false;">1</a>
      </li>
    `;
    if (startPage > 2) {
      html += `<li class="page-item disabled"><a class="page-link" href="#">...</a></li>`;
    }
  }
  
  for (let i = startPage; i <= endPage; i++) {
    if (i === pagination.current_page) {
      html += `
        <li class="page-item active" aria-current="page">
          <a class="page-link" href="#">${i}</a>
        </li>
      `;
    } else {
      html += `
        <li class="page-item">
          <a class="page-link" href="#" onclick="goToPage(${i}); return false;">${i}</a>
        </li>
      `;
    }
  }
  
  if (endPage < pagination.total_pages) {
    if (endPage < pagination.total_pages - 1) {
      html += `<li class="page-item disabled"><a class="page-link" href="#">...</a></li>`;
    }
    html += `
      <li class="page-item">
        <a class="page-link" href="#" onclick="goToPage(${pagination.total_pages}); return false;">
          ${pagination.total_pages}
        </a>
      </li>
    `;
  }
  
  // Кнопка "Вперед"
  if (pagination.has_next) {
    html += `
      <li class="page-item">
        <a class="page-link" href="#" onclick="goToPage(${pagination.current_page + 1}); return false;">
          Вперед →
        </a>
      </li>
    `;
  } else {
    html += `
      <li class="page-item disabled">
        <a class="page-link" href="#">Вперед →</a>
      </li>
    `;
  }
  
  html += `
      </ul>
    </nav>
  `;
  
  paginationContainer.innerHTML = html;
}

function goToPage(page) {
  currentPage = page;
  if (currentCity !== 'Все города' || currentProfession !== 'Все профессии') {
    loadFilteredData(currentCity, currentProfession, page);
  } else {
    loadDataWithPage(page);
  }
  
  // Прокрутка к секции с вакансиями
  setTimeout(() => {
    const section = document.getElementById('vacancySection');
    if (section) {
      section.scrollIntoView({ behavior: 'smooth' });
    }
  }, 200);
}

function updateChart() {
  const dataArray = currentData.data || [];
  
  if (!dataArray || dataArray.length === 0) {
    console.log('Нет данных для отображения');
    myChart.data.labels = [];
    myChart.data.datasets[0].data = [];
    myChart.data.datasets[0].label = 'Нет данных';
    myChart.update();
    updateVacancyCards([]);
    updatePaginationControls(null);
    return;
  }

  const city = document.getElementById('city').textContent;
  const profession = document.getElementById('profession').textContent;
  console.log('📊 Город:', city, '| Профессия:', profession);
  
  let items = [];
  let text = 'Количество вакансий';

  if (city === 'Все города' && profession === 'Все профессии') {
    const profMap = {};
    text = 'Количество вакансий по всем городам и профессиям';
    
    dataArray.forEach(cityData => {
      cityData.professions.forEach(prof => {
        if (!profMap[prof.profession]) {
          profMap[prof.profession] = 0;
        }
        profMap[prof.profession] += prof.count;
      });
    });
    
    for (let [name, value] of Object.entries(profMap)) {
      items.push({ name, value });
    }
  } 
  else if (city === 'Все города') {
    const cityMap = {};
    text = `Количество вакансий для профессии "${profession}" по всем городам`;
    
    dataArray.forEach(cityData => {
      const profData = cityData.professions.find(p => p.profession === profession);
      if (profData) {
        if (!cityMap[cityData.city]) {
          cityMap[cityData.city] = 0;
        }
        cityMap[cityData.city] += profData.count;
      }
    });
    
    for (let [name, value] of Object.entries(cityMap)) {
      items.push({ name, value });
    }
  }
  else if (profession === 'Все профессии') {
    const cityData = dataArray.find(d => d.city === city);
    if (cityData) {
      text = `Количество вакансий в городе "${city}" по всем профессиям`;
      
      cityData.professions.forEach(prof => {
        items.push({ name: prof.profession, value: prof.count });
      });
    }
  }
  else {
    const cityData = dataArray.find(d => d.city === city);
    if (cityData) {
      const profData = cityData.professions.find(p => p.profession === profession);
      if (profData) {
        text = `Количество вакансий для профессии "${profession}" в городе "${city}"`;
        
        profData.groups.forEach(group => {
          items.push({ name: group.groupe, value: group.count });
        });
      }
    }
  }
  
  const allVacancies = currentData.vacancies_list || [];
  const pagination = currentData.pagination;
  
  if (items.length > 0) {
    items.sort((a, b) => b.value - a.value);
    animateChart(items, text);
  } else {
    stopAnimation();
    myChart.data.labels = [];
    myChart.data.datasets[0].data = [];
    myChart.data.datasets[0].label = 'Нет данных';
    myChart.update();
  }
  
  updateVacancyCards(allVacancies);
  updatePaginationControls(pagination);
}

async function loadDataWithPage(page = 1) {
  try {
    insertLoading();
    const response = await fetch(`/api/data/?page=${page}&per_page=10`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log('Данные из БД:', data);
    
    currentData = data;
    currentPage = page;
    updateChart();
  } catch (error) {
    console.error('Ошибка загрузки данных:', error);
    showError('Не удалось загрузить данные. Проверьте подключение к серверу.');
  }
}

async function loadFilteredData(city, profession, page = 1) {
  try {
    insertLoading();
    
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
    
    const csrftoken = getCookie('csrftoken');
    
    const response = await fetch(`/api/filtered-data/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({ city, profession, page, per_page: 10 })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('Отфильтрованные данные из БД:', data);
    
    currentData = data;
    currentCity = city;
    currentProfession = profession;
    currentPage = page;
    updateChart();
  } catch (error) {
    console.error('Ошибка загрузки отфильтрованных данных:', error);
    showError('Не удалось загрузить отфильтрованные данные.');
  }
}

function showError(message) {
  const container = document.getElementById('vacancyContainer');
  container.innerHTML = `
    <div class="alert alert-danger" role="alert">
      ${message}
    </div>
  `;
}

document.addEventListener('DOMContentLoaded', function() {
  const cityButton = document.getElementById('city');
  const professionButton = document.getElementById('profession');
  
  const cityItems = document.querySelectorAll('#cityDropdown .dropdown-item');
  cityItems.forEach(item => {
    item.addEventListener('click', function(e) {
      e.preventDefault();
      const value = this.getAttribute('data-value');
      const displayValue = value === 'all' ? 'Все города' : value;
      cityButton.textContent = displayValue;
      
      cityItems.forEach(i => i.classList.remove('active'));
      this.classList.add('active');
      
      currentCity = cityButton.textContent;
      currentProfession = professionButton.textContent;
      
      if (currentCity !== 'Все города' || currentProfession !== 'Все профессии') {
        loadFilteredData(currentCity, currentProfession, 1);
      } else {
        loadDataWithPage(1);
      }
      
      const bsDropdown = bootstrap.Dropdown.getInstance(cityButton);
      if (bsDropdown) bsDropdown.hide();
    });
  });
  
  const professionItems = document.querySelectorAll('#professionDropdown .dropdown-item');
  professionItems.forEach(item => {
    item.addEventListener('click', function(e) {
      e.preventDefault();
      const value = this.getAttribute('data-value');
      const displayValue = value === 'all' ? 'Все профессии' : value;
      professionButton.textContent = displayValue;
      
      professionItems.forEach(i => i.classList.remove('active'));
      this.classList.add('active');
      
      currentCity = cityButton.textContent;
      currentProfession = professionButton.textContent;
      
      if (currentCity !== 'Все города' || currentProfession !== 'Все профессии') {
        loadFilteredData(currentCity, currentProfession, 1);
      } else {
        loadDataWithPage(1);
      }
      
      const bsDropdown = bootstrap.Dropdown.getInstance(professionButton);
      if (bsDropdown) bsDropdown.hide();
    });
  });
  
  document.getElementById('city').textContent = 'Все города';
  document.getElementById('profession').textContent = 'Все профессии';
  loadDataWithPage(1);
});