function prepareConversationArea() {
  $conversationArea = $( "#conversation-area" );
  $conversationAreaHeight = Math.max(
    $( window ).height() - $( "body" ).height() + $conversationArea.height(),
    300
  );

  $( "#conversation-area" ).css({
    "height": $conversationAreaHeight, "max-height": $conversationAreaHeight
  }).scrollTop( $conversationArea[0].scrollHeight );
}

prepareConversationArea();

$( window ).resize(function(event) {
  prepareConversationArea()
});
