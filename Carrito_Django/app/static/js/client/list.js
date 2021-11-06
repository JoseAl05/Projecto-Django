function getClientData(){
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
            {'data':'names'},
            {'data':'surnames'},
            {'data':'dni'},
            {'data':'birthday'},
            {'data':'address'},
            {'data':'gender'},
            {'data':'gender'},
        ],
        columnDefs:[
            {
                targets: [7],
                class:'text-center',
                orderable:false,
                render:function(data,type,row){
                    
                    var buttons = '<button type="button" onclick="openDeleteModal(\'/erp/client/delete/' + row.id + '/\')" class="btn btn-danger btn-xs"><i class="fas fa-trash"></i></button> ';
                    buttons += '<button type="button" class="btn btn-warning btn-xs" onclick="openEditModal(\'/erp/client/update/' + row.id + '/\')"><i class="fas fa-edit"></i></button>';
                    return buttons;
                }
            },
        ],
        initComplete: function(settings,json){

        }
    });
};