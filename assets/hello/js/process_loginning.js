if (window.location.hash === "#login") {
  $( "#login-modal" ).modal( "show" );
}

function processLoginning() {
  var $loginForm = $( "#login-form" );

  $loginForm.submit(function(event) {
    event.preventDefault();

    $.post( "/login/", data=$loginForm.serialize(), function( data ) {
      if ( data.indexOf("enter a correct username" ) >= 0) {
        var $loginModalBody = $( ".modal-body", "#login-modal" );
        if ( !$( ".alert-danger", $loginModalBody ).length ) {
          $loginModalBody.prepend(
            $( "<div>" ).attr( "class", "alert alert-danger" )
              .text( "Please enter the correct username and password" )
          );
        }
        $( "[name='password']", $loginForm ).val("");
      }
      else
        window.location.reload();
    });
  });
}

processLoginning();
