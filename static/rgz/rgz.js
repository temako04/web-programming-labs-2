document.addEventListener('DOMContentLoaded', function () {
    loadStorageCells();
});

let cellsState = [];  // Хранение состояния ячеек

function loadStorageCells() {
    fetch('/api/storage_cells')
    .then(function(response) {
        return response.json();
    })
    .then(function(cells) {
        const container = document.getElementById('storage-container');
        container.innerHTML = '';  // Очищаем контейнер перед отрисовкой

        cellsState = cells;  // Обновляем состояние ячеек

        cells.forEach(function(cell) {
            const cellDiv = createCellDiv(cell);
            container.appendChild(cellDiv);
        });
    });
}

function createCellDiv(cell) {
    const cellDiv = document.createElement('div');
    cellDiv.classList.add('storage-cell');
    
    if (cell.is_reserved) {
        cellDiv.classList.add('reserved');
    } else {
        cellDiv.classList.add('available');
    }
    
    cellDiv.innerText = `${cell.cell_code}`;
    cellDiv.dataset.id = cell.id;  // Добавляем ID ячейки в атрибут для идентификации
    cellDiv.onclick = function() {
        handleCellClick(cell.id, cell.is_reserved);
    };

    return cellDiv;
}

function handleCellClick(cellId, isReserved) {
    if (isReserved) {
        cancelReservation(cellId);
    } else {
        reserveCell(cellId);
    }
}

function reserveCell(cellId) {
    fetch(`/api/reserve_cell/${cellId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        if (data.error) {
            alert(data.error);  // Показываем сообщение об ошибке

            // Если ошибка 401 (неавторизован), не обновляем состояние ячейки
            if (data.code === 401) {
                return;  // Прерываем выполнение функции
            }
        } else {
            alert(data.message);  // Сообщение об успешном бронировании
            updateCellState(cellId, true);  // Обновляем состояние ячейки
        }
    })
    .catch(function(error) {
        alert('Ошибка бронирования ячейки: ' + error.message);
    });
}

function cancelReservation(cellId) {
    fetch(`/api/cancel_reservation/${cellId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        if (data.error) {
            switch (data.code) {
                case 1:
                    alert('Вы должны быть авторизованы, чтобы отменить бронирование');
                    break;
                case 2:
                    alert('Пользователь не найден');
                    break;
                case 3:
                    alert('Вы не забронировали эту ячейку или она уже отменена');
                    break;
                case 4:
                    alert('Ошибка при отмене бронирования: ' + data.error);
                    break;
                default:
                    alert('Неизвестная ошибка');
            }
        } else {
            alert(data.message);  // Бронирование успешно отменено
            updateCellState(cellId, false);  // Перезагружаем список ячеек
        }
    })
    .catch(function(error) {
        alert('Ошибка при отмене бронирования: ' + error.message);
    });
}

function updateCellState(cellId, isReserved) {
    // Находим ячейку по ID в состоянии
    let cell = cellsState.find(function(c) { return c.id === cellId; });
    if (cell) {
        cell.is_reserved = isReserved;  // Обновляем состояние ячейки

        const container = document.getElementById('storage-container');
        const cellDiv = container.querySelector(`.storage-cell[data-id='${cellId}']`);

        // Обновляем визуальное состояние ячейки
        if (isReserved) {
            cellDiv.classList.remove('available');
            cellDiv.classList.add('reserved');
        } else {
            cellDiv.classList.remove('reserved');
            cellDiv.classList.add('available');
        }
    }
}

function logout() {
    fetch('/lab5/logout', { method: 'GET' })
    .then(function() {
        window.location.reload();
    });
}