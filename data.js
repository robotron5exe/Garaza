// Real Estate Price Data for Maribor
// All prices are in EUR
// Apartment and house prices are per m²
// Garage prices are total price

const realEstateData = {
    // Array of yearly data points
    years: [
        {
            year: 1990,
            garages: {
                avg: 3500,
                min: 2500,
                max: 5000,
                median: 3400
            },
            apartments: {
                avg: 400,
                min: 300,
                max: 600,
                median: 390
            },
            houses: {
                avg: 350,
                min: 250,
                max: 500,
                median: 340
            }
        },
        {
            year: 1995,
            garages: {
                avg: 4200,
                min: 3000,
                max: 6000,
                median: 4100
            },
            apartments: {
                avg: 480,
                min: 350,
                max: 700,
                median: 470
            },
            houses: {
                avg: 420,
                min: 300,
                max: 600,
                median: 410
            }
        },
        {
            year: 2000,
            garages: {
                avg: 5500,
                min: 4000,
                max: 8000,
                median: 5400
            },
            apartments: {
                avg: 650,
                min: 500,
                max: 950,
                median: 640
            },
            houses: {
                avg: 580,
                min: 420,
                max: 850,
                median: 570
            }
        },
        {
            year: 2005,
            garages: {
                avg: 8500,
                min: 6000,
                max: 12000,
                median: 8300
            },
            apartments: {
                avg: 1100,
                min: 850,
                max: 1500,
                median: 1080
            },
            houses: {
                avg: 950,
                min: 700,
                max: 1350,
                median: 940
            }
        },
        {
            year: 2008,
            garages: {
                avg: 12000,
                min: 8500,
                max: 16000,
                median: 11800
            },
            apartments: {
                avg: 1650,
                min: 1300,
                max: 2200,
                median: 1620
            },
            houses: {
                avg: 1400,
                min: 1050,
                max: 1900,
                median: 1380
            }
        },
        {
            year: 2010,
            garages: {
                avg: 10500,
                min: 7500,
                max: 14000,
                median: 10300
            },
            apartments: {
                avg: 1400,
                min: 1100,
                max: 1850,
                median: 1380
            },
            houses: {
                avg: 1200,
                min: 900,
                max: 1600,
                median: 1180
            }
        },
        {
            year: 2012,
            garages: {
                avg: 9500,
                min: 7000,
                max: 13000,
                median: 9400
            },
            apartments: {
                avg: 1250,
                min: 950,
                max: 1650,
                median: 1230
            },
            houses: {
                avg: 1050,
                min: 800,
                max: 1450,
                median: 1040
            }
        },
        {
            year: 2015,
            garages: {
                avg: 10200,
                min: 7500,
                max: 14000,
                median: 10000
            },
            apartments: {
                avg: 1350,
                min: 1050,
                max: 1800,
                median: 1330
            },
            houses: {
                avg: 1150,
                min: 850,
                max: 1550,
                median: 1140
            }
        },
        {
            year: 2018,
            garages: {
                avg: 13500,
                min: 10000,
                max: 18000,
                median: 13300
            },
            apartments: {
                avg: 1750,
                min: 1400,
                max: 2300,
                median: 1720
            },
            houses: {
                avg: 1500,
                min: 1150,
                max: 2000,
                median: 1480
            }
        },
        {
            year: 2020,
            garages: {
                avg: 15000,
                min: 11000,
                max: 20000,
                median: 14800
            },
            apartments: {
                avg: 1950,
                min: 1550,
                max: 2550,
                median: 1920
            },
            houses: {
                avg: 1680,
                min: 1300,
                max: 2200,
                median: 1660
            }
        },
        {
            year: 2022,
            garages: {
                avg: 17500,
                min: 13000,
                max: 23000,
                median: 17200
            },
            apartments: {
                avg: 2250,
                min: 1800,
                max: 2900,
                median: 2220
            },
            houses: {
                avg: 1950,
                min: 1500,
                max: 2550,
                median: 1920
            }
        },
        {
            year: 2024,
            garages: {
                avg: 19500,
                min: 14500,
                max: 26000,
                median: 19200
            },
            apartments: {
                avg: 2450,
                min: 1950,
                max: 3200,
                median: 2420
            },
            houses: {
                avg: 2150,
                min: 1650,
                max: 2800,
                median: 2120
            }
        }
    ],

    // Metadata
    metadata: {
        lastUpdated: '2024-11-09',
        currency: 'EUR',
        source: 'Sample data - replace with real data from GURS, SURS, or nepremicnine.net',
        notes: [
            'Garage prices represent total price for a standard garage (15-20m²)',
            'Apartment and house prices are per square meter',
            'Prices are adjusted for inflation and shown in current EUR value',
            'Data represents average market prices in Maribor city center and surrounding areas'
        ]
    }
};

// Helper functions to work with the data
const DataHelper = {
    // Get all years
    getYears() {
        return realEstateData.years.map(d => d.year);
    },

    // Get data for a specific property type
    getPropertyData(propertyType) {
        return realEstateData.years.map(d => d[propertyType].avg);
    },

    // Get data for a specific year range
    getDataInRange(startYear, endYear) {
        return realEstateData.years.filter(d => d.year >= startYear && d.year <= endYear);
    },

    // Calculate percentage change
    calculateChange(startValue, endValue) {
        return ((endValue - startValue) / startValue * 100).toFixed(1);
    },

    // Get latest data
    getLatest() {
        return realEstateData.years[realEstateData.years.length - 1];
    },

    // Get first data
    getFirst() {
        return realEstateData.years[0];
    }
};
