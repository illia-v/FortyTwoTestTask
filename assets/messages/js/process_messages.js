var lastMessageId;

function setLastMessageId() {
  var $messages = $( ".msg" );
  if ( $messages.length ) {
    lastMessageId = Number($messages.last().data( "msg-id" ));
  } else {
    console.log(1);
    lastMessageId = 0;
  }
}
setLastMessageId();


function pullNewMessages() {
  // Pulls new messages to a conversation
  $.getJSON(messagingPullPageURL, {"last_message_id": lastMessageId},
    function (newMessages) {
      for (var i=0; i<newMessages.length; i++) {
        newMessage = newMessages[i];

        if ( newMessage.sender == "You" ) {
          $messageDiv = $( "<div class='msg sent-msg'>" );
        } else {
          $messageDiv = $( "<div class='msg received-msg'>" );
        }

        $conversationArea.append(
          $messageDiv
          .append( $( "<b class='sender'>" ).text( newMessage.sender ) )
          .append( $( "<i>" ).text( " at " + newMessage.timestamp ) )
          .append( "<hr>" )
          .append( $( "<p>" ).text( newMessage.body ) )
        );
        prepareConversationArea();

        lastMessageId = newMessage.id;
      }
  });

  setTimeout( pullNewMessages, 500 );
}

pullNewMessages();


$( "#new-msg-form" ).submit(function(event) {
  event.preventDefault();
  var message = $( "#msg-input" ).val();

  $.ajax({
    url: messagingCreatePageURL,
    type: "POST",
    dataType: "json",
    data: $( this ).serialize(),
    beforeSend: function(xhr) {
                  xhr.setRequestHeader("X-CSRFToken", $.cookie( "csrftoken" ));
                }
  })
  .done(function () {
    $( "#new-msg-form" ).trigger( "reset" );
  })
  .fail(function () {
    $( "#new-msg-form" ).prepend( $( "<div class='alert alert-danger'>" ).html(
        $( "<b>" ).text( "There was an error sending your message" )
    ))
  });
});


function resetUnreadCount() {
  $( document ).one("mouseover", function() {
    $.post(
      location.pathname+'reset_unread_count', {'last_message_id': lastMessageId}
    );
  });

  setTimeout(resetUnreadCount, 3000);
}

resetUnreadCount();
