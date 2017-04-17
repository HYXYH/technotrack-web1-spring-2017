/**
 * Created by Oskar on 16.04.17.
 */



// old
// function toggleChat(chatid) {
//     resizeChatToPost(chatid);
//     $('#comments-block-' + chatid.toString(10)).toggle();
// }
//
//
// min of screen height or post height
function resizeBlockToPost(id) {
    var h = Math.min($(window).height() - 60, $('#post-block-' + id).height());
    $('#comments-block-' + id).height(h);
    // alert("id: "  + id + "\nwh: " + ($(window).height() - 60) + "\npb: " + $('#post-block-' + id).height() + "\n" + h)
}
//
// function searchFind() {
//     $('#search-find').toggle();
//     $('#sort-find').toggle();
// }


function rate(id, url) {
    $.post(
        url,
        "",
        function (data) {
            if (data.length < 10) {
                $("#rate-" + id).html(data);
            }
        });
    return false;
}


$(document).ready(function () {

    $(".comment-block").each(function (index, block) {
        var pid = block.id;
        var numberPattern = /\d+/g;
        resizeBlockToPost(pid.match(numberPattern)[0]);
    });

    $(document).on('submit', '.ajax-newcomment', function () {
        var id = $(this).attr('data-id');
        $.post(
            $(this).attr('data-url'),
            $(this).serialize(),
            function (data) {
                $('#chat-' + id).html(data);//[0].scrollIntoView(false);
                // $('#chat-' + id).scrollTop = $('#chat-' + id).scrollHeight;
            }
        );
        return false;
    });

    function updateRating() {
        var ids = [];

        $(".rate-slot").each(function () {
            ids.push($(this).data('id'));
        });

        $.getJSON('/rates/', {ids: ids.join(',')}, function (data) {
                for (var i in data) {
                    $('.rate-slot[data-id=' + i + ']').html(data[i]);
                }
            }
        )
    }

    function updateComments() {
        $(".chat").each(function () {
            $(this).load($(this).data("url"))
        });
    }

    window.setInterval(updateRating, 5000);

    window.setInterval(updateComments, 5000);


    // move comments-block when scroll
    $(window).scroll(function () {
        $('.post-block').each(function (index, block) {
            // if (block.position.y )
            var ph = $('#' + block.id).height();
            var postUp = $("#" + block.id).offset().top;
            var pos = $(window).scrollTop() + 55;
            var postDown = ph - ($(window).height() - 55) + postUp + 10;

            var numberPattern = /\d+/g;
            $("#test-" + block.id.match(numberPattern)[0]).html("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>" + postUp + " <br><br>" + pos + "<br><br>" + " " + postDown);

            if (postDown > 0) {
                if ((pos > postUp) && (pos < postDown )) {
                  $("#comment-block-" + block.id.match(numberPattern)[0]).css("position","fixed");
                  // alert("fixed");
                }
                else {
                    $("#comment-block-" + block.id.match(numberPattern)[0]).css("position","relative");
                    // alert("rel");
                }
            }
        });

// // distance from top of footer to top of document
//         footertotop = ($('#footer').position().top);
// // distance user has scrolled from top, adjusted to take in height of sidebar (570 pixels inc. padding)
//         scrolltop = $(document).scrollTop() + 570;
// // difference between the two
//         difference = scrolltop - footertotop;
//
// // if user has scrolled further than footer,
// // pull sidebar up using a negative margin
//
//         if (scrolltop > footertotop) {
//
//             $('#cart').css('margin-top', 0 - difference);
//         }
//
//         else {
//             $('#cart').css('margin-top', 0);
//         }
    });

});
