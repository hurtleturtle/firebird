window.addEventListener('DOMContentLoaded', on_load);

function on_load() {
    const graph = document.getElementById('graph');
    const websocket = new WebSocket('ws://localhost:8001/');
    const chartData = initialiseGraph();
    const chart = new Chart(
        graph,
        {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Nuts',
                    pointRadius: 5,
                    pointBackgroundColor: 'rgba(0, 0, 255, 1)',
                    data: chartData
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
}

function initialiseGraph() {
    const initData = new Request('/init');

    fetch(initData)
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            return data
        })
        .catch((error) => {
            console.log('Error: ', error);
        });

}

function drawGraph(chart, websocket) {
    websocket.addEventListener('message', ({ data }) => {
        const event = JSON.parse(data);
        console.log(event)
        let date = new Date(event.timestamp);
        let newData = {x: date, y: event.temperature};
        console.log(newData);
        addData(chart, newData);
    });
}

function addData(chart, data) {
    // chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}