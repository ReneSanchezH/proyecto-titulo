'use client';

import { db } from "@/utils/firebase";
import { ArrowUpIcon } from "@heroicons/react/24/solid";
import { addDoc, collection, serverTimestamp } from "firebase/firestore";
import { useSession } from "next-auth/react";
import { useState, FormEvent } from "react";
import toast from "react-hot-toast";

// box to write a new message in the chat
function ChatInput({ chatId }) {
  const { data: session } = useSession();
  const [prompt, setPrompt] = useState("");
  const model = "gpt-3";

  const sendMessage = async (e) => {
    // e : FormEvent<HTMLFormElement>
    console.log("sending message...")
    console.log("prompt: ", prompt)


    e.preventDefault();
    if (!prompt) return;

    


    // send the message to the chat
    const input = prompt.trim();
    setPrompt("");
    const message = {
      text: input,
      createdAt: serverTimestamp(),
      user: {
        _id: session?.user?.email,
        name: session?.user?.name,
        avatar:
          session.user.image ||
          `https://ui-avatars.com/api/?name=${session.user.name}`,
      },
    };

    await addDoc(
      collection(
        db,
        "users",
        session?.user?.email,
        "chats",
        chatId,
        "messages"
      ),
      message
    );

    const notification = toast.loading("Loading...");

    await fetch("api/askQuestion", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        prompt: input,
        chatId,
        model,
        session,
      }),
    }).then(() => {
      toast.success("success", { id: notification });
    });
  };

  return (
    <div className="bg-[#2e2e2e] text-white rounded-md text-sm">
      <form onSubmit={sendMessage} className="p-5 space-x-5 flex">
        <input
          className="flex-1 bg-transparent focus:outline-none disabled:cursor-not-allowed disabled:text-gray-300"
          disabled={!session}
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          type="text"
          placeholder="Write a message..."
        />

        <button
          disabled={!session || !prompt}
         
          type="submit"
          className={`relative flex items-center justify-center w-8 h-8 ${
            prompt ? "bg-white" : "bg-[#666666]"
          } rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500
          disabled:cursor-not-allowed hover:opacity-50 `}
        >
          <ArrowUpIcon
            className={`w-6 h-6 ${
              prompt ? "text-black" : "text-[#2e2e2e]"
            } stroke-current stroke-1`}
          />
        </button>
      </form>
      <div>{/*Model selection*/}</div>
    </div>
  );
}

export default ChatInput;
