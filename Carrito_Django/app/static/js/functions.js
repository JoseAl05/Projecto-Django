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