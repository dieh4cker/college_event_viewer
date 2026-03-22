
const compactScreen = window.matchMedia("(max-width: 600px)");
const mediumScreen = window.matchMedia("(max-width: 900px)");

function getChartSizing() {
    if (compactScreen.matches) {
        return {
            legendFont: 12,
            axisFont: 11,
            legendBox: 12,
            pieLegendPosition: 'bottom'
        };
    }

    if (mediumScreen.matches) {
        return {
            legendFont: 16,
            axisFont: 14,
            legendBox: 14,
            pieLegendPosition: 'top'
        };
    }

    return {
        legendFont: 24,
        axisFont: 22,
        legendBox: 18,
        pieLegendPosition: 'top'
    };
}

function buildGameChartOptions() {
    const sizing = getChartSizing();

    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    boxWidth: sizing.legendBox,
                    font: {
                        size: sizing.legendFont
                    }
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    autoSkip: true,
                    maxRotation: 35,
                    minRotation: 0,
                    font: {
                        size: sizing.axisFont
                    }
                }
            },
            y: {
                ticks: {
                    font: {
                        size: sizing.axisFont
                    }
                }
            }
        }
    };
}

function buildBranchChartOptions() {
    const sizing = getChartSizing();

    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: sizing.pieLegendPosition,
                labels: {
                    boxWidth: sizing.legendBox,
                    font: {
                        size: sizing.legendFont
                    }
                }
            }
        }
    };
}

const gameChart = new Chart(document.getElementById("gameChart"), {
    type: 'bar',
    data: {
        labels: gameLabels,
        datasets: [{
            label: 'Participants',
            data: gameData
        }]
    },
    options: buildGameChartOptions()
});


const branchChart = new Chart(document.getElementById("branchChart"), {
    type: 'pie',
    data: {
        labels: branchLabels,
        datasets: [{
            data: branchData
        }]
    },
    options: buildBranchChartOptions()
});

function updateChartOptions() {
    gameChart.options = buildGameChartOptions();
    branchChart.options = buildBranchChartOptions();
    gameChart.update('none');
    branchChart.update('none');
}

[compactScreen, mediumScreen].forEach((mediaQuery) => {
    if (typeof mediaQuery.addEventListener === 'function') {
        mediaQuery.addEventListener('change', updateChartOptions);
        return;
    }

    mediaQuery.addListener(updateChartOptions);
});
