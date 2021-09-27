$(function(){
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
            {'data':'pvp'},
            {'data':'pvp'},
        ],
        columnDefs:[
            {
                targets: [4],
                class:'text-center',
                orderable:false,
                render:function(data,type,row){
                    
                    var buttons = '<button type="button" onclick="openDeleteModal(\'/erp/product/delete/' + row.id + '/\')" class="btn btn-danger"><i class="fas fa-trash"></i></button> ';
                    buttons += '<button type="button" class="btn btn-warning" onclick="openEditModal(\'/erp/product/update/' + row.id + '/\')"><i class="fas fa-edit"></i></button>';
                    return buttons;
                }
            },
        ],
        initComplete: function(settings,json){

        }
    });
});