var toggle = function(element, url) {
    $.ajax({
        url: url,
        type: 'POST',
        data: {'registration': element.data('reg')},
        success: function(response) {
            element.parent().first('.check_in_status').html(response);
        }
    });
}

$(document).on("click", ".toggle_checked_in", function(e) {
    toggle($(this), URL.toggle_checked_in);
    e.preventDefault();
});

$(document).on("click", ".toggle_checked_out", function(e) {
    toggle($(this), URL.toggle_checked_out);
    e.preventDefault();
});
