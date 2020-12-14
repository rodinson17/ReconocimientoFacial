/* new register loan */
$('#saveLoan').click(function() {    
    const token = $("input[name='csrfmiddlewaretoken']").val();
    var dataForm = $('#sendLoan').serialize();

    $.ajax({
        url: '/guardar-prestamo',
        method: 'POST', // or another (GET), whatever you need POST
        //dataType: "json",
        data: dataForm,
        /* data: {
            state: 
            name: value, // data you need to pass to your function
            click: true
        }, */
        headers: { 'X-CSRFToken': token },
        success: function (response) {  
            console.log('llega: ', response) 
            $('#infoLoan').empty();  
            $('#infoLoan').append(response);   
            $('#modalNewLoan').modal('toggle')         
        },
        error: function (error) {   
            console.log(error)     
        }
    });
});

/* setear información a el textarea de observaciones de un libro */
$('#observations').html($('#observations_value').val())

/* update data of book */
$('#sendUpdateBook').click(function() {   
    const token = $("input[name='csrfmiddlewaretoken']").val();
    var dataForm = $('#dataUpdateBook').serialize();
    urlUpdate = '/actualizar-libro/' + $('#id_book').val() 

    $.ajax({
        url: urlUpdate,
        method: 'POST', 
        data: dataForm,
        headers: { 'X-CSRFToken': token },
        success: function (response) {  
            console.log('llega: ', response)       
        },
        error: function (error) {   
            console.log(error)     
        }
    });
});