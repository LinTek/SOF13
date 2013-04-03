$(function() {
    $('#tabs a[href="#turbo"]').tab('show');
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
})
