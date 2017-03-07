$(document).ready(function() {

    // Mascaras nos campos dos forms
    $(function(){
        $('#id_cpf').mask('999.999.999-99');
        $('#id_birth_date').mask('99/99/9999');
        $('#id_zip_code').mask('99999-999');
        $('#id_home_phone').mask('9999-9999');
        $('#id_cell_phone').mask('9999-9999');
    });

    function procura_cep(cep){
        $.post('/locations/refresh-address/', {'zipcode': cep.replace("-", "")}, function(data){
            if (data.empty){
                $('.street #id_street').val('');
                $('.state #id_state').val('');
                $('.state strong').text('');
                $('.city #id_city').val('');
                $('.city strong').text('');
                $('.area #id_area').val('');
                $('.area strong').text('');
            }
            else{
                $('.street #id_street').val(data.address);
                $('.state #id_state').val(data.id_state);
                $('.state strong').text(data.state);
                $('.city #id_city').val(data.id_city);
                $('.city strong').text(data.city);
                $('.area #id_area').val(data.id_area);
                $('.area strong').text(data.area);
            }
        },'json');
    }

    if($('body').find('input#id_zip_code').val() !== ""){
        procura_cep($('#id_zip_code').val());
    }
    $('#id_zip_code').mask('99999-999', {
        completed : function() {
            $('.cep-carregando').show();
            procura_cep(this.val());
        }
    });
    $('#id_zip_code').blur(function(){
        if ($(this).val() !== ""){
            procura_cep($('#id_zip_code').val());
        }
    });
});
