"use client";

import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { PlusIcon } from "@heroicons/react/24/solid";
import { db } from "../utils/firebase";
import { addDoc, collection, serverTimestamp } from "firebase/firestore";

// Create a new chat
function NewChat() {
  const router = useRouter();
  const { data: session } = useSession();

  const createChat = async () => {
    if (!session?.user?.email) {
      console.error("El email del usuario no está definido");
      return;
    }
    console.log("Creando un nuevo chat...");
    console.log("Usuario:", session.user.email);

    // Users collection: each user (by email) has a subcollection of chats with messages
    try {
      const document = await addDoc(
        collection(db, "users", session?.user?.email, "chats"),
        {
          userId: session?.user?.email,
          createdAt: serverTimestamp(),
        }
      );
      router.push(`/chat/${document.id}`);
    } catch (error) {
      console.error("Error al agregar el chat:", error);
    }
  };

  return (
    <div onClick={createChat} className="border-gray-700 border chatRow">
      <PlusIcon className="h-4 w-4" />
      <p>New Chat</p>
    </div>
  );
}

export default NewChat;
