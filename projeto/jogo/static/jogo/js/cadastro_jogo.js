$( document ).ready(function() {
    changeFase();

    $("#id_chave").on('change', carregarDuplasChave);
    $("#id_etapa").on('change', carregarDuplasChave);
    $("#id_fase").on('change', changeFase);
});

function carregarDuplasChave(){
    let chaveId = $('#id_chave').val();
    let etapaId = $('#id_etapa').val();

    if(chaveId || etapaId){
        $.ajax({
        type: 'POST',
        url: $('#url_ajax_duplas_chave').val(),
        data: {
            'chave_id': chaveId,
            'etapa_id': etapaId
        },
        }).done(function (resposta) {
            var opcoes = '<option selected value></option>';
            for (i = 0; i < resposta.lista_duplas.length; i++) {
                opcoes += '<option value="' + resposta.lista_duplas[i].id + '">' + resposta.lista_duplas[i].descricao + '</option>'
            }
            $('#id_timeA').html(opcoes).trigger('change');
            $('#id_timeB').html(opcoes).trigger('change');
        }).fail(function () {
            alert('Erro ao buscar as duplas da chave selecionada!');
        });
    }else{
        $('#id_timeA').html('');
        $('#id_timeB').html('');
    }
}

function changeFase(){
    let fase = $('#id_fase').val();

    if(fase == 'CLASSIFICATÓRIA'){
        $('#id_timeA').html('');
        $('#id_timeB').html('');
        $('#id_chave').attr('readonly', false).attr('disabled', false);
    }else{
        $('#id_chave').attr('readonly', true).attr('disabled', true).val('');
    }

    carregarDuplasChave();
}