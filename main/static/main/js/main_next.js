$("#success-danger").hide();

function setupData() {
    var table = $('#datatable').DataTable({
        ajax: {
            "url": "/ajax/0/next_matches",
            "data": "",
            "dataType": "json",
            "dataSrc": "data",
            "contentType": "application/json"
        },
        scrollResize: true,
        paging: true,
        saveState: true,
        ordering: false,
        deferRender: true,
        scrollY: 100,
        scrollX: true,
        scrollCollapse: true,
        scroller: {
            loadingIndicator: true,
            displayBuffer: 2000
        },
        searching: false,
        dom: "it",
        rowId: 'match_name',
        select: {
            'style': 'multi+shift'
        },
        columns: [
            { "data": "time", "width": "80px" },
            { "data": "league_name" },
            { "data": "match_name" },
            { "data": "coef_p1", "width": "60px" },
            { "data": "coef_x", "width": "60px" },
            { "data": "coef_p2", "width": "60px" }
        ],
        language: {
            "decimal": "",
            "emptyTable": "Нет данных",
            "infoEmpty": "",
            "infoPostFix": "",
            "thousands": ",",
            "lengthMenu": "Показывать по _MENU_ матчей",
            "loadingRecords": "Загрузка данных...",
            "processing": "Обработка...",
            "search": "Поиск:",
            "zeroRecords": "Таких матчей нет",
            'select': {
                'rows': {
                    _: "Выбрано матчей - %d",
                    0: "Выберите матчи для анализа",
                }
            }
        },
        'infoCallback': function (settings, start, end, max, total, pre) {
            if (oldMatches) {
                return "Вчера было " + total + " матчей."
            } else {
                return "Сегодня ожидается " + total + " матчей."
            }
        }
    })

    table
        .on('select', function (e, dt, type, indexes) {
            var selected = table.rows({ selected: true }).nodes().to$()
            for (i = 0; i < selected.length; i++) {
                if (selected.eq(i).children().eq(4).text() != '') {
                    selected.eq(i).addClass('table-success text-dark')
                } else {
                    table.row(selected.eq(i)).deselect()
                    $("#success-danger").removeClass('d-none')
                    $("#success-danger").fadeTo(2000, 500).slideUp(300, function () {
                        $("#success-danger").slideUp(300);
                    });
                }
            }
        })
        .on('deselect', function (e, dt, type, indexes) {
            table.rows({ selected: false }).nodes().to$().removeClass('table-success text-dark')
        });

    $('#datatable_info').addClass('text-center mb-2');
}
$(window).on("load", setupData);

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

var oldMatches = false
$(get_old_matches).click(function () {
    if (oldMatches) {
        oldMatches = false;
        changeAJAXURL('/ajax/0/next_matches');
        $(get_old_matches).removeClass('btn-success').addClass('btn-custom-dark');
        $(to_next).removeClass('disabled');
    } else {
        oldMatches = true;
        changeAJAXURL('/ajax/1/next_matches');
        $(get_old_matches).removeClass('btn-custom-dark').addClass('btn-success');
        $(to_next).addClass('disabled');
    }
});

function changeAJAXURL(url) {
    $('#datatable').DataTable().ajax.url(url).load();
    $('#datatable').DataTable().draw().scroller.toPosition(0, false);
}

function toNextMatches() {
    var table = $('#datatable').DataTable();
    var rows = table.rows().nodes().to$()
    for (i = 0; i < rows.length; i++) {
        if (rows.eq(i).children().eq(4).text() == '') {
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
    }
    if (fulldata.length > 0) {
        localStorage.setItem('matchesForAnalyze', JSON.stringify(fulldata))
    }
}

function changeURLAjax() {
    $('#datatable').DataTable().ajax.reload();
}

setInterval(function () {
    if (!oldMatches) {
        changeURLAjax();
    }
}, 5000);