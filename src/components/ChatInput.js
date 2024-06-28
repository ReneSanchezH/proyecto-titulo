"use client";

import { db } from "@/utils/firebase";
import { ArrowUpIcon } from "@heroicons/react/24/solid";
import {
  addDoc,
  collection,
  serverTimestamp,
  updateDoc,
  doc,
} from "firebase/firestore";
import { useSession } from "next-auth/react";
import { useState, FormEvent } from "react";
import toast from "react-hot-toast";

import NumberInput from "./NumberInput";

function ChatInput({ chatId }) {
  const { data: session } = useSession();
  const [prompt, setPrompt] = useState("");
  const [numbers, setNumbers] = useState("");

  const model = "LLM API";

  const handleInputChange = (value) => {
    setNumbers(value);
    console.log(value);
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!prompt) return;

    const input = prompt.trim();
    setPrompt("");

    const userMessage = {
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

    const notification = toast.loading("Loading...");

    // Guardar el mensaje del usuario
    await addDoc(
      collection(
        db,
        "users",
        session?.user?.email,
        "chats",
        chatId,
        "messages"
      ),
      userMessage
    );

    // Crear el mensaje del LLM con un placeholder
    const llmMessage = {
      text: "Processing...",
      createdAt: serverTimestamp(),
      user: {
        _id: "LLM API",
        name: "LLM API",
        avatar: "https://ui-avatars.com/api/?name=LLM",
      },
      videoUrl: null, // Inicialmente nulo
    };

    const llmMessageRef = await addDoc(
      collection(
        db,
        "users",
        session?.user?.email,
        "chats",
        chatId,
        "messages"
      ),
      llmMessage
    );

    let videoUrl = "";
    if (numbers) {
      videoUrl = await sendNumbers(numbers, notification);
    }

    await fetch("/api/askQuestion", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        prompt: input,
        chatId: chatId,
        model: model,
        session: session,
      }),
    })
      .then(async (res) => {
        const data = await res.json();
        toast.success("LLM success", { id: notification });

        // Actualizar el mensaje del LLM con la respuesta y la URL del video
        await updateDoc(doc(db, "users", session?.user?.email, "chats", chatId, "messages", llmMessageRef.id), {
          text: data.answer,
          videoUrl: videoUrl || null,
        });
      })
      .catch((error) => {
        toast.error("Error", { id: notification });
        console.error("Error:", error);
      });
  };

  const sendNumbers = async (numbers, notification) => {
    console.log("sending message...");
    console.log("numbers: ", numbers);
    if (!numbers) return "";

    return await fetch("http://127.0.0.1:5000/generate-video", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        numbers: numbers.replace(/\s+/g, ""), // Ensure no spaces are included
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        toast.success("Video generated successfully!", { id: notification });
        console.log(data);
        return data.video_url;
      })
      .catch((error) => {
        toast.error("Error generating video", { id: notification });
        console.error("Error:", error);
        return "";
      });
  };

  return (
    <div className="bg-[#2e2e2e] text-white rounded-md text-sm">
      <NumberInput onInputChange={handleInputChange} />
      <hr className="border-gray-600 my-2" />

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
    </div>
  );
}

export default ChatInput;
