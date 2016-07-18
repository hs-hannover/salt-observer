$(function() {
    $('.title-wrapper').click(function() {
        window.location = $(this).data('root');
    });

    // some little helpers
    $.tablesorter.themes.bootstrap = {
        header: 'bootstrap-header',
        iconSortNone: 'fa fa-sort',
        iconSortAsc: 'fa fa-sort-asc',
        iconSortDesc: 'fa fa-sort-desc',
    };
    $('table.sortable').tablesorter({
        theme: 'bootstrap',
        headerTemplate: '{content} {icon}',
        sortList: [[0,0]],
        widgets: ['uitheme'],
    });
});
