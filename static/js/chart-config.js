// Pie chart
document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('taskPieChart');
    if (!ctx) return;
    const data = {
        labels: ['Completed', 'Ongoing', 'Overdue'],
        datasets: [{
            label: 'Tasks',
            data: [window.completed, window.ongoing, window.overdue],
            backgroundColor: [
                'rgb(63, 63, 63)',   // green
                'rgb(92, 92, 92)',   // yellow
                'rgb(154, 154, 154)'    // red
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