
function format ( d ) {
    console.log(d);
    var html = '<table class="table">';
    html += '<thead class="table-dark">';
    html += '<tr><th scope="col">Product</th>';
    html += '<th scope="col">Category</th>';
    html += '<th scope="col">PVP</th>';
    html += '<th scope="col">Amount</th>';
    html += '<th scope="col">SubTotal</th> </tr>';
    html += '</thead>';

    html += '<tbody>';
    $.each(d.det, function(key,value){
        html+='<tr>';
        html+='<td>'+ value.prod.name +'</td>';
        html+='<td>'+ value.prod.cat +'</td>';
        html+='<td>'+ value.price +'</td>';
        html+='<td>'+ value.cant +'</td>';
        html+='<td>'+ value.subtotal +'</td>';
        html+='</tr>'
    });
    html+='</tbody>';

    return html;
}

function getSaleData(){
    var sale_table = $('#data').DataTable({
        //responsive: true,
        scrollX:true,
        autoWidth: false,
        destroy: true,
        deferRender:true,
        language: {
            "decimal": "",
            "emptyTable": "No hay información",
            "info": "Mostrando _START_ a _END_ de _TOTAL_ Filas",
            "infoEmpty": "Mostrando 0 to 0 of 0 Entradas",
            "infoFiltered": "(Filtrado de _MAX_ total entradas)",
            "infoPostFix": "",
            "thousands": ",",
            "lengthMenu": "Mostrar _MENU_ Filas",
            "loadingRecords": "Cargando...",
            "processing": "Procesando...",
            "search": "Buscar:",
            "zeroRecords": "Sin resultados encontrados",
            "paginate": {
                "first": "Primero",
                "last": "Ultimo",
                "next": "Siguiente",
                "previous": "Anterior"
            },
        },
        ajax:{
            url:"",
            type:'POST',
            data:{
                'action':'searchdata'
            },
            dataSrc:'',
        },
        columns:[
            {
                "className":      'details-control',
                "orderable":      false,
                "data":           null,
                "defaultContent": '<i class = "fas fa-plus-circle" style="color:green; cursor:pointer;"></ i>'
            },
            {'data':'id'},
            {'data':'cli.names'},
            {'data':'date_joined'},
            {'data':'subtotal'},
            {'data':'iva'},
            {'data':'total'},
            {'data':'total'},
        ],
        columnDefs:[
            {
                targets: [7],
                class:'text-center',
                orderable:false,
                render:function(data,type,row){
                    
                    var buttons = '<a type="button" onclick="openDeleteModal(\'/erp/sale/delete/' + row.id + '/\')" class="btn btn-danger"><i class="fas fa-trash"></i></a> ';
                    buttons += '<a rel="details" type="button" class="btn btn-primary"><i class="fas fa-book"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function(settings,json){

        }
    });

    $('#data tbody')
    .on('click','a[rel="details"]',function(){
        var tr = sale_table.cell($(this).closest('td,li')).index();
        var data = sale_table.row(tr.row).data();
        $('#detail_table').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender:true,
            processData: false,
            contentType: false,
            language: {
                "decimal": "",
                "emptyTable": "No hay información",
                "info": "Mostrando _START_ a _END_ de _TOTAL_ Filas",
                "infoEmpty": "Mostrando 0 to 0 of 0 Entradas",
                "infoFiltered": "(Filtrado de _MAX_ total entradas)",
                "infoPostFix": "",
                "thousands": ",",
                "lengthMenu": "Mostrar _MENU_ Filas",
                "loadingRecords": "Cargando...",
                "processing": "Procesando...",
                "search": "Buscar:",
                "zeroRecords": "Sin resultados encontrados",
                "paginate": {
                    "first": "Primero",
                    "last": "Ultimo",
                    "next": "Siguiente",
                    "previous": "Anterior"
                },
            },
            ajax:{
                url:'',
                type:'POST',
                data:{
                    'action':'search_details_product',
                    'id': data.id
                },
                dataSrc:'',
            },
            columns:[
                {'data':'prod.name'},
                {'data':'prod.cat'},
                {'data':'price'},
                {'data':'cant'},
                {'data':'subtotal'},
            ],
            columnDefs:[

            ],
            initComplete: function(settings,json){
    
            }
        });
        $('#detailModal').modal('show');
    })
    .on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = sale_table.row( tr );
 
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
            $(this).html('<i class = "fas fa-plus-circle" style="color:green; cursor:pointer;"></ i>')
        }
        else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
            $(this).html('<i class = "fas fa-minus-circle" style="color:red; cursor:pointer;"></ i>')
        }
    });
};