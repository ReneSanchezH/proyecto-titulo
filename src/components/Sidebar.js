"use client";
import { ArrowRightStartOnRectangleIcon } from "@heroicons/react/24/outline";

import NewChat from "./NewChat";
import { useSession, signOut } from "next-auth/react";

function Sidebar() {
  const { data: session } = useSession();

  return (
    <div className="p-2 flex flex-col h-screen">
      <div className="flex-1 ">
        <div>
          {/* New Chat */}
          <NewChat />
          {/* Map through the ChatRows */}
        </div>
      </div>

      <div className="p-4">
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
