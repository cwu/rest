function heatmapify(img) {
  var canvas = document.getElementById('test');
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
    img[y] = [img[y][0]].concat(img[y]).concat(img[y][img[y].length - 1]);
  }
  img = [img[0]].concat(img).concat([img[img.length - 1]]);

  var width = $(canvas).width();
  var height = $(canvas).height();
  var x_unit = width / small_width;
  var y_unit = height / small_height;

  var image = c.createImageData($(canvas).width(), $(canvas).height());
  var min_norm = 10000;
  var max_norm = -1;
  for (var y = 0; y < height; y++) {
    for (var x = 0; x < width; x++) {
      var i = Math.floor(y / y_unit) + 1;
      var j = Math.floor(x / x_unit) + 1;
      var topleft = img[i][j],
          topright = img[i][j+1],
          bottomleft = img[i+1][j],
          bottomright = img[i+1][j+1];
      var up = (topleft + topright) / 2;
      var down = (bottomleft + bottomright) / 2;
      var left = (topleft + bottomleft) / 2;
      var right = (topright + bottomright) / 2;
      var dx = (x % x_unit) / x_unit;
      var dy = (y % y_unit) / y_unit;
      var interpolated = (left + (right - left) * dx);
      var normalized = (interpolated - min_value) / (max_value - min_value + 1);
      min_norm = Math.min(normalized, min_norm);
      max_norm = Math.max(normalized, max_norm);
      var rgb = normalized * 256 * 256 *256;
      var r = Math.floor(rgb / (256 * 256));
      var g = Math.floor(rgb / 256 - r * 256);
      var b = Math.floor(rgb - r * 256 * 256 - g * 256);
      var index = (y * width + x) * 4;
      image.data[index + 0] = r;
      image.data[index + 1] = g;
      image.data[index + 2] = b;
      image.data[index + 3] = 255;
    }
  }
  console.log(min_norm);
  console.log(max_norm);

  c.putImageData(image, 0, 0);
}
