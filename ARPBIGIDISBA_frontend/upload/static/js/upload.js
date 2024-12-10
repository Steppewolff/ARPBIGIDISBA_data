function abrir_modal(url)
{
    $('#upload_modal').load(url, function()
    {
    $(this).modal({
        backdrop: 'static',
        keyboard: false
    })
    $(this).modal('show');
    });
    return false;
}

function cerrar_modal()
{
$('#upload_modal').modal('hide');
return false;
}

var dialog = document.getElementById("myDialog");

function showDialog() {
  dialog.show();
}

function closeDialog() {
  dialog.close();
}