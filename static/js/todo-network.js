document.addEventListener('DOMContentLoaded', function () {
    if (!window.todos || !document.getElementById('todo-network')) return;

    // Create nodes from todos
    const nodes = new vis.DataSet(window.todos);

    // No edges for now (unless you want to show relationships)
    const edges = new vis.DataSet([]);

    const container = document.getElementById('todo-network');
    const data = { nodes, edges };
    const options = {
        nodes: {
            shape: 'box',
            font: { size: 16 }
        },
        layout: {
            improvedLayout: true
        }
    };
    new vis.Network(container, data, options);
});