// Main application logic
let priceChart, garageDetailChart, comparisonChart;

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    initializeSummaryCards();
    initializeCharts();
    initializeFilters();
    populateDataTable();
    updateLastUpdated();
});

// Initialize summary cards with latest data
function initializeSummaryCards() {
    const latest = DataHelper.getLatest();
    const first = DataHelper.getFirst();

    // Garage prices
    document.getElementById('avgGaragePrice').textContent = formatCurrency(latest.garages.avg);
    const garageChange = DataHelper.calculateChange(first.garages.avg, latest.garages.avg);
    document.getElementById('garagePriceChange').textContent = `${garageChange > 0 ? '+' : ''}${garageChange}% od ${first.year}`;
    document.getElementById('garagePriceChange').className = garageChange >= 0 ? 'change positive' : 'change negative';

    // Apartment prices
    document.getElementById('avgApartmentPrice').textContent = formatCurrency(latest.apartments.avg) + '/m²';
    const apartmentChange = DataHelper.calculateChange(first.apartments.avg, latest.apartments.avg);
    document.getElementById('apartmentPriceChange').textContent = `${apartmentChange > 0 ? '+' : ''}${apartmentChange}% od ${first.year}`;
    document.getElementById('apartmentPriceChange').className = apartmentChange >= 0 ? 'change positive' : 'change negative';

    // House prices
    document.getElementById('avgHousePrice').textContent = formatCurrency(latest.houses.avg) + '/m²';
    const houseChange = DataHelper.calculateChange(first.houses.avg, latest.houses.avg);
    document.getElementById('housePriceChange').textContent = `${houseChange > 0 ? '+' : ''}${houseChange}% od ${first.year}`;
    document.getElementById('housePriceChange').className = houseChange >= 0 ? 'change positive' : 'change negative';

    // Garage statistics
    document.getElementById('minGaragePrice').textContent = formatCurrency(latest.garages.min);
    document.getElementById('maxGaragePrice').textContent = formatCurrency(latest.garages.max);
    document.getElementById('medianGaragePrice').textContent = formatCurrency(latest.garages.median);
    document.getElementById('garageGrowth').textContent = `+${garageChange}%`;
}

// Initialize all charts
function initializeCharts() {
    createPriceChart();
    createGarageDetailChart();
    createComparisonChart();
}

// Main price trend chart
function createPriceChart() {
    const ctx = document.getElementById('priceChart').getContext('2d');
    const years = DataHelper.getYears();

    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: years,
            datasets: [
                {
                    label: 'Garaže (€)',
                    data: DataHelper.getPropertyData('garages'),
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Stanovanja (€/m²)',
                    data: DataHelper.getPropertyData('apartments'),
                    borderColor: '#16a34a',
                    backgroundColor: 'rgba(22, 163, 74, 0.1)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Hiše (€/m²)',
                    data: DataHelper.getPropertyData('houses'),
                    borderColor: '#ea580c',
                    backgroundColor: 'rgba(234, 88, 12, 0.1)',
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            label += formatCurrency(context.parsed.y);
                            return label;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return formatCurrency(value);
                        }
                    }
                }
            }
        }
    });
}

// Detailed garage chart with min/max/median
function createGarageDetailChart() {
    const ctx = document.getElementById('garageDetailChart').getContext('2d');
    const years = DataHelper.getYears();
    const garageData = realEstateData.years;

    garageDetailChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: years,
            datasets: [
                {
                    label: 'Maksimalna cena',
                    data: garageData.map(d => d.garages.max),
                    borderColor: '#dc2626',
                    backgroundColor: 'rgba(220, 38, 38, 0.1)',
                    borderDash: [5, 5],
                    tension: 0.4,
                    fill: false
                },
                {
                    label: 'Povprečna cena',
                    data: garageData.map(d => d.garages.avg),
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.2)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 3
                },
                {
                    label: 'Mediana',
                    data: garageData.map(d => d.garages.median),
                    borderColor: '#7c3aed',
                    backgroundColor: 'rgba(124, 58, 237, 0.1)',
                    borderDash: [3, 3],
                    tension: 0.4,
                    fill: false
                },
                {
                    label: 'Minimalna cena',
                    data: garageData.map(d => d.garages.min),
                    borderColor: '#16a34a',
                    backgroundColor: 'rgba(22, 163, 74, 0.1)',
                    borderDash: [5, 5],
                    tension: 0.4,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            label += formatCurrency(context.parsed.y);
                            return label;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return formatCurrency(value);
                        }
                    }
                }
            }
        }
    });
}

// Comparison chart showing growth percentage
function createComparisonChart() {
    const ctx = document.getElementById('comparisonChart').getContext('2d');
    const first = DataHelper.getFirst();
    const years = DataHelper.getYears();

    // Calculate percentage growth from first year for each property type
    const garageGrowth = realEstateData.years.map(d =>
        ((d.garages.avg - first.garages.avg) / first.garages.avg * 100)
    );
    const apartmentGrowth = realEstateData.years.map(d =>
        ((d.apartments.avg - first.apartments.avg) / first.apartments.avg * 100)
    );
    const houseGrowth = realEstateData.years.map(d =>
        ((d.houses.avg - first.houses.avg) / first.houses.avg * 100)
    );

    comparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: years,
            datasets: [
                {
                    label: 'Garaže',
                    data: garageGrowth,
                    backgroundColor: 'rgba(37, 99, 235, 0.7)',
                    borderColor: '#2563eb',
                    borderWidth: 1
                },
                {
                    label: 'Stanovanja',
                    data: apartmentGrowth,
                    backgroundColor: 'rgba(22, 163, 74, 0.7)',
                    borderColor: '#16a34a',
                    borderWidth: 1
                },
                {
                    label: 'Hiše',
                    data: houseGrowth,
                    backgroundColor: 'rgba(234, 88, 12, 0.7)',
                    borderColor: '#ea580c',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            label += context.parsed.y.toFixed(1) + '%';
                            return label;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    },
                    title: {
                        display: true,
                        text: 'Rast cen od ' + first.year + ' (%)'
                    }
                }
            }
        }
    });
}

// Initialize filter functionality
function initializeFilters() {
    // Property type checkboxes
    const checkboxes = document.querySelectorAll('input[name="propertyType"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateChartVisibility);
    });

    // Time range selector
    const timeRangeSelect = document.getElementById('timeRange');
    timeRangeSelect.addEventListener('change', updateTimeRange);
}

// Update chart visibility based on selected property types
function updateChartVisibility() {
    const checkboxes = document.querySelectorAll('input[name="propertyType"]');
    const selected = {
        garages: false,
        apartments: false,
        houses: false
    };

    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            selected[checkbox.value] = true;
        }
    });

    // Update main chart
    priceChart.data.datasets[0].hidden = !selected.garages;
    priceChart.data.datasets[1].hidden = !selected.apartments;
    priceChart.data.datasets[2].hidden = !selected.houses;
    priceChart.update();

    // Update comparison chart
    comparisonChart.data.datasets[0].hidden = !selected.garages;
    comparisonChart.data.datasets[1].hidden = !selected.apartments;
    comparisonChart.data.datasets[2].hidden = !selected.houses;
    comparisonChart.update();
}

// Update charts based on time range selection
function updateTimeRange() {
    const timeRange = document.getElementById('timeRange').value;
    let filteredData = realEstateData.years;

    switch(timeRange) {
        case '1990s':
            filteredData = realEstateData.years.filter(d => d.year >= 1990 && d.year < 2000);
            break;
        case '2000s':
            filteredData = realEstateData.years.filter(d => d.year >= 2000 && d.year < 2010);
            break;
        case '2010s':
            filteredData = realEstateData.years.filter(d => d.year >= 2010 && d.year < 2020);
            break;
        case '2020s':
            filteredData = realEstateData.years.filter(d => d.year >= 2020);
            break;
        default:
            filteredData = realEstateData.years;
    }

    updateChartsWithData(filteredData);
}

// Update all charts with filtered data
function updateChartsWithData(data) {
    const years = data.map(d => d.year);

    // Update main price chart
    priceChart.data.labels = years;
    priceChart.data.datasets[0].data = data.map(d => d.garages.avg);
    priceChart.data.datasets[1].data = data.map(d => d.apartments.avg);
    priceChart.data.datasets[2].data = data.map(d => d.houses.avg);
    priceChart.update();

    // Update garage detail chart
    garageDetailChart.data.labels = years;
    garageDetailChart.data.datasets[0].data = data.map(d => d.garages.max);
    garageDetailChart.data.datasets[1].data = data.map(d => d.garages.avg);
    garageDetailChart.data.datasets[2].data = data.map(d => d.garages.median);
    garageDetailChart.data.datasets[3].data = data.map(d => d.garages.min);
    garageDetailChart.update();

    // Update comparison chart
    const first = data[0];
    comparisonChart.data.labels = years;
    comparisonChart.data.datasets[0].data = data.map(d =>
        ((d.garages.avg - first.garages.avg) / first.garages.avg * 100)
    );
    comparisonChart.data.datasets[1].data = data.map(d =>
        ((d.apartments.avg - first.apartments.avg) / first.apartments.avg * 100)
    );
    comparisonChart.data.datasets[2].data = data.map(d =>
        ((d.houses.avg - first.houses.avg) / first.houses.avg * 100)
    );
    comparisonChart.update();
}

// Populate the data table
function populateDataTable() {
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = '';

    realEstateData.years.forEach(yearData => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${yearData.year}</td>
            <td>${formatCurrency(yearData.garages.avg)}</td>
            <td>${formatCurrency(yearData.apartments.avg)}</td>
            <td>${formatCurrency(yearData.houses.avg)}</td>
        `;
        tbody.appendChild(row);
    });
}

// Update last updated date
function updateLastUpdated() {
    const date = new Date(realEstateData.metadata.lastUpdated);
    document.getElementById('lastUpdated').textContent = date.toLocaleDateString('sl-SI');
}

// Utility function to format currency
function formatCurrency(value) {
    return new Intl.NumberFormat('sl-SI', {
        style: 'currency',
        currency: 'EUR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(value);
}
