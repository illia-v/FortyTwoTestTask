localStorage.lastSeenRequestId = Number($( "#requests-table tr" ).eq(1)
                                         .data( "request-id" ));
var lastRequestId = localStorage.lastSeenRequestId;

function pullNewRequests() {
  // Pulls new requests to a page
  $.getJSON(requestsPullingPageURL, {"last_request_id": lastRequestId},
    function(newRequests) {
      for (var i=0; i<newRequests.length; i++) {
        var newRequest = newRequests[i];
        var $requestTable = $( "#requests-table" );

        var $newRow = $( "<tr>" ).data( "request-id", newRequest.id )
          .append($( "<td>" ).text( newRequest.id ))
          .append($( "<td>" ).text( newRequest.timestamp ))
          .append($( "<td>" ).html(
            $( "<a>" ).attr( "href", newRequest.url ).text( newRequest.url )
          ))
          .append($( "<td>" ).text( newRequest.method ))
          .append($( "<td>" ).text( 1 ));

        requestsDataTable.row.add($newRow)
        .row(
          $( "tr[data-request-id=" + String(lastRequestId-9) + "]" )
        ).remove().draw();

        lastRequestId = newRequest.id;
    }
    // Adding an amount of new requests, added to a page when a user was
    // out, to a title of a document
    var notSeenRequestsNumber = lastRequestId-localStorage.lastSeenRequestId;
    document.title = (notSeenRequestsNumber > 0 ?
                      "(" + notSeenRequestsNumber + ") " : "") +
                      "Requsts History";
    clearDocumentTitleOnAction();
  });

  setTimeout( pullNewRequests, 1000 );
}

pullNewRequests();


function clearDocumentTitleOnAction() {
  // Changes a title of a document to 'Requsts History' when a user's mouse is
  // over the document
  $( document ).one("mouseover", function(event) {
    document.title = "Requsts History";
    localStorage.lastSeenRequestId = lastRequestId;
  });
}
