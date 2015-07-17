$(function() {

$('.drawer-header').on('click', function(e) {
    $(e.delegateTarget).parents('.drawer').toggleClass('show');
});

})
