$ ->
  DATA_POINTS = 10
  accelCharts = [null, null]
  _.each [1, 2], (id) ->
    $.ajax(url: "/accel/#{id}").done (data) ->
      accelCharts[id] = new Highcharts.Chart
        chart:
          renderTo: "accel-#{id}"
          type: 'line'
          events :
            load : () ->
              setInterval(() ->
                $.ajax(url : "/accel/#{id}").done (data) ->
                  series = accelCharts[id].series
                  shift = series[0].data.length > DATA_POINTS
                  series[0].addPoint data.series[0].data[0], true, shift
                  series[1].addPoint data.series[1].data[0], true, shift
                  series[2].addPoint data.series[2].data[0], true, shift
              , 500)
        title:
          text: "Accelerometer #{id}"
        xAxis:
          labels: false
        yAxis:
          title:
            text: 'Accelometer Values'
        series: data.series
