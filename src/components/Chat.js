"use client";
// src/components/Chat.js

import { db } from "@/utils/firebase";
import { collection, orderBy, query } from "firebase/firestore";
import { useSession } from "next-auth/react";
import { useCollection } from "react-firebase-hooks/firestore";
import Message from "./Message";
import Image from "next/image";
import { useEffect, useRef } from "react";

// retrieve messages from the database and display them in the chat
function Chat({ chatId }) {
  const { data: session } = useSession();
  const endOfMessagesRef = useRef(null);

  const [messages, loading, error] = useCollection(
    session &&
      query(
        collection(
          db,
          "users",
          session?.user?.email,
          "chats",
          chatId,
          "messages"
        ),
        orderBy("createdAt", "asc")
      )
  );

  const noMessages = !messages || messages.empty;

  useEffect(() => {
    if (endOfMessagesRef.current) {
      endOfMessagesRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto overflow-x-hidden h-full">
      {" "}
      {/* h-full to ensure it takes full height */}
      {noMessages && (
        <div className="flex items-start justify-center h-full">
          <Image src="/logo.png" alt="Logo" width={80} height={80} />
        </div>
      )}
      {messages?.docs.map((doc) => (
        <Message key={doc.id} message={doc.data()} />
      ))}
      <div ref={endOfMessagesRef} /> {/* Marker for the end of messages */}
    </div>
  );
}

export default Chat;
