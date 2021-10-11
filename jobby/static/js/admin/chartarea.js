$(document).ready(function () {
  // Set new default font family and font color to mimic Bootstrap's default styling
  Chart.defaults.global.defaultFontFamily = "Nunito";
  Chart.defaults.global.defaultFontColor = '#888';
  Chart.defaults.global.defaultFontSize = '14';

  var ctx = document.getElementById('myAreaChart').getContext('2d');

  var myLineChart = new Chart(ctx, {
    type: 'line',

    // The data for our dataset
    data: {
      labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
      // Information about the dataset
        datasets: [{
        label: "Views",
        backgroundColor: 'rgba(42,65,232,0.08)',
        borderColor: '#2a41e8',
        borderWidth: "3",
        data: [0, 0, 0, 0, 0, 0, 0],
        pointRadius: 5,
        pointHoverRadius:5,
        pointHitRadius: 10,
        pointBackgroundColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointBorderWidth: "2",
      }]
    },

    // Configuration options
    options: {

        layout: {
          padding: 10,
        },

      legend: { display: false },
      title:  { display: false },

      scales: {
        yAxes: [{
          scaleLabel: {
            display: false
          },
          gridLines: {
             borderDash: [6, 10],
             color: "#d8d8d8",
             lineWidth: 1,
                },
        }],
        xAxes: [{
          scaleLabel: { display: false },
          gridLines:  { display: false },
        }],
      },

        tooltips: {
          backgroundColor: '#333',
          titleFontSize: 13,
          titleFontColor: '#fff',
          bodyFontColor: '#fff',
          bodyFontSize: 13,
          displayColors: false,
          xPadding: 10,
          yPadding: 10,
          intersect: false
        }
    },
});

  $('#dataView').on('change', function(e){
    const xhr = new XMLHttpRequest();
    var view_type = $(this).attr('data');
    if (view_type == "userView") {
      var username = $(this).val();
      var url = '/user-view-data/' + username;
    }
    else if (view_type == "projectView") {
      var project_id = $(this).val();
      var url = '/project-view-data/' + project_id;
    }

    xhr.open('GET', url);
    xhr.onload = () => {
      if (xhr.status == 200){
        const result = JSON.parse(xhr.responseText);
        if (result.success) {
          myLineChart.data.datasets[0].data = result.view_list;
          myLineChart.update();
        }
      }
    }
    xhr.send();
  })
});
