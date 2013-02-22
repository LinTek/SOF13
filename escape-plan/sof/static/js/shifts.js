$(function() {
    $(".add_worker").dblclick(
    function() {
        var e = $(this);
        $.ajax({
            url: URL.add_worker,
            type: 'POST',
            data: {'shift': e.data('shift')},
            success: function(response) {
                if (response === 'ok') {
                    e.addClass('added');
                }
            }
        });
        return false;
    });

    $("#id_term").focus();
});
