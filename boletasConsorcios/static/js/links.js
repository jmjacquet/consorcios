$(document).ready(function(){           
$("body").on("click", "a[data-href]", function() {
    var href = $(this).data("href");
    if (href) {
        location.href = href;
    }
});

});

