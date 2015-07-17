$(function() {

$('.drawer-toggle').on('click', function(e) {
    $(e.delegateTarget).parents('.drawer').toggleClass('show');
});

})
