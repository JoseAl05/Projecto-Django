var prod_table;
var vents = {
    items:{
        cli:'',
        date_joined:'',
        subtotal:0.00,
        iva:0.00,
        total:0.00,
        products:[]
    },

    ////////////Funcion para caluclar subtotal,iva y total de la venta///////////////

    calculate_invoice: function(){
        var subtotal = 0.00;
        var iva = $('input[name="iva"]').val();
        $.each(this.items.products, function(pos,dict){
            dict.subtotal = dict.cant * parseFloat(dict.pvp);
            subtotal += dict.subtotal
        })
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * iva;
        this.items.total = this.items.subtotal + this.items.iva;

        $('input[name = "subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name = "iva_calculated"]').val(this.items.iva.toFixed(2));
        $('input[name = "total"]').val(this.items.total.toFixed(2));
    },

    //////////////Funcion para inicializar la datatable///////////////////

    list: function(){
        this.calculate_invoice();
        prod_table = $('#prod_table').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            columns:[
                {'data':'id'},
                {'data':'name'},
                {'data':'cat'},
                {'data':'pvp'},
                {'data':'cant'},
                {'data':'subtotal'},
            ],
            columnDefs:[
                {
                    targets: [0],
                    class:'text-center',
                    orderable:false,
                    render:function(data,type,row){
                        
                        var buttons = '<a rel="remove" class="btn btn-danger"><i class="fas fa-trash"></i></a> '//'<button type="button" onclick="openDeleteModal(\'/erp/category/delete/' + row.id + '/\')" class="btn btn-danger"><i class="fas fa-trash"></i></button> ';
                        return buttons;
                    }
                },
                {
                    targets: [3,5],
                    class:'text-center',
                    orderable:false,
                    render:function(data,type,row){
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [4],
                    class:'text-center',
                    orderable:false,
                    render:function(data,type,row){
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete = "off" value="'+ row.cant +'" />';
                    }
                },
            ],
            rowCallback( row, data, displayNum, displayIndex, dataIndex ){
                $(row).find('input[name="cant"]').TouchSpin({
                    min: 0,
                    max: 1000,
                    step: 1,
                });
            },
            initComplete: function(settings,json){
    
            }
        });
    },

    ///////////////Function para añadir los productos al array de productos dentro del objeto items y renderizar la datatable con la nueva info/////////////////////

    add: function(item){
        this.items.products.push(item);
        this.list();
    }
};

///////////////Inicializar Select2 para la seleccion de clientes///////////////////
$(function(){
    $('select2').select2({
        theme:'bootstrap4',
        language:'es'
    });
});


$('input[name="iva"]').on('change keyup',function(){
    vents.calculate_invoice();
}).val(0.19);

$('input[name="search"]').autocomplete({
    source: function(request,response){
        $.ajax({
            url: window.location.pathname,
            type:'POST',
            data: {
                'action' : 'search_product',
                'term': request.term
            },
            dataType:'json',
        }).done(function(data){
            response(data);
        }).fail(function(jqXHR,textStatus,errorThrown){
            //alert(textStatus+':'+errorThrown);
        });
    },
    delay:500,
    minLength:1,
    select: function( event, ui ) {
        event.preventDefault();
        ui.item.cant = 1;
        ui.item.subtotal = 0.00;

        vents.add(ui.item);

        $(this).val('');
    }
});

$('#prod_table tbody')
    .on('click','a[rel="remove"]',function(){
        var tr = prod_table.cell($(this).closest('td,li')).index();
        Swal.fire({
            title: 'Do yo want to delete this item?',
            showDenyButton: true,
            confirmButtonText: 'Yes',
            denyButtonText: `No`,
            confirmButtonColor: '#8fce00',
        }).then(function(result){
            if(result.isConfirmed){
                vents.items.products.splice(tr.row,1);
                vents.list();
            }else if(result.isDenied){
                Swal.fire({
                    title:'Nothing was deleted!',
                    icon:'info',
                    position:'top-end',
                    showConfirmButton: false,
                    timer:1000
                })
            }
        })
        // var tr = prod_table.cell($(this).closest('td,li')).index();
        // vents.items.products.splice(tr.row,1);
        // vents.list();
    })
    .on('change keyup','input[name="cant"]',function(){
        var cant = parseInt($(this).val());
        var tr = prod_table.cell($(this).closest('td,li')).index();
        vents.items.products[tr.row].cant = cant;
        vents.calculate_invoice();
        $('td:eq(5)', prod_table.row(tr.row).node()).html( '$'+ vents.items.products[tr.row].subtotal.toFixed(2) );
    });

$('.btnRemoveAll').on('click',function(){
    if(vents.items.products.length === 0){
        return false;
    }

    Swal.fire({
        title: 'Do yo want to delete all this items?',
        showDenyButton: true,
        confirmButtonText: 'Yes',
        denyButtonText: `No`,
        confirmButtonColor: '#8fce00',
    }).then(function(result){
        if(result.isConfirmed){
            vents.items.products = [];
            vents.list();
        }else if(result.isDenied){
            Swal.fire({
                title:'Nothing was deleted!',
                icon:'info',
                position:'top-end',
                showConfirmButton: false,
                timer:1000
            })
        }
    });
});

$('form').on('submit',function(e){
    e.preventDefault();

    if(vents.items.products.length === 0){
        message_category_error('No data in table');
        return false;
    }


    vents.items.date_joined = $('input[name="date_joined"]').val();
    vents.items.cli = $('select[name="cli"]').val()


    var parameters = new FormData();
    parameters.append('action',$('input[name="action"]').val());
    parameters.append('vents',JSON.stringify(vents.items));
    submit_sale(window.location.pathname,parameters);
})

$('.btnClear').on('click',function(){
    $('input[name="search"]').val('').focus();
})

vents.list();





function message_sale_error(obj){
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

function delete_sale(url,params){
    Swal.fire({
        title: 'Do yo want to delete this Sale?:',
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
                        title: 'Sale eliminated!',
                        position:'top-end',
                        icon:'success',
                        showConfirmButton: false,
                    });

                    getSaleData();

                    $('#deleteModal').modal('hide');

                    return false;
                }
                //Si hubo algun error al ingresar los datos se muestra la alerta con los errores
                message_sale_error(data.error);
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

function submit_sale(url,params){
    //Se pregunta si se desea añadir la categoria ingresada
    Swal.fire({
        title: 'Do yo want to add this sale?',
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
                processData: false,
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
                    return false;
                }
                //Si hubo algun error al ingresar los datos se muestra la alerta con los errores
                message_category_error(data.error);
            }).fail(function(jqXHR,textStatus,errorThrown){
                alert(textStatus+':'+errorThrown);
            })
        }else if(result.isDenied){
            Swal.fire({
                title:'Do you want to add another sale?',
                showDenyButton: true,
                confirmButtonText: 'Yes',
                denyButtonText: 'No', 
            }).then(function(result){
                if(result.isConfirmed){
                    Swal.fire({
                        title:'Enter a new sale',
                        icon:'info',
                        timer:1500
                    });
                }else if(result.isDenied){
                    Swal.fire({
                        title:'Nothing was added!',
                        icon:'info',
                        position:'top-end',
                        showConfirmButton: false,
                        timer:1500
                    })
                }
            });
        }
    });
}