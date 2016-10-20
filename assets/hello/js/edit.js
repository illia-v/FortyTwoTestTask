// Settings of `datepicker`
$(function () {
  $( "#datepicker" ).datepicker({
    format: "yyyy-mm-dd",
    endDate: "+0d",
    autoclose: true
  });
});


var encodedPhoto;
// Showing a photo preview
function showPhotoPreview(input) {
  if (input.files && input.files[0]) {
      var reader = new FileReader();
      var $photoPreview = $( "#photo-preview" );

      $( reader ).on( "load", function(event) {
        $( "#photo-preview" ).attr( "src", event.target.result );
        $photoPreview.parent( "div" ).show();
        encodedPhoto = event.target.result.replace(/data:image\/.+;base64,/,
                                                   '');
      });

      reader.readAsDataURL(input.files[0]);
  }
}

$( "#photo-input" ).change(function() {
  showPhotoPreview( this );
});


$( "#edit-form" ).submit(function(event) {
  event.preventDefault();

  // Indicating loading state
  var $submitButton = $( "#form-submit-btn" );
  $submitButton.button( "loading" );

  var $formFields = $( "input, textarea",  $( this ) );

  $.ajax({
    url: window.location.href,
    type: "POST",
    dataType: "json",
    data: JSON.stringify({form_data: $( this ).serialize(),
                          encoded_photo: encodedPhoto}),
    beforeSend: function(xhr) {
                  xhr.setRequestHeader("X-CSRFToken", $.cookie( "csrftoken" ));
                  $formFields.attr( "disabled", "" );
                }
  })
  .done(function() {
    var $successAlert = $( "<div class='alert alert-success'>" ).html(
      $( "<b>" ).text( "Your data is edited successfully" )
    );

    $( "main" ).prepend( $successAlert );
    setTimeout( function() {
      $successAlert.remove();
    }, 10000 );
  })
  .fail(function() {
    var $dangerAlert = $( "<div class='alert alert-danger'>" ).html(
      $( "<b>" ).text( "There are some errors. Try again" )
    );

    $( "main" ).prepend( $dangerAlert );
    setTimeout( function() {
      $dangerAlert.remove();
    }, 10000 );
  })
  .always(function() {
    $formFields.removeAttr( "disabled" );
    $submitButton.button( "reset" );
    window.scrollTo(0, 0);
  });
});
