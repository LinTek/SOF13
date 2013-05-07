var toggle = function(element, url) {
    $.ajax({
        url: url,
        type: 'POST',
        data: {'pk': element.data('pk')},
        success: function(response) {
            element.parent().first('.check_in_status').html(response);
        }
    });
};

$(document).on("click", ".toggle_checked_in", function(e) {
    toggle($(this), URL.toggle_checked_in);
    e.preventDefault();
});

$(document).on("click", ".toggle_checked_out", function(e) {
    toggle($(this), URL.toggle_checked_out);
    e.preventDefault();
});

$(document).on("click", ".toggle_info_meeting", function(e) {
    toggle($(this), URL.toggle_info_meeting);
    e.preventDefault();
});

$(document).on("click", ".toggle_merchandise", function(e) {
    toggle($(this), URL.toggle_merchandise);
    e.preventDefault();
});

function update_watchlist() {
    $.ajax({
        url: window.location.href,
        data: {'watchlist': ''},
        method: 'GET',
        success: function(response) {
            $('watchlist').html(response);
        }
    });
}
