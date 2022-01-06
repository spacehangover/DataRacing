$(function(){
    //function to show modelo
    var showmodelo = function(selectedmarca){
     $('#modelo option').hide();
        $('#modelo').find('option').filter(function(){
            var modelo = $(this).text();
            return modelo.indexOf(selectedmarca)!=-1;
        }).show();
        //set default value
        var defaultmodelo = $('#modelo option:visible:first').text();
        $('#modelo').val(defaultmodelo);
    };

    //set default marca
    var marca = $('#marca').val();
    showmodelo(marca);

    //on change event call showmodelo function 
    $('#marca').change(function(){
       showmodelo($(this).val());
    });
});