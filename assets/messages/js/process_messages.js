$( "#new-msg-form" ).submit(function(event) {
  event.preventDefault();

  var message = $( "#msg-input" ).val();
  var $conversationArea = $( "#conversation-area" );

  $conversationArea.append(
    $( "<div class='msg sent-msg'>" )
    .append( "<b class='sender'>You</b> " )
    .append( "<i>at Nov. 8, 2016, 8:00 p.m.</i>" )
    .append( "<hr>" )
    .append( $( "<p>" ).text( message ) )
  );

  prepareConversationArea();
  $( this ).trigger( "reset" );

  setTimeout( addAnswerToConversationArea, 1500, message );
});


function addAnswerToConversationArea(message) {
  var $conversationArea = $( "#conversation-area" );

  $conversationArea.append(
    $( "<div class='msg received-msg'>" )
    .append( "<b class='sender'>Somebody</b> " )
    .append( "<i>at Nov. 8, 2016, 8:00 p.m.</i>" )
    .append( "<hr>" )
    .append( $( "<p>" ).text( "I am answering on your message: " + message) )
  );

  prepareConversationArea();
}
