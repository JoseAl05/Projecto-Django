var date_range = null;
var date_now = new moment().format('YYYY-MM-DD');


function generate_report(){
    var parameters = {
        'action' : 'search_report',
        'start_date':date_now,
        'end_date':date_now
    };

    if(date_range !== null){
        parameters['start_date'] = date_range.startDate.format('YYYY-MM-DD');
        parameters['end_date'] = date_range.endDate.format('YYYY-MM-DD')
    }


    $('#data').DataTable({
        responsive:true,
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
            url:window.location.pathname,
            type:'POST',
            data: parameters,
            dataSrc:'',
        },
        order:false,
        paging:false,
        ordering:false,
        info:false,
        searching:false,
        dom: 'Bfrtip',
        buttons:[
            {
                extend: 'excelHtml5',
                text: 'Download Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs'
            },
            {
                extend: 'pdfHtml5',
                text: 'Download Pdf <i class="fas fa-file-pdf"></i>',
                titleAttr: 'PDF',
                className: 'btn btn-danger btn-flat btn-xs',
                download: 'open',
                orientation: 'landscape',
                pageSize: 'LEGAL',
                customize: function (doc) {
                    doc.styles = {
                        header: {
                            fontSize: 18,
                            bold: true,
                            alignment: 'center'
                        },
                        subheader: {
                            fontSize: 13,
                            bold: true
                        },
                        quote: {
                            italics: true
                        },
                        small: {
                            fontSize: 8
                        },
                        tableHeader: {
                            bold: true,
                            fontSize: 11,
                            color: 'white',
                            fillColor: '#2d4154',
                            alignment: 'center'
                        }
                    };
                    doc.content[1].table.widths = ['20%','20%','15%','15%','15%','15%'];
                    doc.content[1].margin = [0, 35, 0, 0];
                    doc.content[1].layout = {};
                    doc['footer'] = (function (page, pages) {
                        return {
                            columns: [
                                {
                                    alignment: 'left',
                                    text: ['Fecha de creación: ', {text: date_now}]
                                },
                                {
                                    alignment: 'right',
                                    text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                }
                            ],
                            margin: 20
                        }
                    });

                }
            }
        ],
        // columns:[
        //     {'data':'id'},
        //     {'data':'cli.names'},
        //     {'data':'date_joined'},
        //     {'data':'subtotal'},
        //     {'data':'iva'},
        //     {'data':'total'},
        //     {'data':'total'},
        // ],
        columnDefs:[
            {
                targets: [3,4,5],
                class:'text-center',
                orderable:false,
                render:function(data,type,row){
                    return '$'+parseFloat(data).toFixed(2)
                }
            },
        ],
        initComplete: function(settings,json){

        }
    });
}

$(function(){
    $('input[name="date_range"]').daterangepicker({
        locale:{
            format:'YYYY-MM-DD'
        }
    }).on('apply.daterangepicker',function(ev,picker){
        date_range = picker;
        generate_report();

    }).on('cancel.daterangepicker',function(ev,picker){
        $(this).data('daterangepicker').setStartDate(date_now);
        $(this).data('daterangepicker').setEndDate(date_now);
        date_range = picker;
        generate_report();
    })
    generate_report();
});