import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

const query = async (prompt) => {

  const res = await openai.chat.completions
    .create({
      messages: [{ role: "user", content: prompt }],
      model: "gpt-3.5-turbo",
      temperature: 1,
      max_tokens: 256,
      top_p: 1,
      frequency_penalty: 0,
      presence_penalty: 0,
      stream: true,
    })
    .then((res) => res.data.choices[0].text)
    .catch((err) => {
      console.log("Error in query function");
      console.error(err);
    });
  return res;
};

export default query;
