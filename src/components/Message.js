function Message(message) {
  return (
    <div>
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
