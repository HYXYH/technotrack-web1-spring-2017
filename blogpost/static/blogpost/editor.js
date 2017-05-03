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
                // data contains the HTML for the replacement post/blog
                $('#modal-editor').modal('hide');
                var result = $(data).find('#' + id);
                if ($('#' + id).length == 0) {
                    location.reload();
                    return;
                }
                $('#' + id).replaceWith(result);
                location.hash = '#' + id;
                window.scrollTo(window.scrollX, window.scrollY - 55);
            }
        );
        return false;
    }),

    // refresh selectpicker
    $(document).on('click', '.load-editor', function () {
        var url = $(this).attr('data-url');
        $("#editor-content").load(url, function () {
            $('.selectpicker').selectpicker();
        });
        return false;
    })
);


