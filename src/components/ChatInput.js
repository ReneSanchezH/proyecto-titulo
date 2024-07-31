"use client";

// src/components/ChatInput.js
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
  };

  const getVideoUrlFromPrompt = (prompt) => {
    const lowerCasePrompt = prompt.toLowerCase();
    const detailedKeywords = [
      "detallado",
      "detalles",
      "explicaciones",
      "explicación",
      "analisis",
      "paso a paso",
      "detalladamente",
      "explicación completa",
      "en profundidad",
      "descripción",
      "en detalle",
      "con detalle",
      "explicación exhaustiva",
      "detallada explicación",
      "paso por paso",
      "detallada",
      "completamente",
      "explicaciones detalladas",
      "descripción en detalle",
      "información completa",
      "desglose detallado",
    ];

    const countingSortKeywords = [
      "counting sort",
      "ordenación por conteo",
      "ordenación de conteo",
      "ordenamiento por conteo",
      "ordenamiento de conteo",
      "sort counting",
      "conteo",
      "ordenar por conteo",
      "sort de conteo",
      "sort conteo",
      "explicación counting sort",
      "detalles de counting sort",
      "cómo funciona counting sort",
      "algoritmo counting sort",
      "counting sort paso a paso",
      "ordenar por conteo",
      "sort de conteo",
      "counting sort explicado",
      "counting sort detallado",
      "contar y ordenar",
      "explicación de counting sort",
      "ordenación por contaje",
      "ordenar mediante conteo",
      "sort basado en conteo",
    ];

    const bucketSortKeywords = [
      "bucket sort",
      "ordenación por cubetas",
      "ordenación de cubetas",
      "ordenamiento por cubetas",
      "ordenamiento de cubetas",
      "sort bucket",
      "cubetas",
      "ordenar por cubetas",
      "sort de cubetas",
      "sort cubetas",
      "explicación bucket sort",
      "detalles de bucket sort",
      "cómo funciona bucket sort",
      "algoritmo bucket sort",
      "bucket sort paso a paso",
      "ordenar por cubetas",
      "sort de cubetas",
      "bucket sort explicado",
      "bucket sort detallado",
      "cubetas de ordenamiento",
      "explicación de bucket sort",
      "ordenación mediante cubetas",
      "bucket sort detalladamente",
    ];

    // Verificar si el prompt contiene alguna de las palabras clave de radix sort detallado
    for (const word of detailedKeywords) {
      if (lowerCasePrompt.includes(word)) {
        return "/videos/radix_detailed.mp4";
      }
    }

    // Verificar si el prompt contiene alguna de las palabras clave de counting sort
    for (const word of countingSortKeywords) {
      if (lowerCasePrompt.includes(word)) {
        return "/videos/counting_sort.mp4";
      }
    }

    // Verificar si el prompt contiene alguna de las palabras clave de bucket sort
    for (const word of bucketSortKeywords) {
      if (lowerCasePrompt.includes(word)) {
        return "/videos/bucket.mp4";
      }
    }

    return null;
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!prompt) return;

    const input = prompt.trim();
    setPrompt("");

    const notification = toast.loading("Loading...");

    const userMessage = {
      text: input,
      numbers: numbers.trim(),
      createdAt: serverTimestamp(),
      user: {
        _id: session?.user?.email,
        name: session?.user?.name,
        avatar:
          session.user.image ||
          `https://ui-avatars.com/api/?name=${session.user.name}`,
      },
    };

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

    // Verificar si el prompt contiene una palabra clave para un video estático

    let videoUrl = getVideoUrlFromPrompt(input);
    console.log("videoUrl: ", videoUrl);

    if (!videoUrl && numbers) {
      // Si no se encontró un video estático, generar un video dinámico
      videoUrl = await sendNumbers(numbers, notification);
    }

    const fetchApiAndUpdateMessage = async () => {
      try {
        const res = await fetch("/api/askQuestion", {
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
        });

        const data = await res.json();
        toast.success("LLM success", { id: notification });

        // Actualizar el mensaje del LLM con la respuesta y la URL del video
        await updateDoc(
          doc(
            db,
            "users",
            session?.user?.email,
            "chats",
            chatId,
            "messages",
            llmMessageRef.id
          ),
          {
            text: data.answer,
            videoUrl: videoUrl || null,
          }
        );
      } catch (error) {
        toast.error("Error", { id: notification });
        console.error("Error:", error);
      }
    };

    // Ejecutar la llamada a la API y actualizar el mensaje "Processing..."
    fetchApiAndUpdateMessage();
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
        prompt: prompt,
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
