function message_category_error(obj){
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

function message_category_success(){
    Swal.fire({
        icon: 'success',
        title: 'Success',
        text: 'Category saved successfully!',
    }).then(function(result){
        if(result.value){
            location.href = '/erp/category/list';
        }
    })
}

function openEditModal(url){

    $('#editModal').load(url,function(){
        $(this).modal('show');
    });
};

function openDeleteModal(url){
    console.log(url);
    $('#deleteModal').load(url,function(){
        $(this).modal('show');
    });
};

function openCreateModal(url){
    $('#createModal').load(url,function(){
        $(this).modal('show');
    });
};


