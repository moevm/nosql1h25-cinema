const ctx = document.getElementById('statsChart').getContext('2d');
let chart;

function getColor(i) {
    const colors = [
        '#FF6384', '#36A2EB', '#FFCE56',
        '#4BC0C0', '#9966FF', '#FF9F40',
        '#00C853', '#D50000', '#AA00FF',
        '#0091EA', '#FF6D00', '#C51162'
    ];
    return colors[i % colors.length];
}

function countByKey(data, key) {
    const counts = {};
    data.forEach(film => {
        const value = film[key];
        if (Array.isArray(value)) {
            value.forEach(item => {
                if (typeof item === 'string') {
                    counts[item] = (counts[item] || 0) + 1;
                }
            });
        } else {
            if (typeof value === 'string' || typeof value === 'number') {
                counts[value] = (counts[value] || 0) + 1;
            }
        }
    });
    return counts;
}

function renderChart(counts, label) {
    const labels = Object.keys(counts);
    const values = Object.values(counts);
    const backgroundColors = labels.map((_, i) => getColor(i));

    if (chart) chart.destroy();

    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: `Количество фильмов по ${label}`,
                data: values,
                backgroundColor: backgroundColors,
                borderRadius: 6,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        precision: 0,
                        callback: value => Number.isInteger(value) ? value : '',
                        font: { size: 14 }
                    },
                    grid: {
                        drawTicks: true,
                        drawOnChartArea: true,
                        drawBorder: true
                    },
                    title: {
                        display: true,
                        text: 'Количество фильмов',
                        font: { size: 16 }
                    }
                },
                x: {
                    ticks: {
                        font: { size: 14 }
                    },
                    title: {
                        display: true,
                        text: label,
                        font: { size: 16 }
                    }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

async function fetchDataAndRender() {
    const selectedKey = document.getElementById('keySelector').value;
    const response = await fetch('/api/content');
    const fullData = await response.json();
    const counts = countByKey(fullData, selectedKey);
    renderChart(counts, selectedKey);
}

document.getElementById('keySelector').addEventListener('change', fetchDataAndRender);
fetchDataAndRender();
