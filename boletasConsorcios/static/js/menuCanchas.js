
$(function() {
  $('.tabsCanchas nav a').on('click', function() {
    show_content($(this).index());
  });
  
  show_content(1);

  function show_content(index) {
    // Make the content visible
    $('.tabsCanchas .content.visible').removeClass('visible');
    $('.tabsCanchas .content:nth-of-type(' + (index + 1) + ')').addClass('visible');

    // Set the tab to selected
    $('.tabsCanchas nav a.selected').removeClass('selected');
    $('.tabsCanchas nav a:nth-of-type(' + (index + 1) + ')').addClass('selected');
  }
});
