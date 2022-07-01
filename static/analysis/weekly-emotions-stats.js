var xValues = ["Happy", "Angry", "Sad", "Surprise", "Fear"];
var yValues = [{{ emotion_data_weekly.Happy }}, {{ emotion_data_weekly.Angry }}, {{ emotion_data_weekly.Sad }}, {{ emotion_data_weekly.Surprise }},
            {{ emotion_data_weekly.Fear }}];
    var barColors = [
      "#1572A1",
      "#9AD0EC",
      "#EFDAD7",
      "#E3BEC6",
      "#FFDFD3",
    ];

new Chart("myChart2", {
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
      text: "Weekly Mood Analysis"
    }
  }
});