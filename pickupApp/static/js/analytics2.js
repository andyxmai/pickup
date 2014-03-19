function drawChart_2() {
    var data = google.visualization.arrayToDataTable(mySportsArr2);

    var options = {
      title: 'Sports Breakdown',
      is3D: true,
    };
    var chart = new google.visualization.PieChart(document.getElementById('piechart_3d_2'));
    var options = {
		colors: ['FF00CC',	'FF33FF',	'FF66FF',	'FF99FF',	'FFCCFF']
	};
    chart.draw(data, options);
}