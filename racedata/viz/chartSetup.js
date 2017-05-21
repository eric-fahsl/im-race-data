Highcharts.chart('container', {

    chart: {
        type: 'boxplot'
    },

    title: {
        text: 'Finish Times 2012 - 2016 by Ironman Races'
    },

    legend: {
        enabled: false
    },

    xAxis: {
        categories: ['Cozumel', 'Arizona', 'CDA'],
        title: {
            text: 'Race'
        }
    },

    yAxis: {
        title: {
            text: 'Finish Time (Hours)'
        },
        plotLines: []
    },

    series: [{
        name: 'Finish Time (Hours)',
        data: [
            [7.923, 11.7, 13.02, 14.456, 17],
            [7.741, 11.732, 13.084, 14.648, 17],

            [8.292, 12.054, 13.463, 14.838, 17]
        ],
        tooltip: {
            headerFormat: '<em>Race: {point.key}</em><br/>'
        }
    }, {
        name: 'Outlier',
        color: Highcharts.getOptions().colors[0],
        type: 'scatter',
        data: [ // x, y positions where 0 is the first category
            
        ],
        marker: {
            fillColor: 'white',
            lineWidth: 1,
            lineColor: Highcharts.getOptions().colors[0]
        },
        tooltip: {
            pointFormat: 'Observation: {point.y}'
        }
    }]

});