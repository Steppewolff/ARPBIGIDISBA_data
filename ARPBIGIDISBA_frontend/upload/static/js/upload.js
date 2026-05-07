function abrir_modal(url) {
    var $div = $('#upload_modal');
    $div.load(url, function(response, status, xhr) {
        if (status === "error") {
            console.error("Error HTTP:", xhr.status, xhr.statusText);
            return;
        }
        $(this).modal({ backdrop: 'static', keyboard: false });
        $(this).modal('show');
    });
    return false;
}

function cerrar_modal() {
    $('#upload_modal').modal('hide');
    return false;
}

function showDialog() {
    var dialog = document.getElementById("myDialog");
    dialog.show();
}

function closeDialog() {
    var dialog = document.getElementById("myDialog");
    dialog.close();
}