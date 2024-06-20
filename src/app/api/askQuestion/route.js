// This file is the route for the askQuestion API. It is called when the user sends a message in the chat. The message is sent to the chat and then to the API. The API sends the message to the gemini model for processing. The API then sends the response back to the chat. The API is a POST request that takes in the prompt, chatId, model, and session as parameters. The prompt is the message that the user sent in the chat. The chatId is the ID of the chat. The model is the gemini model that the API will use to process the message. The API sends a success message back to the chat when the message is successfully sent to the gemini model.

import { adminDb } from "@/utils/firebaseAdmin";
import query from "@/utils/gemini";
import admin from 'firebase-admin'

export async function handler(req) {
    const { prompt, chatId, model, session } = await req.json();
    if (!prompt || !chatId) {
        return new Response(JSON.stringify({ message: "Bad request" }), { status: 400 });
    }
    console.log("ejecutando handler askQuestion... ");
    // API call
    const response = await query(prompt);

    const message = {
        text: response || "Error in processing the message",
        createdAt: admin.firestore.Timestamp.now(),
        user: {
            _id: "Gemini",
            name: "Gemini",
            avatar: "https://ui-avatars.com/api/?name=Gpt",
        },
    };

    // Save the response to the chat
    await adminDb.collection('users').doc(session?.user?.email).collection('chats').doc(chatId).collection('messages').add(message);

    return new Response(JSON.stringify({ answer: message.text }), { status: 200 });
}

export { handler as GET, handler as POST };
