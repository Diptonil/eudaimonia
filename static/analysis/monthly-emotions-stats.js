var xValues = ["Happy", "Angry", "Sad", "Surprise", "Fear"];
var yValues = [{{ emotion_data_monthly.Happy }}, {{ emotion_data_monthly.Angry }}, {{ emotion_data_monthly.Sad }}, {{ emotion_data_monthly.Surprise }},
            {{ emotion_data_monthly.Fear }}];
    var barColors = [
      "#1572A1",
      "#9AD0EC",
      "#EFDAD7",
      "#E3BEC6",
      "#FFDFD3",
    ];

new Chart("myChart3", {
  type: "pie",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: barColors,
      data: yValues
    }]
  },
  options: {
    title: {
      display: true,
      text: "Monthly Mood Analysis"
    }
  }
});