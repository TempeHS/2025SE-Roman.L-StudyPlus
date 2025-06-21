document.addEventListener("DOMContentLoaded", function() {
    const ctx = document.getElementById('taskProgressionChart');
    if (ctx) {
        new Chart(ctx.getContext('2d'), {
            type: 'line',
            data: {
                labels: window.progressionLabels || [],
                datasets: [{
                    label: 'Completed Tasks',
                    data: window.progressionStats || [],
                    borderColor: 'rgb(63, 63, 63)',
                    backgroundColor: 'rgb(154, 154, 154)',
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }
});