$(function(){
    $('select[name="groups"]').select2({
        theme:'bootstrap4',
        language:'es',
        placeholder:'buscar...',
    });
});

function message_user_error(obj){
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

function submit_user(url,params){
    //Se pregunta si se desea añadir la categoria ingresada
    Swal.fire({
        title: 'Do yo want to add this user?',
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
                dataType:'json'
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

                    getUserData();

                    $('#createModal').modal('hide');

                    return false;
                }
                //Si hubo algun error al ingresar los datos se muestra la alerta con los errores
                message_user_error(data.error);
            }).fail(function(jqXHR,textStatus,errorThrown){
                alert(textStatus+':'+errorThrown);
            })
        }else if(result.isDenied){
            Swal.fire({
                title:'Do you wante to add another user?',
                showDenyButton: true,
                showCancelButton: true,
                confirmButtonText: 'Yes',
                denyButtonText: 'No', 
            }).then(function(result){
                if(result.isConfirmed){
                    Swal.fire({
                        title:'Enter a new user',
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

                    $('#createModal').modal('hide');

                }
            });
        }
    });
}

function edit_user(url,params){
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
                processData: false,
                contentType: false,
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

                    getUserData();

                    $('#editModal').modal('hide');

                    return false;
                }
                //Si hubo algun error al ingresar los datos se muestra la alerta con los errores
                message_user_error(data.error);
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
        $('#editModal').modal('hide');
    });
}

function edit_profile_user(url,params){
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
                dataType:'json'
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
                    setTimeout(function () {
                        location.href = "/erp/dashboard/"; 
                     }, 1000);
                    return false;
                }
                //Si hubo algun error al ingresar los datos se muestra la alerta con los errores
                message_user_error(data.error);
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

function reset_password_user(url,params){
    Swal.fire({
        title: 'Do yo want to reset your password?',
        showDenyButton: true,
        confirmButtonText: 'Save',
        denyButtonText: `Don't save`,
        confirmButtonColor: '#8fce00',
    }).then(function(result){
        if(result.isConfirmed){
            Swal.fire({
                title:'Sending email',
                html:'Pleas Wait..',
                allowEscapeKey: false,
                allowOutsideClick: false,
                showLoaderOnConfirm:true,
                didOpen:()=>{
                    Swal.showLoading()
                }
            })
            $.ajax({
                url: url,
                type:'POST',
                data: params,
                dataType:'json',
                processData: false,
                contentType: false,
            }).done(function(data){
                //Si no hubo error en la peticion, se le da el mensaje al usuario de que la accion fue correcta y se redirige a la lista de catgorias
                if(!data.hasOwnProperty('error')){
                    Swal.fire({
                        title: 'Notification',
                        position:'top-end',
                        icon:'success',
                        text:'We send you an email to change your password',
                        showConfirmButton: true,
                    });
                    setTimeout(function () {
                        location.href = "/login"; 
                     }, 1000);
                    return false;
                }
                //Si hubo algun error al ingresar los datos se muestra la alerta con los errores
                message_user_error(data.error);
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

function change_password_user(url,params){
    Swal.fire({
        title: 'Do yo want to change your password?',
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
                processData: false,
                contentType: false,
            }).done(function(data){
                //Si no hubo error en la peticion, se le da el mensaje al usuario de que la accion fue correcta y se redirige a la lista de catgorias
                if(!data.hasOwnProperty('error')){
                    Swal.fire({
                        title: 'Password changed!',
                        position:'top-end',
                        icon:'success',
                        showConfirmButton: false,
                        timer:1000
                    });
                    setTimeout(function () {
                        location.href = "/"; 
                     }, 1000);
                    return false;
                }
                //Si hubo algun error al ingresar los datos se muestra la alerta con los errores
                message_user_error(data.error);
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

function delete_user(url,params,name){
    Swal.fire({
        title: 'Do yo want to delete this User?: \n' + name,
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
                dataType:'json'
            }).done(function(data){
                //Si no hubo error en la peticion, se le da el mensaje al usuario de que la accion fue correcta y se redirige a la lista de catgorias
                if(!data.hasOwnProperty('error')){
                    Swal.fire({
                        title: 'User eliminated!',
                        position:'top-end',
                        icon:'success',
                        showConfirmButton: false,
                        timer:1000
                    });

                    getUserData();

                    $('#deleteModal').modal('hide');

                    return false;
                }
                //Si hubo algun error al ingresar los datos se muestra la alerta con los errores
                message_user_error(data.error);
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