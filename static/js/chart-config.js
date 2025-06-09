document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('taskPieChart');
    if (!ctx) return;
    const data = {
        labels: ['Completed', 'Ongoing', 'Overdue'],
        datasets: [{
            label: 'Tasks',
            data: [window.completed, window.ongoing, window.overdue],
            backgroundColor: [
                'rgb(75, 220, 109)',   // green
                'rgb(210, 172, 58)',   // yellow
                'rgb(207, 69, 83)'    // red
            ],
            hoverOffset: 4
        }]
    };
    const config = {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    };
    new Chart(ctx, config);
});