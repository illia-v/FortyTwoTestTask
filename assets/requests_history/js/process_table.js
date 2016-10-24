var requestsDataTable = $( "#requests-table" ).DataTable({
  aoColumns: [
    null,
    { bSortable: false },
    { bSortable: false },
    { bSortable: false },
    null
  ],
  bFilter: false,
  bInfo: false,
  bPaginate: false,
  order: [[0, "desc"]],
  columns: [
    { data: "id" },
    { data: "timestamp" },
    { data: "url" },
    { data: "method" },
    { data: "priority" }
  ]
});
