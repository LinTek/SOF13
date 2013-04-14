$(function() {
    $(".toggle_handed_out").click(
    function(e) {
        var element = $(this);
        $.ajax({
            url: URL.toggle_handed_out,
            type: 'POST',
            data: {'member': element.data('member')},
            success: function(response) {
                if (response.ticket_handed_out === true) {
                    element.addClass('btn-danger');
                    element.html('Utlämnad');

                } else {
                    element.removeClass('btn-danger');
                    element.html('Lämna ut');
                }
            }
        });
        e.preventDefault();
    });
    $("#id_q").focus();
});
