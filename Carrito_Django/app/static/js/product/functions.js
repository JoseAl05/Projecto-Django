function message_product_error(obj){
    var html = '';
    if(typeof (obj) === 'object'){
        html = '<ul style="text-align: left;">';
        $.each(obj, function(key,value){
            html+='<li>'+key+': '+value+'</li>';
        });
        html += '</ul>'; 
    }
    else{
        html = '<p>'+obj+'</p>'
    }
    Swal.fire({
        icon: 'error',
        title: 'Error',
        html: html,
    });
}

function submit_product(url,params){
    //Se pregunta si se desea añadir la categoria ingresada
    Swal.fire({
        title: 'Do yo want to add this product?',
        showDenyButton: true,
        confirmButtonText: 'Save',
        denyButtonText: `Don't save`,
        confirmButtonColor: '#8fce00',
    }).then(function(result){
        //Si la respuesta es si, se hace la peticion ajax
        if(result.isConfirmed){
            $.ajax({
                url: url,
                type:'POST',
                data: params,
                dataType:'json',
                processData:false,
                contentType:false,
            }).done(function(data){
                //Si no hubo error en la peticion, se le da el mensaje al usuario de que la accion fue correcta y se redirige a la lista de catgorias
                if(!data.hasOwnProperty('error')){
                    Swal.fire({
                        title: 'Saved',
                        position:'top-end',
                        icon:'success',
                        showConfirmButton: false,
                        timer:1000
                    });

                    getProductData();

                    $('#createModal').modal('hide');

                    return false;
                }
                //Si hubo algun error al ingresar los datos se muestra la alerta con los errores
                message_product_error(data.error);
            }).fail(function(jqXHR,textStatus,errorThrown){
                alert(textStatus+':'+errorThrown);
                })
        }else if(result.isDenied){
            Swal.fire({
                title:'Do you want to add another product?',
                showDenyButton: true,
                showCancelButton: true,
                confirmButtonText: 'Yes',
                denyButtonText: 'No', 
            }).then(function(result){
                if(result.isConfirmed){
                    Swal.fire({
                        title:'Enter a new product',
                        icon:'info',
                        timer:1500
                    });
                }else if(result.isDenied){
                    Swal.fire({
                        title:'Nothing was added!',
                        icon:'info',
                        position:'top-end',
                        showConfirmButton: false,
                    })

                    getProductData();

                    $('#createModal').modal('hide');

                }
            });
        }
    });
}

function edit_product(url,params){
    Swal.fire({
        title: 'Do yo want to save the changes?',
        showDenyButton: true,
        confirmButtonText: 'Save',
        denyButtonText: `Don't save`,
        confirmButtonColor: '#8fce00',
    }).then(function(result){
        if(result.isConfirmed){
            $.ajax({
                url: url,
                type:'POST',
                data: params,
                dataType:'json',
                processData:false,
                contentType:false,
            }).done(function(data){
                //Si no hubo error en la peticion, se le da el mensaje al usuario de que la accion fue correcta y se redirige a la lista de catgorias
                if(!data.hasOwnProperty('error')){
                    Swal.fire({
                        title: 'Saved changes!',
                        position:'top-end',
                        icon:'success',
                        showConfirmButton: false,
                        timer:1000
                    });

                    getProductData();

                    $('#editModal').modal('hide');

                    return false;
                }
                //Si hubo algun error al ingresar los datos se muestra la alerta con los errores
                message_category_error(data.error);
            }).fail(function(jqXHR,textStatus,errorThrown){
                alert(textStatus+':'+errorThrown);
                })
        }else if(result.isDenied){
            Swal.fire({
                title:'Nothing was changed!',
                icon:'info',
                position:'top-end',
                showConfirmButton: false,
                timer:1000,
            });
        }
    });
}

function delete_product(url,params,name){
    Swal.fire({
        title: 'Do yo want to delete this Product?: \n' + name,
        showDenyButton: true,
        confirmButtonText: 'Delete',
        denyButtonText: `Don't delete`,
        confirmButtonColor: '#f44336',
        denyButtonColor: '#0073da',
    }).then(function(result){
        if(result.isConfirmed){
            $.ajax({
                url: url,
                type:'POST',
                data: params,
                dataType:'json',
                processData:false,
                contentType:false,
            }).done(function(data){
                //Si no hubo error en la peticion, se le da el mensaje al usuario de que la accion fue correcta y se redirige a la lista de catgorias
                if(!data.hasOwnProperty('error')){
                    Swal.fire({
                        title: 'Product eliminated!',
                        position:'top-end',
                        icon:'success',
                        showConfirmButton: false,
                        timer:1000
                    });

                    getProductData();

                    $('#deleteModal').modal('hide');

                    return false;
                }
                //Si hubo algun error al ingresar los datos se muestra la alerta con los errores
                message_category_error(data.error);
            }).fail(function(jqXHR,textStatus,errorThrown){
                alert(textStatus+':'+errorThrown);
                })
        }else if(result.isDenied){
            Swal.fire({
                title:'Nothing was changed!',
                icon:'info',
                position:'top-end',
                showConfirmButton: false,
                timer:1000,
            });
        }
    });
}


