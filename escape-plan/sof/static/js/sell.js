WORKER_ID = 0;
VISITOR_ID = 0;

var submit_turbo_form = function(e) {
    $.ajax({
        url: URL.turbo_submit,
        type: 'POST',
        data: $(this).serialize(),
        success: function(response) {
            if (response.is_valid === false) {
                 $('#turbo').html(response.html);
            } else {
                WORKER_ID = response.worker_id;
                VISITOR_ID = response.visitor_id;
                $('#modal_container').html(response.html);
                $('#turbo_modal').modal();
            }
        }
    });
    e.preventDefault();
};

var confirm_turbo_form = function(e) {
    var form_url = URL.turbo_confirm;
    if (WORKER_ID) {
        form_url += '?worker_id=' + WORKER_ID;
    } else if(VISITOR_ID) {
        form_url += '?visitor_id=' + VISITOR_ID;
    }

    $.ajax({
        url: form_url,
        type: 'POST',
        data: $(this).serialize(),
        success: function(response) {
            if (response.is_valid === false) {
                 alert('Något verkar inte vara korrekt ifyllt.');
            } else {
                window.location.replace(response.url);
            }
        },
        error: function(response) {
            alert('Servern gjorde något dumt.');
        }
    });
    e.preventDefault();
};


$(function() {
    $('#tabs a[href="#turbo"]').tab('show');

    $(".tab-content").on('submit', '.turbo_form', submit_turbo_form);
    $(".tab-content").on('submit', '.turbo_confirm', confirm_turbo_form);
});


// Change hash for page-reload
$('.nav-tabs a').on('shown', function (e) {
    window.location.hash = e.target.hash;
    window.scrollTo(0, 0);
    $(e.target.hash).find('input[type=text]')[0].focus();
});

var url = document.location.toString();
if (url.match('#')) {
    $('.nav-tabs a[href=#'+url.split('#')[1]+']').tab('show');
    window.scrollTo(0, 0);
    $(window.location.hash).find('input[type=text]')[0].focus();
}
