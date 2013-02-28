$(function() {
  var navBottom = $('#nav_wrap').offset().top + $('#nav_wrap').height()
  if ($(window).scrollTop() > navBottom) {
    $('#nav_wrap').addClass('sticky');
  }
  $(window).scroll(function() {
    if ($(window).scrollTop() > navBottom) {
      $('#nav_wrap').addClass('sticky');
    } else {
      $('#nav_wrap').removeClass('sticky');
    }
  });
  $('a[href*=#]:not([href=#])').on('click', function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'')
        || location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html,body').animate({
          scrollTop: target.offset().top
        }, 1000);
        return false;
      }
    }
  });
});
