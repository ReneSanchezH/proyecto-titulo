const {
  GoogleGenerativeAI,
  HarmCategory,
  HarmBlockThreshold,
} = require("@google/generative-ai");

const apiKey = process.env.GEMINI_API_KEY;
const genAI = new GoogleGenerativeAI(apiKey);

const model = genAI.getGenerativeModel({
  model: "gemini-1.5-flash",
});

const generationConfig = {
  temperature: 0.7, // Ajuste la temperatura para mayor precisión
  topP: 0.95,
  topK: 64,
  maxOutputTokens: 200, // Reducir el número máximo de tokens
  responseMimeType: "text/plain",
};

async function query(prompt) {
  const chatSession = model.startChat({
    generationConfig,
    history: [],
  });
  console.log("gemini query...");
  console.log("prompt: ", prompt);
  
  // Incluir instrucciones en el prompt para respuestas cortas y precisas
  const modifiedPrompt = `Por favor, responde de manera breve y precisa: ${prompt}.`;

  const result = await chatSession.sendMessage(modifiedPrompt);
  return result.response.text();
}

module.exports = query;
