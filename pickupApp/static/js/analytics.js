
function drawChart() {
	var data = google.visualization.arrayToDataTable(mySportsArr);

	var options = {
	  title: 'My Sports Breakdown',
	  is3D: true,
	};
	var chart = new google.visualization.PieChart(document.getElementById('piechart_3d'));
	var options = {
		colors: ['#e0440e', '#e6693e', '#ec8f6e', '#f3b49f', '#f6c7b6']
	};
	chart.draw(data, options);
}