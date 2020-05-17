google.charts.load("current", { packages: ["bar"] });
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
  var data = google.visualization.arrayToDataTable([
    ["Year", "Semester 1", "Semester 2", "Semester 3"],
    ["2014", 78, 69, 72],
    ["2015", 71, 65, 68],
    ["2016", 66, 67, 65],
    ["2017", 68, 72, 70],
  ]);

  var options = {
    chart: {
      title: "Examination Performance",
      subtitle: "Semester 1, Semester 2, and Semester 3: 2014-2017",
    },
    bars: "horizontal", // Required for Material Bar Charts.
  };

  var chart = new google.charts.Bar(
    document.getElementById("barchart_material")
  );

  chart.draw(data, google.charts.Bar.convertOptions(options));
}
