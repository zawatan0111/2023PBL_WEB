$(document).ready(function () {
    hsize = $(window).height();
    $("#info_table").css("height", hsize-30 + "px");
  });
  $(window).resize(function () {
    hsize = $(window).height();
    $("#info_table").css("height", hsize-30 + "px");
});

$(document).ready(function () {
    hsize = $(window).height();
    $(".lsb_ul").css("height", hsize-30 + "px");
  });
  $(window).resize(function () {
    hsize = $(window).height();
    $(".lsb_ul").css("height", hsize-30 + "px");
});