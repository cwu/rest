$ ->
  accelCharts = [null, null]
  createAccelChart = (id) ->
    accelCharts[id] =
      chart : new SmoothieChart(
        maxValue : 2048
        minValue : -2058
      )
      x     : new TimeSeries()
      y     : new TimeSeries()
      z     : new TimeSeries()
    accelCharts[id].chart.streamTo(document.getElementById("accel-#{id}"), 1000)
    accelCharts[id].chart.addTimeSeries(accelCharts[id].x,
      { strokeStyle:'rgb(255, 0, 0)', lineWidth:3 })
    accelCharts[id].chart.addTimeSeries(accelCharts[id].y,
      { strokeStyle:'rgb(0, 255, 0)', lineWidth:3 })
    accelCharts[id].chart.addTimeSeries(accelCharts[id].z,
      { strokeStyle:'rgb(255, 0, 255)', lineWidth:3 })
    setInterval(()->
      $.ajax("/accel/#{id}").done (data) ->
        now = new Date().getTime()
        accelCharts[id].x.append(now, data.x)
        accelCharts[id].y.append(now, data.z)
        accelCharts[id].z.append(now, data.y)
    , 100)

  #_.each [0, 1], createAccelChart

  heatmap = h337.create
    element  : 'heatmap'
    radius   : 50
    opacity  : 90
    visible : true

  setInterval(()->
    width = $('#heatmap').width()
    height = $('#heatmap').height()
    $.ajax('/fsr').done (response) ->
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
