$ ->
  accelChart = [null, null]
  accelChart =
    chart : new SmoothieChart(
      maxValue : Math.floor(2048 * Math.sqrt(3) - 950)
      minValue : Math.floor(-2048 * Math.sqrt(3) + 950)
    )
    accel     : [new TimeSeries(), new TimeSeries()]
  accelChart.chart.streamTo(document.getElementById("accel"), 500)
  accelChart.chart.addTimeSeries(accelChart.accel[0], { strokeStyle:'rgb(255, 0, 0)', lineWidth:3 })
  accelChart.chart.addTimeSeries(accelChart.accel[1], { strokeStyle:'rgb(255, 0, 255)', lineWidth:3 })
  setInterval(()->
    _.each [0, 1], (id) ->
      $.ajax("/fake/accel/#{id}").done (data) ->
        now = new Date().getTime()
        value = Math.sqrt(data.x * data.x + data.y * data.y + data.z * data.z) - 950
        accelChart.accel[id].append(now, value)
  , 500)


  heatmap = h337.create
    element  : 'heatmap'
    radius   : 50
    opacity  : 90
    visible : true

  setInterval(()->
    width = $('#heatmap').width()
    height = $('#heatmap').height()
    $.ajax('/fake/fsr').done (response) ->
      data =
        max : 1023
        data : []
      _.each response.data, (fsr) ->
        # switch x and y
        data.data.push
          x     : fsr.y * width
          y     : fsr.x * height
          count : fsr.value
      heatmap.store.setDataSet data
  , 100)
  #$.ajax('/fsr').done (response) ->
  #  heatmapify(response.data)
