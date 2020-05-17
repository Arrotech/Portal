// Load google charts
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

// Draw the chart and set the chart values
function drawChart() {
  var data = google.visualization.arrayToDataTable([
  ['Task', 'Hours per Day'],
  ['Total units', 8],
  ['Registered units', 7],
  ['Compulsory units', 6],
  ['Optional units', 2],
  ['Unregistered unit', 1],
  ['Minimum units', 52]
]);

  // Optional; add a title and set the width and height of the chart
  var options = {'title':'Units registration', 'width':520, 'height':400};

  // Display the chart inside the <div> element with id="piechart"
  var chart = new google.visualization.PieChart(document.getElementById('piechart'));
  chart.draw(data, options);
}