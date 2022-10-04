import { useState } from "react";

function MessageManager() {
  const [messages, setMessages] = useState([]);

  function addMessage(msg, msgType) {
    setMessages((messages) => [
      ...messages,
      { message: msg, messageType: msgType },
    ]);
  }

  function removeMessage(messageIndex) {
    setMessages((messages) =>
      messages.filter((msg, index) => {
        return index !== messageIndex;
      })
    );
  }

  return {
    addMessage,
    messages,
    removeMessage,
  };
}

export default MessageManager;
