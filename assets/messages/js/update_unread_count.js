function updateUnreadMessagesCount() {
  var $allConversations = $( ".conversation" );

  for (var $conversation of $allConversations) {
    $badgeWithUnreadMessagesCount = $( ".badge", $conversation );

    if ( $badgeWithUnreadMessagesCount.length ) {
      $badgeWithUnreadMessagesCount.text(
        Math.floor(Math.random() * (100 - 1 + 1) + 1)
      );
    } else {
      $( "<span class='badge'>" )
      .text( Math.floor(Math.random() * (100 - 1 + 1) + 1) )
      .appendTo( $conversation )
    }
  }

  setTimeout(updateUnreadMessagesCount, 5000);
}

updateUnreadMessagesCount();
