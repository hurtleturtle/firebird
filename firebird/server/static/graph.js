window.addEventListener('DOMContentLoaded', on_load);

async function on_load() {
    const graph = document.getElementById('graph');
    const websocketURL = 'ws://' + window.location.hostname + ':8001';
    const websocket = new WebSocket(websocketURL);
    let chartData = await initialiseGraphData();
    const chart = new Chart(
        graph,
        {
            type: 'line',
            data: {
                datasets: [{
                    label: 'CPU',
                    pointRadius: 2.5,
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
                        type: 'time',
                        title: {
                            display: true,
                            text: 'Time'
                        },
                        time: {
                            unit: 'minute'
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

    return transformedEvents;
}

function drawGraph(chart, websocket) {
    websocket.addEventListener('message', ({ data }) => {
        let events = [];
        try {
            events = JSON.parse(data);
            let transformedEvents = transformDataToAxes(events);
            transformedEvents.forEach(event => addData(chart, event))
        }
        catch {
        }
            
    });
}

function addData(chart, data, max_data_points=100) {
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
        if (dataset.data.length > max_data_points) {
            dataset.data.shift();
        }
    });
    chart.update();
}