

// image gallery

$("#slideshow > img:gt(0)").hide();

setInterval(function () {
    $('#slideshow > img:first')
        .fadeOut(3000)
        .next()
        .fadeIn(3000)
        .end()
        .appendTo('#slideshow');
}, 5000);


whr(document).ready(function () {
    whr_embed(164082, { detail: 'titles', base: 'jobs', zoom: 'country', grouping: 'none', url: 'url' });
});


$(document).ready(function () {
    //console.log( "ready!" );

    var timerId = setInterval(function () {

        $('h3.whr-title').each(function () {

            var href = $(this).children().first().attr('href');

            var new_content = $(this).parent().html() + "<div class='apply-now-btn'><a href='" + href + "' target='_blank'>Apply Now</a></div>";

            $(this).parent().html(new_content);

            clearInterval(timerId);
        });

    }, 1000);
});
