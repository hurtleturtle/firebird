window.addEventListener('DOMContentLoaded', on_load);

async function on_load() {
    const graph = document.getElementById('graph');
    const websocket = new WebSocket('ws://localhost:8001/');
    let chartData = await initialiseGraphData();
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

async function initialiseGraphData() {
    const url = '/init';
    let response = await fetch(url);
    let data = await response.json();
    return transformDataToAxes(data);
}

function transformDataToAxes(events) {
    let transformedEvents = []

    events.forEach(event => {
        let date = new Date(event.timestamp);
        let newData = {x: date, y: event.temperature};
        transformedEvents.push(newData);
    })
    console.log(events);
    console.log(transformedEvents);
    return transformedEvents
}

function drawGraph(chart, websocket) {
    websocket.addEventListener('message', ({ data }) => {
        let newData = transformDataToAxes(data);
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