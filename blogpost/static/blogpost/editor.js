/**
 * Created by Oskar on 16.04.17.
 */

$(document).ready(
    $(document).on('submit', '.ajaxform', function () {
        var id = $(this).attr('data-id');
        $.post(
            $(this).attr('data-url'),
            $(this).serialize(),
            function (data) {
                if (data.redirect) {
                    // data.redirect contains the string URL to redirect to
                    window.location.href = data.redirect;
                }
                else {
                    // data contains the HTML for the replacement form
                    $('#modal-editor').modal('hide');
                    var result = $(data).find('#blog-' + id);

                    if ($(result).length == 0) {
                        result = $(data).find('#post-' + id);
                        $('#post-' + id).replaceWith(result);
                        location.hash = '#post-' + id
                    } else {

                        $('#blog-' + id).replaceWith(result);
                        location.hash = '#blog-' + id
                    }
                     window.scrollTo(window.scrollX, window.scrollY - 55);
                }
            }
        );
        return false;
    }),

    $(document).on('click', '.load-editor', function () {
        var url = $(this).attr('data-url');
        var id = $(this).attr('data-id');
        $("#editor-content").load(url, function () {
            $(".ajaxform").attr('data-url', url).attr('data-id', id);
            $('.selectpicker').selectpicker();
        });
        return false;
    })
);


