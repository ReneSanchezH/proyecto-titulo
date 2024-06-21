"use client";

import { db } from "@/utils/firebase";
import { collection, orderBy, query } from "firebase/firestore";
import { useSession } from "next-auth/react";
import { useCollection } from "react-firebase-hooks/firestore";
import Message from "./Message";

// messages in the selected chat
function Chat({ chatId }) {
  const { data: session } = useSession();

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

  return (
    <div className="flex-1">
      {messages?.docs.map((doc) => (
        <Message key={doc.id} message={doc.data()} />
      ))}
    </div>
  );
}

export default Chat;
