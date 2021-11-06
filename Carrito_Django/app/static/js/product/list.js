function getProductData(){
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
            {'data':'name'},
            {'data':'cat'},
            {'data':'stock'},
            {'data':'pvp'},
            {'data':'pvp'},
        ],
        columnDefs:[
            {
                targets: [5],
                class:'text-center',
                orderable:false,
                render:function(data,type,row){
                    
                    var buttons = '<button type="button" onclick="openDeleteModal(\'/erp/product/delete/' + row.id + '/\')" class="btn btn-danger btn-xs"><i class="fas fa-trash"></i></button> ';
                    buttons += '<button type="button" class="btn btn-warning btn-xs" onclick="openEditModal(\'/erp/product/update/' + row.id + '/\')"><i class="fas fa-edit"></i></button>';
                    return buttons;
                }
            },
            {
                targets: [3],
                class:'text-center',
                orderable:false,
                render:function(data,type,row){
                    if(data > 0){
                        return '<span class="badge badge-success">'+ data +'</span>'
                    }
                    return '<span class="badge badge-danger">'+ data +'</span>'
                }
            },
        ],
        initComplete: function(settings,json){

        }
    });
};