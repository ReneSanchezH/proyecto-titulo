// a single message inside the chat
function Message({ message }) {
  const isUser = !(message?.user?.name === "LLM API");
  return (
    <div
      className={`py-5 text-white ${isUser ? "bg-[#2e2e2e]" : "bg-[#3e3e3e]"}`}
    >
      <div className="flex flex-col space-y-2 px-10 max-w-2xl mx-auto">
        <div className="flex space-x-5">
          <img
            src={message?.user?.avatar}
            alt={message?.user?.name}
            className="h-8 w-8"
          />
          <p className="pt-1 text-sm">{message.text}</p>
        </div>
        {!isUser && message.videoUrl && (
          <div className="flex justify-center mt-4">
            <video width="600" controls>
              <source src={`http://127.0.0.1:5000${message.videoUrl}`} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>
        )}
      </div>
    </div>
  );
}

export default Message;
