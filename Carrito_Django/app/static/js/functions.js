function message_error(obj){
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

function openEditModal(url){

    $('#editModal').load(url,function(){
        $(this).modal('show');
    });
};

function openDeleteModal(url){
    $('#deleteModal').load(url,function(){
        $(this).modal('show');
    });
};

function openCreateModal(url){
    $('#createModal').load(url,function(){
        $(this).modal('show');
    });
};


