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

// ...existing code for pie chart...

// Progression Line Chart
if (window.chartLabels && window.chartData) {
    const ctxLine = document.getElementById('progressionLineChart').getContext('2d');
    new Chart(ctxLine, {
        type: 'line',
        data: {
            labels: window.chartLabels,
            datasets: [{
                label: 'Tasks Completed',
                data: window.chartData,
                borderColor: 'rgba(40, 167, 69, 1)',
                backgroundColor: 'rgba(40, 167, 69, 0.2)',
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}