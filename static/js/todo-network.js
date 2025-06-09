document.addEventListener('DOMContentLoaded', function () {
    if (!window.todos || !document.getElementById('todo-network')) return;

    // Create nodes from todos
    const nodes = new vis.DataSet(window.todos);

    // Create edges for todos with the same label
    const edges = [];
    for (let i = 0; i < window.todos.length; i++) {
        for (let j = i + 1; j < window.todos.length; j++) {
            if (
                window.todos[i].label &&
                window.todos[j].label &&
                window.todos[i].label.trim().toLowerCase() === window.todos[j].label.trim().toLowerCase()
            ) {
                edges.push({
                    from: window.todos[i].id,
                    to: window.todos[j].id,
                    color: { color: '#888' },
                    dashes: true
                });
            }
        }
    }

    const container = document.getElementById('todo-network');
    const data = { nodes, edges: new vis.DataSet(edges) };
    const options = {
        nodes: {
            shape: 'circle',
            font: { size: 16 }
        },
        layout: {
            improvedLayout: true
        }
    };
    new vis.Network(container, data, options);
});