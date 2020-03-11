$(document).ready(function(){
  
    /* 1. Visualizing things on Hover - See next part for action on click */
    $('#stars_taste li, #stars_cost li, #stars_prep li').on('mouseover', function(){
      var onStar = parseInt($(this).data('value'), 10); // The star currently mouse on
     
      // Now highlight all the stars that's not after the current hovered star
      $(this).parent().children('li.star').each(function(e){
        if (e < onStar) {
          $(this).addClass('hover');
        }
        else {
          $(this).removeClass('hover');
        }
      });
      
    }).on('mouseout', function(){
      $(this).parent().children('li.star').each(function(e){
        $(this).removeClass('hover');
      });
    });
    
    
    /* 2. Action to perform on click */
    $('#stars_taste li, #stars_cost li, #stars_prep li').on('click', function(){
      var onStar = parseInt($(this).data('value'), 10); // The star currently selected
      var stars = $(this).parent().children('li.star');
      
      for (i = 0; i < stars.length; i++) {
        $(stars[i]).removeClass('selected');
      }
      
      for (i = 0; i < onStar; i++) {
        $(stars[i]).addClass('selected');
      }
      
      // JUST RESPONSE (Not needed)
      var ratingCost = parseInt($('#stars_cost li.selected').last().data('value'), 10);
      var ratingTaste = parseInt($('#stars_taste li.selected').last().data('value'), 10);
      var ratingPrep = parseInt($('#stars_prep li.selected').last().data('value'), 10);

      $('#taste_star').val(ratingTaste);
      $('#cost_star').val(ratingCost);
      $('#prep_hardness_star').val(ratingPrep);
    });
    
  });