"use client";

import NewChat from "./NewChat";
import { useSession, signOut } from "next-auth/react";
import { useCollection } from "react-firebase-hooks/firestore";
import { ArrowRightStartOnRectangleIcon, ChevronLeftIcon, ChevronRightIcon } from "@heroicons/react/24/outline";
import { query, collection, orderBy } from "firebase/firestore";
import { db } from "@/utils/firebase";
import ChatRow from "./ChatRow";
import { useState } from "react";

// Sidebar component
function Sidebar() {
  const { data: session } = useSession();
  const [collapsed, setCollapsed] = useState(false);

  const [chats, loading, error] = useCollection(
    session &&
      query(
        collection(db, "users", session?.user?.email, "chats"),
        orderBy("createdAt", "asc")
      )
  );

  return (
    <div className={`flex flex-col h-screen ${collapsed ? 'w-20' : 'w-64'} transition-all duration-300`}>
      <div className="p-2 flex flex-col h-full">
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-2 hover:bg-gray-700 focus:outline-none transition-colors duration-200 ease-out"
          title={collapsed ? "Abrir barra lateral" : "Colapsar barra lateral"}
        >
          {collapsed ? (
            <ChevronRightIcon className="h-6 w-6 text-white" />
          ) : (
            <ChevronLeftIcon className="h-6 w-6 text-white" />
          )}
        </button>
        <div className={`flex-1 overflow-y-auto overflow-x-hidden ${collapsed ? 'hidden' : 'block'}`}>
          <div>
            <NewChat />
            {chats?.docs.map((chat) => (
              <ChatRow key={chat.id} id={chat.id} users={chat.data().users} />
            ))}
          </div>
        </div>
      </div>
      <div className={`p-4 ${collapsed ? 'hidden' : 'block'}`}>
        {session?.user?.image && (
          <div className="flex flex-col items-center space-y-4 mb-4">
            <div className="flex items-center space-x-4">
              <img
                src={session.user.image}
                alt="User profile"
                className="h-8 w-8 rounded-full cursor-pointer hover:scale-110 transition-transform duration-200 ease-out"
              />
              <span className="text-white">{session.user.name}</span>
            </div>
          </div>
        )}
        <div
          className="border border-gray-700 chatRow flex items-center space-x-2 p-2 cursor-pointer hover:bg-gray-700/70 transition-colors duration-200 ease-out"
          onClick={() => signOut()}
        >
          <ArrowRightStartOnRectangleIcon className="h-6 w-6 text-white" />
          <p className="text-white">Logout</p>
        </div>
      </div>
    </div>
  );
}

export default Sidebar;
