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

function desplegar_variables(divId)
{
    const divElt = document.getElementById(divId);

    if(divElt){
        if (divElt.style.display === 'none') || divElement.style.display === "")
        {
            divElt.style.display = 'block'; //divId está desplegado
        }else{
            divElt.style.display = 'none'; //divId está oculto
    }else{
        console.error('No se encontró el elemento con id: ' + divId);
    }
}