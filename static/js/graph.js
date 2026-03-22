

new Chart(document.getElementById("gameChart"), {
    type: 'bar',
    data: {
        labels: gameLabels,
        datasets: [{
            label: 'Participants',
            data: gameData
        }]
    },
    options: {
        responsive: true,

        plugins: {
            legend: {
                labels: {
                    font: {
                        size: 24
                    }
                }
            }
        },

        scales: {
            x: {
                ticks: {
                    font: {
                        size: 22
                    }
                }
            },
            y: {
                ticks: {
                    font: {
                        size: 22
                    }
                }
            }
        }
    }
});


new Chart(document.getElementById("branchChart"), {
    type: 'pie',
    data: {
        labels: branchLabels,
        datasets: [{
            data: branchData
        }]
    },
    options: {
        responsive: true,

        plugins: {
            legend: {
                labels: {
                    font: {
                        size: 24
                    }
                }
            }
        },
    }
});