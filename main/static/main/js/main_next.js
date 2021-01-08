$("#success-danger").hide();

function setupData() {
    var table = $('#datatable').DataTable({
        "ajax": {
            "url": "/ajax/next_matches",
            "data": "",
            "dataType": "json",
            "dataSrc": "data",
            "contentType": "application/json"
        },
        "paging": true,
        "saveState": true,
        "ordering": false,
        "deferRender": true,
        "scrollY": '60vh',
        "scrollX": true,
        "scrollCollapse": true,
        scroller: {
            loadingIndicator: true,
            displayBuffer: 2000
        },
        "searching": false,
        "fixedHeader": true,
        "dom": "<'row'<'col-sm-2'l><'col-sm-2'><'col-sm-4'><'col-sm-4'p>>" +
            "<'row'<'col-sm-2'><'col-sm-8 text-center'i><'col-sm-2'>>t",
        'rowId': 'match_name',
        'select': {
            'style': 'multi'
        },
        "columns": [
            { "data": "time", "width": "80px" },
            { "data": "league_name" },
            { "data": "match_name" },
            { "data": "coef_p1", "width": "60px" },
            { "data": "coef_x", "width": "60px" },
            { "data": "coef_p2", "width": "60px" }
        ],
        "language": {
            "decimal": "",
            "emptyTable": "Нет данных",
            "info": "Сегодня _TOTAL_ матчей.",
            "infoEmpty": "",
            "infoFiltered": "(Фильтр на основе _MAX_ матчей)",
            "infoPostFix": "",
            "thousands": ",",
            "lengthMenu": "Показывать по _MENU_ матчей",
            "loadingRecords": "Загрузка данных...",
            "processing": "Обработка...",
            "search": "Поиск:",
            "zeroRecords": "Таких матчей нет",
            "paginate": {
                "first": "Первая",
                "last": "Последняя",
                "next": "Вперед",
                "previous": "Назад"
            },
            "aria": {
                "sortAscending": ": activate to sort column ascending",
                "sortDescending": ": activate to sort column descending"
            },
            'select': {
                'rows': {
                    _: "Выбрано матчей - %d",
                    0: "Выберите матчи для анализа",
                }
            }
        },
        "lengthMenu": [[50, -1], [50, 'Все']]
    })

    table
        .on('select', function (e, dt, type, indexes) {
            var selected = table.rows({ selected: true }).nodes().to$()
            for (i = 0; i < selected.length; i++) {
                if (selected.eq(i).children().eq(4).text() != '') {
                    selected.eq(i).addClass('table-success text-dark')
                } else {
                    table.row(selected.eq(i)).deselect()
                    $("#success-danger").fadeTo(2000, 500).slideUp(500, function () {
                        $("#success-danger").slideUp(500);
                    });
                }
            }
        })
        .on('deselect', function (e, dt, type, indexes) {
            table.rows({ selected: false }).nodes().to$().removeClass('table-success text-dark')
        });

    $('#datatable_info').addClass('text-white bg-dark border border-dark rounded py-2');
    $('.select_item').addClass('text-white');
}
$(window).on("load", setupData);

$(document).ready(function () {
    $(to_analyze).click(function () {
        reloadMathcesInLS();
    });
    $(reset_select).click(function () {
        $('#datatable').DataTable().rows({ selected: true }).deselect()
        localStorage.clear()
    });
    $(to_next).click(function () {
        toNextMatches();
    });
});

function toNextMatches() {
    var time = new Date().toLocaleTimeString().slice(0, -3)
    var table = $('#datatable').DataTable();
    var rows = table.rows().nodes().to$()
    for (i = 0; i < rows.length; i++) {
        var rowTime = rows.eq(i).children().eq(0).text()
        if (rowTime.split(':')[0] == '00') { rowTime = rowTime.replace('00:', '24:') }
        if (rowTime > time) {
            table.row(i).scrollTo();
            break;
        }
    }
}

function reloadMathcesInLS() {
    var table = $('#datatable').DataTable();
    var matches = table.rows({ selected: true }).data();
    localStorage.clear();
    fulldata = []
    for (i = 0; i < matches.count(); i++) {
        fulldata.push(matches[i])
        console.log('Add match to LS')
    }
    console.log(JSON.stringify(fulldata))
    if (fulldata.length > 0) {
        localStorage.setItem('matchesForAnalyze', JSON.stringify(fulldata))
    }
}

function changeURLAjax() {
    $('#datatable').DataTable().ajax.reload();
}

setInterval(function () {
    changeURLAjax();
}, 5000);