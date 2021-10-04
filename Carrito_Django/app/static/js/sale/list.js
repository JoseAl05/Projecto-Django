function getSaleData(){
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender:true,
        ajax:{
            url:"",
            type:'POST',
            data:{
                'action':'searchdata'
            },
            dataSrc:'',
        },
        columns:[
            {'data':'id'},
            {'data':'cli'},
            {'data':'date_joined'},
            {'data':'subtotal'},
            {'data':'iva'},
            {'data':'total'},
            {'data':'total'},
        ],
        columnDefs:[
            {
                targets: [6],
                class:'text-center',
                orderable:false,
                render:function(data,type,row){
                    
                    var buttons = '<button type="button" onclick="openDeleteModal(\'/erp/sale/delete/' + row.id + '/\')" class="btn btn-danger"><i class="fas fa-trash"></i></button> ';
                    buttons += '<button type="button" class="btn btn-warning" onclick="openEditModal(\'/erp/sale/update/' + row.id + '/\')"><i class="fas fa-edit"></i></button>';
                    return buttons;
                }
            },
        ],
        initComplete: function(settings,json){

        }
    });
};