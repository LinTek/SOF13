$(function() {
    $(".add_worker").click(
    function() {
        var e = $(this);
        $.ajax({
            url: URL.add_worker,
            type: 'POST',
            data: {'shift': e.data('shift')},
            success: function() {
                e.addClass('added');
            }
        });
        return false;
    });
});
