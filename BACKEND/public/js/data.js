$(document).ready(function(){
    $("#owner_ref").select2({
        width:'resolve'
    });
    $(".form-control").keyup(function(){
        
        $(this).removeClass('is-invalid').addClass('is-valid');
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
    });
