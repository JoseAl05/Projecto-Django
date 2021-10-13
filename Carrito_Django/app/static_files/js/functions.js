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