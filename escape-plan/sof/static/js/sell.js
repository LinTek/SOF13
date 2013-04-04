var submit_turbo_form = function(e) {
    $.ajax({
        url: URL.turbo_submit,
        type: 'POST',
        data: $(this).serialize(),
        success: function(response) {
            if (response.is_valid === false) {
                 $('#turbo').html(response.html);
            } else {
                $('#turbo').html(response.html);
                console.log("Valid!");
            }
        }
    });
    e.preventDefault();
};

$(function() {
    $('#tabs a[href="#turbo"]').tab('show');

    $(".tab-content").on('submit', '.turbo_form', submit_turbo_form);
});


var url = document.location.toString();
if (url.match('#')) {
    $('.nav-tabs a[href=#'+url.split('#')[1]+']').tab('show');
}

// Change hash for page-reload
$('.nav-tabs a').on('shown', function (e) {
    window.location.hash = e.target.hash;
    window.scrollTo(0, 0);
    $(e.target.hash).find('input[type=text]')[0].focus();
});

