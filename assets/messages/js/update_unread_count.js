function updateUnreadMessagesCount() {
  $.getJSON(updateUnreadCountURL,
    function (allConversations) {
      for (var conversation of allConversations) {
        var interlocutor = conversation.interlocutor;
        var unreadMessagesCount = conversation['unread_count'];

        var $badgeWithUnreadCount = $( "#unread-count-" + interlocutor );

        if ( $badgeWithUnreadCount.length ) {
          if ( unreadMessagesCount ) {
            $badgeWithUnreadCount.text( unreadMessagesCount );
          } else {
            $badgeWithUnreadCount.remove();
          }
        } else if ( unreadMessagesCount != 0 ) {
          $( "<span class='badge' id='unread-count-" + interlocutor + "'>" )
          .text( unreadMessagesCount ).appendTo(
            $( "#conversation-" + interlocutor )
          );
        }
      }
    }
  );

  setTimeout(updateUnreadMessagesCount, 2000);
}

updateUnreadMessagesCount();
