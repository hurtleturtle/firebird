window.addEventListener('DOMContentLoaded', on_load);

async function on_load() {
    const graph = document.getElementById('graph');
    const websocketURL = 'ws://' + window.location.hostname + ':8001';
    const websocket = new WebSocket(websocketURL);
    monitorConnections(websocket);
    getTemperature();
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
                    legend: {display: false},
                    title: {
                        display: true,
                        text: 'Firebird Monitoring'
                    }
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
            if (Array.isArray(events)) {
                let transformedEvents = transformDataToAxes(events);
                transformedEvents.forEach(event => addData(chart, event))
            }
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

function monitorConnections(websocket) {
    websocket.addEventListener('message', ({ data }) => {
        let event = JSON.parse(data);
        if ('connections' in event) {
            updateConnectionCount(event.connections);
        }
    })
}

function updateConnectionCount(count) {
    let connectionEl = document.querySelector('#connections > span');
    connectionEl.innerText = count;
}

async function getTemperature(url='/temperature') {
    let tempEl = document.querySelector('#temperature > span');
    let response = await fetch(url);
    let temp = await response.text();
    tempEl.innerText = temp + '\'C';
}