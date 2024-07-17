google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawCharts);

function drawCharts() {
    var categoryCounts = JSON.parse(document.getElementById('categoryCounts').textContent);
    var ageDistribution = JSON.parse(document.getElementById('ageDistribution').textContent);

    drawCategoryChart(categoryCounts);
    drawAgeChart(ageDistribution);
}

function drawCategoryChart(categoryData) {
    var chartData = [['Categoría', 'Total']];
    categoryData.forEach(function(item) {
        chartData.push([item.categoria__nombre, item.total]);
    });

    var dataTable = google.visualization.arrayToDataTable(chartData);
    var options = {
        title: 'Cantidad de Usuarios por Categoría',
            fontSize: 15,
        width: 800,
        height: 400
    };

    var chart = new google.visualization.PieChart(document.getElementById('graficoCategorias'));
    chart.draw(dataTable, options);
}

function drawAgeChart(ageData) {
    var chartData = [['Categoría', 'Edad Promedio', { role: 'annotation' }]];
    
    var categoryAges = {};
    ageData.forEach(function(item) {
        var categoria = item.categoria__nombre;
        var edad = item.edad;
        
        if (!categoryAges[categoria]) {
            categoryAges[categoria] = { total: 0, count: 0 };
        }
        
        categoryAges[categoria].total += edad;
        categoryAges[categoria].count++;
    });
    
    for (var categoria in categoryAges) {
        if (categoryAges.hasOwnProperty(categoria)) {
            var promedioEdad = categoryAges[categoria].total / categoryAges[categoria].count;
            var totalPersonas = categoryAges[categoria].count;
            chartData.push([categoria, promedioEdad, totalPersonas.toString()]);
        }
    }
    var options = {
        title: 'Edad Promedio de Usuarios por Categoría',
            fontSize: 15, 
            bold: true,
        height: 400,
        hAxis: { title: 'Categoría' },
        vAxis: { title: 'Edad Promedio' },
        legend: { position: 'right', maxLines: 4 }, 
        colors: ['#3366CC'], 
        tooltip: { isHtml: true } 
    };
    
var dataTable = google.visualization.arrayToDataTable(chartData);
var chart = new google.visualization.ColumnChart(document.getElementById('graficoEdades'));
chart.draw(dataTable, options);
}