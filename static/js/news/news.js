$(document).ready(function(e) {   
    
    // $(".card-img-top").css({
    //     "transition": "transform .2s",
    //     "overflow": "hidden",
    // });
//     $(".card-img-top").hover(function () {
//         $(this).toggle('animate');
        
//     }, function () {
//         $(this).toggle('usual');
//     }
// );
$(".title").css({
    "text-decoration":"none",
    "color": "#858796"
});
$(".title").hover(function () {
    $(this).css({
        "color": "#4e73df"
    });
        
    }, function () {
        $(this).css({
            "color": "#858796"
        });
    }
);
$(".card").hover(function () {
        $(this).removeClass("shadow-small");
        $(this).addClass("shadow");
        
    }, function () {
        $(this).removeClass("shadow");
        $(this).addClass("shadow-small");
    }
);
});