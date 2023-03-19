window.addEventListener('DOMContentLoaded', () => {
    const graph = document.getElementById('graph');
    const websocket = new WebSocket('ws://localhost:8001/');
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
                plugins: {
                    legend: {display: false}
                },
                scales: {
                    x: {
                        type: 'timeseries',
                        title: {
                            display: true,
                            text: 'Time'
                        },
                        grid: {display: false}
                    },
                    y: {
                        type: 'linear',
                        min: 0,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Temperature (\'C)'
                        },
                        grid: {display: false}
                    }
                }
            }
        }
    );
    websocket.addEventListener('open', (ev) => {
        websocket.send(JSON.stringify({event: 'register'}))
    })
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