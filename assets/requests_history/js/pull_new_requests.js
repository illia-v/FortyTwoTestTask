localStorage.lastSeenRequestId = Number($( "#requests-table tr" ).eq(1)
                                         .data( "request-id" ));
var lastRequestId = localStorage.lastSeenRequestId;

function pullNewRequests() {
  // Pulls new requests to a page
  var $requestsTable = $( "#requests-list " );

  $.getJSON(requestsPullingPageURL, {"last_request_id": lastRequestId},
    function(newRequests) {
      for (var i=0; i<newRequests.length; i++) {
        var newRequest = newRequests[i];

        $requestsTable.prepend(
          $( "<li>" )
          .html("A URL <a href='" + newRequest.url + "'>" + newRequest.url +
                "</a> was requested with method " +
                newRequest.method + " at " + newRequest.timestamp)
          .data( "request-id", newRequest.id )
          .addClass( "list-group-item" )
        );
      }

      // Adding an amount of new requests, added to a page when a user was
      // out, to a title of a document
      if (newRequests.length > 0) {
        lastRequestId = Number(newRequests.pop().id);
      }
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
