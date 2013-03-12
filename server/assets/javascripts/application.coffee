$ ->
  ACCEL_UPDATE = 1000
  FSR_UPDATE = 1000
  accel_url = $('#accel-url').attr('value')
  fsr_url = $('#fsr-url').attr('value')
  accelChart = [null, null]
  accelChart =
    chart : new SmoothieChart(
      maxValue : Math.floor(2048 * Math.sqrt(3) - 950)
      minValue : Math.floor(-2048 * Math.sqrt(3) + 950)
    )
    accel     : [new TimeSeries(), new TimeSeries()]
  accelChart.chart.streamTo(document.getElementById("accel"), ACCEL_UPDATE)
  accelChart.chart.addTimeSeries(accelChart.accel[0], { strokeStyle:'rgb(255, 0, 0)', lineWidth:3 })
  accelChart.chart.addTimeSeries(accelChart.accel[1], { strokeStyle:'rgb(255, 0, 255)', lineWidth:3 })
  setInterval(()->
    _.each [0, 1], (id) ->
      $.ajax("#{accel_url}/#{id}?t=#{ACCEL_UPDATE}").done (data) ->
        now = new Date().getTime()
        accelChart.accel[id].append(now, data.data)
  , ACCEL_UPDATE)


  heatmap = h337.create
    element  : 'heatmap'
    radius   : 50
    opacity  : 90
    visible : true

  setInterval(()->
    width = $('#heatmap').width()
    height = $('#heatmap').height()
    $.ajax("#{fsr_url}?t=#{FSR_UPDATE}").done (response) ->
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
