var num_of_character = $(".character").length;

$(document).ready(function(){
  reactor();
});

function reactor(){
    $(".character").each(function(index, element){
      $(this).mouseenter(function(){
        $("#big_font").text(this.id);
        $(".glass").css('left',this.offsetLeft + 15 + 'px');
        $(".glass").css('top',this.offsetTop + 15 + 'px');
      });
    });
}
