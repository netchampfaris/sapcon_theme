import 'bootstrap/dist/js/bootstrap.bundle';
import './modal'

// multilevel dropdown
$('.dropdown-menu a.dropdown-toggle').on('click', function (e) {
    e.preventDefault();
    e.stopImmediatePropagation();
    if (!$(this).next().hasClass('show')) {
        $(this).parents('.dropdown-menu').first().find('.show').removeClass("show");
    }
    var $subMenu = $(this).next(".dropdown-menu");
    $subMenu.toggleClass('show');


    $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function (e) {
        $('.dropdown-submenu .show').removeClass("show");
    });


    return false;
});