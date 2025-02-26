document.addEventListener('DOMContentLoaded', () => {
    const employeeSelect = document.getElementById('employee');
    const shiftForm = document.getElementById('shift-form');

    // Загрузка списка сотрудников
    fetch('/employees')
        .then(response => response.json())
        .then(employees => {
            employees.forEach(employee => {
                const option = document.createElement('option');
                option.value = employee.id;
                option.textContent = `${employee.name} (${employee.position})`;
                employeeSelect.appendChild(option);
            });
        });

    // Отправка формы для назначения смены
    shiftForm.addEventListener('submit', event => {
        event.preventDefault();
        const employeeId = employeeSelect.value;
        const startTime = document.getElementById('start-time').value;
        const endTime = document.getElementById('end-time').value;

        fetch('/shifts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ employee_id: employeeId, start_time: startTime, end_time: endTime })
        }).then(response => {
            if (response.ok) {
                alert('Смена назначена!');
            } else {
                alert('Ошибка при назначении смены.');
            }
        });
    });
});