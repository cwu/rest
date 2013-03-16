var bicubic = (function(){
  return function(x, y, values){
    var i0, i1, i2, i3;

    i0 = TERP(x, values[0][0], values[0][1], values[0][2], values[0][3]);
    i1 = TERP(x, values[1][0], values[1][1], values[1][2], values[1][3]);
    i2 = TERP(x, values[2][0], values[2][1], values[2][2], values[2][3]);
    i3 = TERP(x, values[3][0], values[3][1], values[3][2], values[3][3]);
    return TERP(y, i0, i1, i2, i3);
  };
  function TERP(t, a, b, c, d){
    return 0.5 * (c - a + (2.0*a - 5.0*b + 4.0*c - d + (3.0*(b - c) + d - a)*t)*t)*t + b;
  }
})();

var colormap = function(value) {
  var fourValue = value * 4;
  var red   = parseInt(Math.min(fourValue - 1.5, -fourValue + 4.5) * 255, 10);
  var green = parseInt(Math.min(fourValue - 0.5, -fourValue + 3.5) * 255, 10);
  var blue  = parseInt(Math.min(fourValue + 0.5, -fourValue + 2.5) * 255, 10);
  return [red, green, blue];
}

function heatmapify(img) {
  var canvas = document.getElementById('test');
  var buffer = document.createElement('canvas');
  buffer.width = canvas.width;
  buffer.height = canvas.height;
  var c = canvas.getContext('2d');

  var small_width = img[0].length;
  var small_height = img.length;
  var max_value = -1, min_value = 1000000;
  for (var y = 0; y < img.length; y++) {
    for (var x = 0; x < img[y].length; x++) {
      if (img[y][x] > max_value) { max_value = img[y][x]; }
      if (img[y][x] < min_value) { min_value = img[y][x]; }
    }
  }

  // buffer the end elements
  for (var y = 0; y < img.length; y++) {
    img[y] = [img[y][0], img[y][0]].concat(img[y]).concat([
        img[y][img[y].length - 1],
        img[y][img[y].length - 1]
    ]);
  }
  img = [img[0], img[0]].concat(img).concat([img[img.length - 1], img[img.length-1]]);

  var width = $(canvas).width();
  var height = $(canvas).height();
  var x_unit = width / (small_width+1);
  var y_unit = height / (small_height+1);

  var image = c.getImageData(0,0,width,height);
  var min_norm = 10000;
  var max_norm = -1;
  for (var y = 0; y < height; y++) {
    for (var x = 0; x < width; x++) {
      var i = parseInt(y / y_unit, 10)+1;
      var j = parseInt(x / x_unit, 10)+1;
      var values = [
        [ img[i-1][j-1] , img[i-1][j] , img[i-1][j+1] , img[i-1][j+2] ] ,
        [ img[i][j-1]   , img[i][j]   , img[i][j+1]   , img[i][j+2] ]   ,
        [ img[i+1][j-1] , img[i+1][j] , img[i+1][j+1] , img[i+1][j+2] ] ,
        [ img[i+2][j-1] , img[i+2][j] , img[i+2][j+1] , img[i+2][j+2] ]
      ];
      var dx = (x / x_unit) % 1;
      var dy = (y / y_unit) % 1;
      var interpolated = bicubic(dx, dy, values);
      var normalized = interpolated / 1024; //(interpolated - min_value) / (max_value - min_value);
      min_norm = Math.min(normalized, min_norm);
      max_norm = Math.max(normalized, max_norm);
      normalized = Math.min(Math.max(normalized, 0), 1);
      var color = colormap(normalized);
      var index = (y * width + x) * 4;
      image.data[index + 0] = color[0];
      image.data[index + 1] = color[1];
      image.data[index + 2] = color[2];
      image.data[index + 3] = 255;
    }
  }
  console.log(min_norm + " < pixel < " + max_norm);

  c.putImageData(image, 0, 0);
}
