document.addEventListener('DOMContentLoaded', function() {
function updatePreview() {
    const title = document.getElementById('titleInput')?.value || '';
    const due = document.getElementById('dueDateInput')?.value || '';
    const labels = document.getElementById('labelsInput')?.value || '';
    const body = document.getElementById('bodyText')?.value || '';
    document.getElementById('logPreview').innerHTML = `
        <h4>${title || ''}</h4>
        <p><strong></strong> ${due || ''}</p>
        <p><strong></strong> ${labels || ''}</p>
        <p><strong></strong> ${body || ''}</p>
    `;
}
['titleInput', 'dueDateInput', 'labelsInput', 'bodyText'].forEach(id => {
    const element = document.getElementById(id);
    if (element) element.addEventListener('input', updatePreview);
});
updatePreview();
});