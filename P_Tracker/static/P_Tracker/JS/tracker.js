if (location.hash) {
    $('a[href=\'' + location.hash + '\']').tab('show');
}
var activeTab = localStorage.getItem('activeTab');
if (activeTab) {
    $('a[href="' + activeTab + '"]').tab('show');
}

$('body').on('click', 'a[data-toggle=\'tab\']', function (e) {
    e.preventDefault()
    var tab_name = this.getAttribute('href')
    if (history.pushState) {
        history.pushState(null, null, tab_name)
    }
    else {
        location.hash = tab_name
    }
    localStorage.setItem('activeTab', tab_name)

    $(this).tab('show');
    return false;
});
$(window).on('popstate', function () {
    var anchor = location.hash ||
        $('a[data-toggle=\'tab\']').first().attr('href');
    $('a[href=\'' + anchor + '\']').tab('show');
});

function setInputDate(_id) {
    var _dat = document.querySelector(_id);
    var hoy = new Date(),
        d = hoy.getDate(),
        m = hoy.getMonth() + 1,
        y = hoy.getFullYear(),
        data;
    if (d < 10) {
        d = "0" + d;
    }
    ;
    if (m < 10) {
        m = "0" + m;
    }
    ;
    data = y + "-" + m + "-" + d;
    console.log(data);
    _dat.value = data;
};
setInputDate("#date1");
setInputDate("#date2");
setInputDate("#date3");