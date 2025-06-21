document.addEventListener('DOMContentLoaded', function () {
    const deleteForms = document.querySelectorAll('.delete-todo-form');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function (event) {
            if (!confirm('Are you sure you want to delete this todo? This action cannot be undone.')) {
                event.preventDefault();
            }
        }, { once: true });
    });
});