$(document).ready(function(){
    $("#ownerInput").select2({
        width:'resolve'
    });
    $('#vehicleDataSubmit').click((event)=>{
        event.preventDefault();
        $.ajax({
            url:"/api/addUser",
            dataType:'json',
            type:'post',
            contentType:'application/x-www-form-urlencoded',
            success: function(data,textStatus,jqxhr){
                $('#vehicleAddForm').trigger('reset');
                console.log('success');
                },
            error: function(jqxhr, textStatus,errorThrown) {
                    console.log(textStatus,errorThrown);
                }

            });
            
        });
    });
