$(document).ready(function(){
    $("#owner_ref").select2({
        width:'resolve'
    });
    $("#userId").select2({
        width: 'resolve'
    });
    let date = new Date();
    $("#date").datepicker({
        "todayHighlight":true,
        "setDate": new Date(date.getFullYear(),date.getMonth(), date.getDay()),
        "autoclose":true
    });
        
    $("#time").timepicker();
    $(".form-control").keyup(function(){
        if($(this).hasClass('is-invalid'))
            {
                $(this).removeClass('is-invalid').addClass('is-valid');           
            }
    });
    $("#userDataSubmit").click((event)=>{
        event.preventDefault();
        $.ajax({
            url:"/api/adduser",
            dataType:'json',
            type:'post',
            contentType:'application/x-www-form-urlencoded',
            data: $('#userAddForm').serialize(),
            success: function(data,textStatus,jqxhr) {
                location.reload();
            },
            error: function(jqxhr,textStatus,errorThrown){
             //TODO: handle error
             console.log(jqxhr);   
            }
        });
    });
    $('#vehicleDataSubmit').click((event)=>{
        event.preventDefault();
        $.ajax({
            url:"/api/addvehicle",
            dataType:'json',
            type:'post',
            contentType:'application/x-www-form-urlencoded',
            data: $('#vehicleAddForm').serialize(),
            success: function(data,textStatus,jqxhr){
                location.reload();
            },
            error: function(jqxhr, textStatus,errorThrown) {
                    switch(jqxhr.responseJSON.response)
                    {
                        case "null owner":
                            $("#owner_ref").addClass('is-invalid').focus();
                            break;
                        case "null license number":
                            $("#licensePlateNo").addClass('is-invalid').focus();
                            break;
                        default:
                        {
                            console.log(jqxhr);
                            err = jqxhr.responseJSON.response.errors[0];

                            $(`#${err.path}`).siblings(".invalid-feedback").text(`the entered ${err.path} already exists`);
                            $(`#${err.path}`).addClass('is-invalid').focus();
                            
                        }
                    }
                }

            });
            
    });
    
    $('#infractionDataSubmit').click(function(event){
        event.preventDefault();
        $.ajax({
            url:"/api/addinfraction",
            dataType:'json',
            type:'post',
            contentType:'application/x-www-form-urlencoded',
            data: $('#infractionAddForm').serialize(),
            success: function(data,textStatus,jqxhr){
                location.reload();
            },
            error: function(jqxhr, textStatus,errorThrown) {
                    switch(jqxhr.responseJSON.response)
                    {
                        case "null date":
                            $("#date").addClass('is-invalid').focus();
                            break;
                        case "null person":
                            $("#userId").addClass('is-invalid').focus();
                            break;
                        case "null time":
                            $("#time").addClass('is-invalid').focus();
                            break;
                        case "null location":
                            $("#location").addClass('is-invalid').focus();
                            break;
                        default:
                        {
                            console.log(jqxhr);
                            err = jqxhr.responseJSON.response.errors[0];

                            $(`#${err.path}`).siblings(".invalid-feedback").text(`the entered ${err.path} already exists`);
                            $(`#${err.path}`).addClass('is-invalid').focus();
                            
                        }
                    }
                }
        });
    })
});
