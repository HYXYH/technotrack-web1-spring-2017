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

        var url = $(".rate-slot")[0].data('url');

        $.getJSON(url, {ids: ids.join(',')}, function (data) {
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
            var numberPattern = /\d+/g;

            var postBlock = $("#post-block-" + block.id.match(numberPattern)[0]);
            var commentsBlock = $("#comments-block-" + block.id.match(numberPattern)[0]);

            var ph = postBlock.height();
            var postUp = postBlock.offset().top;
            var pos = $(window).scrollTop() + 55;
            var postDown = ph - ($(window).height() - 55) + postUp + 10;


            var status;
            status = 'no scroll';
            if (postDown > 0) {
                if ((pos > postUp) && (pos < postDown )) {
                    var x = postBlock.offset().left + postBlock.width() + 17;
                    commentsBlock.css("position", "fixed").width('auto').offset({top: pos, left: x});
                    status = 'catch! '
                }
                else if (pos <= postUp) {
                    commentsBlock.css("position", "relative").css('top', 'auto').css('left', 'auto');
                    status = 'upper';
                } else if (pos >= postDown) {
                    var d = ph - commentsBlock.height();
                    commentsBlock.css("position", "relative").css('top', d).css('left', 'auto');
                    status = 'lower';
                }
            }
            // $("#test-" + block.id.match(numberPattern)[0]).html("<br><br>" + postUp
            // + " <br><br>" + status + " " + pos + "<br><br>" + " " + postDown);
        });
    });

});
