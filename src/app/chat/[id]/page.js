'use client';
import Chat from "@/components/Chat";
import ChatInput from "@/components/ChatInput";
import React from "react";

// List all the messages in the selected chat
// Box to write a new message

/**id of the chat
 * @param {string} params.id
 */
function ChatPage({ params: { id } }) {
  return (
    <div className="flex flex-col h-screen overflow-hidden p-4">
      <div className="flex flex-col flex-grow rounded-md p-4 h-full"> {/* h-full ensures full height */}
        <Chat chatId={id} />
        <ChatInput chatId={id} />
      </div>
    </div>
  );
}

export default ChatPage;
