var xValues = ["Happy", "Angry", "Sad", "Surprise", "Fear"];
var yValues = [{{ emotion_data.Happy }}, {{ emotion_data.Angry }}, {{ emotion_data.Sad }}, {{ emotion_data.Surprise }},
            {{ emotion_data.Fear }}];
    var barColors = [
      "#1572A1",
      "#9AD0EC",
      "#EFDAD7",
      "#E3BEC6",
      "#FFDFD3",
    ];

new Chart("myChart1", {
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
      text: "Overall Mood Analysis"
    }
  }
});