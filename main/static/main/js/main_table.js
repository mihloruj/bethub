function setupData() {
    var table = $('#datatable').DataTable({
        ajax: {
            "url": "/ajax/table_matches",
            "data": "",
            "dataType": "json",
            "dataSrc": "data",
            "contentType": "application/json"
        },
        ordering: false,
        searching: false,
        scrollResize: true,
        deferRender: true,
        scroller: {
            displayBuffer: 150
        },
        scrollY: 100,
        scrollCollapse: true,
        dom: '<t>',
        scrollX: true,
        "columns": [
            { "data": "date", "width": "53px" },
            { "data": "league_name", "width": "53px" },
            { "data": "match_name", "width": "53px" },
            { "data": "total_score", "width": "53px" },
            { "data": "first_half_score", "width": "53px" },
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
            if (r1 > r2) { p1 = true; $('td', row).eq(5).css('background-color', '#5ad478bb'); }
            if (r2 > r1) { p2 = true; $('td', row).eq(7).css('background-color', '#5ad478bb'); }
            if (r1 == r2) { n = true; $('td', row).eq(6).css('background-color', '#5ad478bb'); }
            if (r1_t > r2_t) { p1_t = true; }
            if (r2_t > r1_t) { p2_t = true; }
            if (r1_t == r2_t) { n_t = true; }

            if ((r1 + r2) >= 3) { $('td', row).eq(8).css('background-color', '#5caf71bb').text('X'); }
            if ((r1 + r2) < 3) { $('td', row).eq(9).css('background-color', '#5caf71bb').text('X'); }
            if ((r1 > 0) && (r2 > 0)) { $('td', row).eq(10).css('background-color', '#5caf71bb').text('X'); }
            if (p1_t && p1) { $('td', row).eq(11).css('background-color', '#5caf71bb').text('X'); }
            if (n_t && p1) { $('td', row).eq(12).css('background-color', '#5caf71bb').text('X'); }
            if (p2_t && p1) { $('td', row).eq(13).css('background-color', '#5caf71bb').text('X'); }
            if (p1_t && n) { $('td', row).eq(14).css('background-color', '#5caf71bb').text('X'); }
            if (p2_t && n) { $('td', row).eq(15).css('background-color', '#5caf71bb').text('X'); }
            if (p1_t && p2) { $('td', row).eq(16).css('background-color', '#5caf71bb').text('X'); }
            if (n_t && p2) { $('td', row).eq(17).css('background-color', '#5caf71bb').text('X'); }
            if (p2_t && p2) { $('td', row).eq(18).css('background-color', '#5caf71bb').text('X'); }
            if (n_t && n) { $('td', row).eq(19).css('background-color', '#5caf71bb').text('X'); }

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
            }
        },
    });
}
$(window).on("load", setupData);
$(window).on("load", getMatchesToAnalyze);

setTimeout(reDrawTable, 300);

$('input.column_filter').on('input', function () {
    $(this).val($(this).val().replace(/\,/g, '.'));
    $(this).val($(this).val().replace(
        /(?=(\d+\.\d{2})).+|(\.(?=\.))|([^\.\d])|(^\D)/gi, '$1'));
});

function reDrawTable() {
    $('#datatable').DataTable().columns.adjust().draw();
    console.log('redraw')
}


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

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })

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
        $('#matchAnalyzeInfo').addClass('d-none')
        return true
    } else {
        $('#matchAnalyze').addClass('d-none')
        $('#matchAnalyzeInfo').removeClass('d-none')
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
    setTimeout(reDrawTable, 300);
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
                $(statCount).text(response['count']);
                document.querySelectorAll('#fs_p1')[0].innerHTML = response['percentW1'] + '%'
                document.querySelectorAll('#fs_x')[0].innerHTML = response['percentN'] + '%'
                document.querySelectorAll('#fs_p2')[0].innerHTML = response['percentW2'] + '%'
                document.querySelectorAll('#fs_tb')[0].innerHTML = response['advanced']['tb25'] + '%'
                document.querySelectorAll('#fs_tm')[0].innerHTML = response['advanced']['tm25'] + '%'
                document.querySelectorAll('#fs_oz')[0].innerHTML = response['advanced']['oz'] + '%'
                document.querySelectorAll('#fs_p1p1')[0].innerHTML = response['advanced']['p1p1'] + '%'
                document.querySelectorAll('#fs_xp1')[0].innerHTML = response['advanced']['xp1'] + '%'
                document.querySelectorAll('#fs_p2p1')[0].innerHTML = response['advanced']['p2p1'] + '%'
                document.querySelectorAll('#fs_p1x')[0].innerHTML = response['advanced']['p1x'] + '%'
                document.querySelectorAll('#fs_p2x')[0].innerHTML = response['advanced']['p2x'] + '%'
                document.querySelectorAll('#fs_p1p2')[0].innerHTML = response['advanced']['p1p2'] + '%'
                document.querySelectorAll('#fs_xp2')[0].innerHTML = response['advanced']['xp2'] + '%'
                document.querySelectorAll('#fs_p2p2')[0].innerHTML = response['advanced']['p2p2'] + '%'
                document.querySelectorAll('#fs_xx')[0].innerHTML = response['advanced']['xx'] + '%'
            }
            if (!response["valid"]) {
                $(statP1F).text('');
                $(statXF).text('');
                $(statP2F).text('');
                $(statP1C).text('');
                $(statXC).text('');
                $(statP2C).text('');
                $(statCount).text('');
                document.querySelectorAll('#fs_p1')[0].innerHTML = '-%'
                document.querySelectorAll('#fs_x')[0].innerHTML = '-%'
                document.querySelectorAll('#fs_p2')[0].innerHTML = '-%'
                document.querySelectorAll('#fs_tb')[0].innerHTML = '-%'
                document.querySelectorAll('#fs_tm')[0].innerHTML = '-%'
                document.querySelectorAll('#fs_oz')[0].innerHTML = '-%'
                document.querySelectorAll('#fs_p1p1')[0].innerHTML = '-%'
                document.querySelectorAll('#fs_xp1')[0].innerHTML = '-%'
                document.querySelectorAll('#fs_p2p1')[0].innerHTML = '-%'
                document.querySelectorAll('#fs_p1x')[0].innerHTML = '-%'
                document.querySelectorAll('#fs_p2x')[0].innerHTML = '-%'
                document.querySelectorAll('#fs_p1p2')[0].innerHTML = '-%'
                document.querySelectorAll('#fs_xp2')[0].innerHTML = '-%'
                document.querySelectorAll('#fs_p2p2')[0].innerHTML = '-%'
                document.querySelectorAll('#fs_xx')[0].innerHTML = '-%'
            }
        },
        error: function (response) {
            console.log('ERROR: ' + response)
            console.log(response)
        }
    })
}

