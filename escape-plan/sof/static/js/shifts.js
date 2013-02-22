$(function() {
    $(".add_worker").click(
    function(e) {
        var element = $(this);
        $.ajax({
            url: URL.add_worker,
            type: 'POST',
            data: {'shift': element.data('shift'),
                   'worker': $('#shift_accordion').data('worker')},
            success: function(response) {
                if (response.book_status == 'ok') {
                    element.parent().addClass('added');
                    element.html(response.html);
                }
            }
        });
        e.preventDefault();
    });

    $("#id_term").focus();
});
