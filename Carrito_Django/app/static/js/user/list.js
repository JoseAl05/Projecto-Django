function getUserData(){
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
            {'data':'full_name'},
            {'data':'username'},
            {'data':'date_joined'},
            {'data':'groups'},
            {'data':'id'},
        ],
        columnDefs:[
            {
                targets: [5],
                class:'text-center',
                orderable:false,
                render:function(data,type,row){
                    var buttons = '<button type="button" class="btn btn-danger btn-xs" onclick="openDeleteModal(\'/users/delete/' + row.id + '/\')"><i class="fas fa-trash"></i></button> ';
                    buttons += '<button type="button" class="btn btn-warning btn-xs" onclick="openEditModal(\'/users/update/' + row.id + '/\')"><i class="fas fa-edit"></i></button>';
                    return buttons;
                }
            },
            {
                targets: [4],
                class:'text-center',
                orderable:false,
                render:function(data,type,row){
                    var html = '';
                    $.each(row.groups,function(key,value){
                        if(value.name == 'Administrador'){
                            html += '<span class="badge badge-warning">'+ value.name +'</span> ';
                        }else{
                            html += '<span class="badge badge-success">'+ value.name +'</span> ';
                        }
                    })
                    return html;
                }
            },
        ],
        initComplete: function(settings,json){

        }
    });
};