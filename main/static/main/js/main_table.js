function setupData() {
    var table = $('#datatable').DataTable({
        "ajax": {
            "url": "/ajax/table_matches",
            "data": "",
            "dataType": "json",
            "dataSrc": "data",
            "contentType": "application/json"
        },
        "ordering": false,
        "deferRender": true,
        "scrollY": '50vh',
        "scrollX": true,
        "scrollCollapse": true,
        "scroller": true,
        "searching": false,
        "fixedHeader": true,
        "dom": "<'row'<'col-sm-2'i><'col-sm-2'><'col-sm-4 text-center'><'col-sm-4'>t>",
        "columns": [
            { "data": "date" },
            { "data": "league_name" },
            { "data": "match_name" },
            { "data": "total_score" },
            { "data": "first_half_score" },
            { "data": "coef_p1", "width": "53px" },
            { "data": "coef_x", "width": "53px" },
            { "data": "coef_p2", "width": "53px" },
            { "data": null, "defaultContent": "", "width": "25px" },
            { "data": null, "defaultContent": "", "width": "25px" },
            { "data": null, "defaultContent": "", "width": "25px" },
            { "data": null, "defaultContent": "", "width": "25px" },
            { "data": null, "defaultContent": "", "width": "25px" },
            { "data": null, "defaultContent": "", "width": "25px" },
            { "data": null, "defaultContent": "", "width": "25px" },
            { "data": null, "defaultContent": "", "width": "25px" },
            { "data": null, "defaultContent": "", "width": "25px" },
            { "data": null, "defaultContent": "", "width": "25px" },
            { "data": null, "defaultContent": "", "width": "25px" },
            { "data": null, "defaultContent": "", "width": "25px" }
        ],
        "rowCallback": function (row, data, index) {
            for (i = 0; i < 20; i++) {
                $('td', row).eq(i).addClass('border border-secondary');
            }
            var r1 = parseInt(data.total_score.split(':')[0]);
            var r2 = parseInt(data.total_score.split(':')[1]);
            var r1_t = parseInt(data.first_half_score.split(':')[0]);
            var r2_t = parseInt(data.first_half_score.split(':')[1]);
            var p1 = false;
            var p2 = false;
            var n = false;
            var p1_t = false;
            var p2_t = false;
            var n_t = false;
            if (r1 > r2) { p1 = true; $('td', row).eq(5).css('background-color', 'DarkOliveGreen'); }
            if (r2 > r1) { p2 = true; $('td', row).eq(7).css('background-color', 'DarkOliveGreen'); }
            if (r1 == r2) { n = true; $('td', row).eq(6).css('background-color', 'DarkOliveGreen'); }
            if (r1_t > r2_t) { p1_t = true; }
            if (r2_t > r1_t) { p2_t = true; }
            if (r1_t == r2_t) { n_t = true; }

            if ((r1 + r2) >= 3) { $('td', row).eq(8).css('background-color', 'DarkGreen').text('X'); }
            if ((r1 + r2) < 3) { $('td', row).eq(9).css('background-color', 'DarkGreen').text('X'); }
            if ((r1 > 0) && (r2 > 0)) { $('td', row).eq(10).css('background-color', 'DarkGreen').text('X'); }
            if (p1_t && p1) { $('td', row).eq(11).css('background-color', 'DarkGreen').text('X'); }
            if (n_t && p1) { $('td', row).eq(12).css('background-color', 'DarkGreen').text('X'); }
            if (p2_t && p1) { $('td', row).eq(13).css('background-color', 'DarkGreen').text('X'); }
            if (p1_t && n) { $('td', row).eq(14).css('background-color', 'DarkGreen').text('X'); }
            if (p2_t && n) { $('td', row).eq(15).css('background-color', 'DarkGreen').text('X'); }
            if (p1_t && p2) { $('td', row).eq(16).css('background-color', 'DarkGreen').text('X'); }
            if (n_t && p2) { $('td', row).eq(17).css('background-color', 'DarkGreen').text('X'); }
            if (p2_t && p2) { $('td', row).eq(18).css('background-color', 'DarkGreen').text('X'); }
            if (n_t && n) { $('td', row).eq(19).css('background-color', 'DarkGreen').text('X'); }

        },
        "language": {
            "decimal": "",
            "emptyTable": "Матчей не найдено",
            "info": "Показано _TOTAL_ матчей",
            "infoEmpty": "",
            "infoFiltered": "(Фильтр на основе _MAX_ матчей)",
            "infoPostFix": "",
            "thousands": ",",
            "lengthMenu": "Показывать по _MENU_ матчей",
            "loadingRecords": "Загрузка данных...",
            "processing": "Обработка...",
            "search": "Поиск:",
            "zeroRecords": "Матчей не найдено",
            "paginate": {
                "first": "Первая",
                "last": "Последняя",
                "next": "Вперед",
                "previous": "Назад"
            },
            "aria": {
                "sortAscending": ": activate to sort column ascending",
                "sortDescending": ": activate to sort column descending"
            }
        },
    });
    $('#datatable_info').addClass('text-white');
}
$(window).on("load", setupData);
$(window).on("load", getMatchesToAnalyze);

$('input.column_filter').on('input', function () {
    $(this).val($(this).val().replace(/\,/g, '.'));
    $(this).val($(this).val().replace(
        /(?=(\d+\.\d{2})).+|(\.(?=\.))|([^\.\d])|(^\D)/gi, '$1'));
});

$(document).ready(function () {
    $('#searchLigue').keyup(function () {
        changeURLAjax();
    });
    $('input.column_filter').keyup(function () {
        changeURLAjax();
    });
    $('#selectCountry').change(function () {
        changeURLAjax();
    });
    function reloadValSelect() {
        var opt = $('#selectMatch').children("option:selected")
        if (opt.val() == 0) {
            $("#col5_filter").val('');
            $("#col6_filter").val('');
            $("#col7_filter").val('');
        } else {
            $("#col5_filter").val(opt.attr('cp1'));
            $("#col6_filter").val(opt.attr('cx'));
            $("#col7_filter").val(opt.attr('cp2'));
        }
        changeURLAjax();
    };
    var scrollTimer = null;
    $('#selectMatch').on('wheel', function (e) {
        e.preventDefault();
        var len = this.length,
        i = this.selectedIndex;
        if (e.originalEvent.wheelDelta > 0 || e.originalEvent.detail < 0) {
            this.selectedIndex = --i == -1 ? len - 1 : i;
        } else {
            this.selectedIndex = ++i % len;
        }
        if (scrollTimer) {
            clearTimeout(scrollTimer);   // clear any previous pending timer
        }
        scrollTimer = setTimeout(reloadValSelect, 300);   // set new timer
        //reloadValSelect();
    });
    $('#selectMatch').change(function () {
        reloadValSelect();
    });
    $('#deleteSelectMatch').click(function () {
        var opt = $('#selectMatch').children("option:selected")
        if (opt.val() > 0) {
            deleteMatchFromLS(opt.val())
            setNullValue()
        }
    });
    $('#deleteAllMatch').click(function () {
        localStorage.clear()
        getMatchesToAnalyze()
        setNullValue()
    });
});

function getMatchesToAnalyze() {
    var matches = JSON.parse(localStorage.getItem('matchesForAnalyze'));
    $('#selectMatch').empty()
    if (LSIsNotEmtpy(matches)) {
        $('#selectMatch').append('<option value=0>Выбрать матч...</option>')
        for (i = 0; i < matches.length; i++) {
            $('#selectMatch').append(`<option value="${i + 1}"
                    cP1=${matches[i]["coef_p1"]} 
                    cX=${matches[i]["coef_x"]} 
                    cP2=${matches[i]["coef_p2"]} >${matches[i]["league_name"]}: ${matches[i]["match_name"]}
                    </option>`)
        }
    }
}

function deleteMatchFromLS(index) {
    var beforeDelete = JSON.parse(localStorage.getItem('matchesForAnalyze'));
    beforeDelete.splice(index - 1, 1);
    if (beforeDelete.length > 0) {
        localStorage.setItem('matchesForAnalyze', JSON.stringify(beforeDelete))
    } else {
        localStorage.clear()
    }
    getMatchesToAnalyze()
}

function LSIsNotEmtpy(matches) {
    if (matches) {
        $('#matchAnalyze').removeClass('d-none')
        return true
    } else {
        $('#matchAnalyze').addClass('d-none')
        return false
    }
}

function setNullValue() {
    $("#col5_filter").val('');
    $("#col6_filter").val('');
    $("#col7_filter").val('');
    changeURLAjax();
}

function changeURLAjax() {
    var url = "/ajax/table_matches";
    url += "?p1=" + $(col5_filter).val();
    url += "&x=" + $(col6_filter).val();
    url += "&p2=" + $(col7_filter).val();
    url += "&ligname=" + $(searchLigue).val();
    url += "&country=" + $(selectCountry).val();
    getStatMatch();

    $('#datatable').DataTable().ajax.url(url).load();
    $('#datatable').DataTable().draw().scroller.toPosition(0, false);
}

function getStatMatch() {
    var p1 = $(col5_filter).val();
    var x = $(col6_filter).val();
    var p2 = $(col7_filter).val();
    var ligname = $(searchLigue).val();
    var country = $(selectCountry).val();
    $.ajax({
        type: 'GET',
        url: "/ajax/stat_match",
        data: {
            "p1": p1,
            "x": x,
            "p2": p2,
            "ligname": ligname,
            "country": country
        },
        success: function (response) {
            if (response["valid"]) {
                $(statP1F).text(response['fltP1']);
                $(statXF).text(response['fltX']);
                $(statP2F).text(response['fltP2']);
                $(statP1C).text(response['countW1']);
                $(statXC).text(response['countN']);
                $(statP2C).text(response['countW2']);
                document.querySelectorAll('#fs_p1')[1].innerHTML = response['percentW1'] + '%'
                document.querySelectorAll('#fs_x')[1].innerHTML = response['percentN'] + '%'
                document.querySelectorAll('#fs_p2')[1].innerHTML = response['percentW2'] + '%'
                document.querySelectorAll('#fs_tb')[1].innerHTML = response['advanced']['tb25'] + '%'
                document.querySelectorAll('#fs_tm')[1].innerHTML = response['advanced']['tm25'] + '%'
                document.querySelectorAll('#fs_oz')[1].innerHTML = response['advanced']['oz'] + '%'
                document.querySelectorAll('#fs_p1p1')[1].innerHTML = response['advanced']['p1p1'] + '%'
                document.querySelectorAll('#fs_xp1')[1].innerHTML = response['advanced']['xp1'] + '%'
                document.querySelectorAll('#fs_p2p1')[1].innerHTML = response['advanced']['p2p1'] + '%'
                document.querySelectorAll('#fs_p1x')[1].innerHTML = response['advanced']['p1x'] + '%'
                document.querySelectorAll('#fs_p2x')[1].innerHTML = response['advanced']['p2x'] + '%'
                document.querySelectorAll('#fs_p1p2')[1].innerHTML = response['advanced']['p1p2'] + '%'
                document.querySelectorAll('#fs_xp2')[1].innerHTML = response['advanced']['xp2'] + '%'
                document.querySelectorAll('#fs_p2p2')[1].innerHTML = response['advanced']['p2p2'] + '%'
                document.querySelectorAll('#fs_xx')[1].innerHTML = response['advanced']['xx'] + '%'
            }
            if (!response["valid"]) {
                $(statP1F).text('');
                $(statXF).text('');
                $(statP2F).text('');
                $(statP1C).text('');
                $(statXC).text('');
                $(statP2C).text('');
                document.querySelectorAll('#fs_p1')[1].innerHTML = 'П1'
                document.querySelectorAll('#fs_x')[1].innerHTML = 'Х'
                document.querySelectorAll('#fs_p2')[1].innerHTML = 'П2'
                document.querySelectorAll('#fs_tb')[1].innerHTML = 'ТБ 2.5'
                document.querySelectorAll('#fs_tm')[1].innerHTML = 'ТМ 2.5'
                document.querySelectorAll('#fs_oz')[1].innerHTML = 'ОЗ'
                document.querySelectorAll('#fs_p1p1')[1].innerHTML = 'П1/П1'
                document.querySelectorAll('#fs_xp1')[1].innerHTML = 'Н/П1'
                document.querySelectorAll('#fs_p2p1')[1].innerHTML = 'П2/П1'
                document.querySelectorAll('#fs_p1x')[1].innerHTML = 'П1/Н'
                document.querySelectorAll('#fs_p2x')[1].innerHTML = 'П2/Н'
                document.querySelectorAll('#fs_p1p2')[1].innerHTML = 'П1/П2'
                document.querySelectorAll('#fs_xp2')[1].innerHTML = 'Н/П2'
                document.querySelectorAll('#fs_p2p2')[1].innerHTML = 'П2/П2'
                document.querySelectorAll('#fs_xx')[1].innerHTML = 'Н/Н'
            }
        },
        error: function (response) {
            console.log('ERROR: ' + response)
            console.log(response)
        }
    })
}

