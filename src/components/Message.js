// a single message inside the chat
function Message(message) {
  const isUser = !(message?.message?.user?.name === "LLM API");
  return (
    <div
      className={`py-5 text-white 
    ${isUser ? "bg-[#2e2e2e]" : ""}`}
    >
      <div className="flex space-x-5 px-10 max-w-2xl mx-auto">
        <img
          src={message.message?.user?.avatar}
          alt={message.message?.user?.name}
          className="h-8 w-8"
        />
        <p className="pt-1 text-sm">{message.message.text}</p>
      </div>
    </div>
  );
}

export default Message;
