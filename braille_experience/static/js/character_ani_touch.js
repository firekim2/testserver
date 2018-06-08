var num_of_character = $(".character").length;
var index_now;

$(document).ready(function(){
  $("body").on("touchmove", function(e){
    triggerReactor(e);
  });
  $("body").on("click", function(e){
    triggerReactor(e);
  });
});
function triggerReactor(e){
  if (e.originalEvent.type == "touchmove"){
    e = e.originalEvent.changedTouches[0];
  }
  else {
    e = e.originalEvent;
  }
  var characters = $(".character");
  for (var i = 0; i < num_of_character; i++) {
    var left = characters[i].offsetLeft;
    var right = left + characters[i].offsetWidth;
    var top = characters[i].offsetTop;
    var bottom = top + characters[i].offsetHeight;
    if (e.clientX > left && e.clientX < right && e.clientY > top && e.clientY < bottom && index_now !== i) {
      index_now = i;
      $("#big_font").text(characters[i].id);
      characters.css("color","#000000");
      $(".character:eq("+i+")").css("color","#ff0000");
      window.navigator.vibrate([10]);
    }
  }
}
