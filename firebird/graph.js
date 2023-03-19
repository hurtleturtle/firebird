window.addEventListener('DOMContentLoaded', () => {
    const graph = document.getElementById('graph');
    const websocket = new WebSocket('ws://localhost:8001/')
    const values = [
        {x: 10, y: 1},
        {x: 20, y: 2},
        {x: 30, y: 3},
        {x: 40, y: 4},
        {x: 50, y: 5},
    ]
    const chart = new Chart(
        graph,
        {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Nuts',
                    pointRadius: 5,
                    pointBackgroundColor: 'rgba(0, 0, 255, 1)',
                    data: []
                }]
            },
            options: {
                legend: {display: false},
                scales: {
                    x: {
                        type: 'timeseries',
                        title: {
                            display: true,
                            text: 'Time'
                        }
                    },
                    y: {
                        type: 'linear',
                        min: 0,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Temperature (\'C)'
                        }
                    }
                }
            }
        }
    )
    drawGraph(chart, websocket);
});

function drawGraph(chart, websocket) {
    websocket.addEventListener('message', ({ data }) => {
        const event = JSON.parse(data);
        let date = new Date(event.timestamp)
        let newData = {x: date, y: event.temperature}
        console.log(newData)
        addData(chart, newData)
    });
}

function addData(chart, data) {
    // chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}