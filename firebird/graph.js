window.addEventListener('DOMContentLoaded', () => {
    const graph = document.getElementById('graph');
    const websocket = new WebSocket('ws://localhost:8001/')
    drawGraph(graph, websocket);
});

function drawGraph(graph, websocket) {
    websocket.addEventListener('message', ({ data }) => {
        const event = JSON.parse(data);
        var p = document.createElement('p')
        p.innerText = `${event.timestamp} - ${event.temperature}`
        graph.appendChild(p)
    });
}