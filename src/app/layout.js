import Sidebar from "@/components/Sidebar";
import "./globals.css";
import { SessionProvider } from "./contexts/sessionProvider";
import { getServerSession } from "next-auth";
import { handler } from "./api/auth/[...nextauth]/route";
import Login from "@/components/Login";

export const metadata = {
  title: "Sorting Algorithms",
  description: "A visual representation of sorting algorithms",
};

export default async function RootLayout({ children }) {
  const session = await getServerSession(handler);
  return (
    <html lang="es">
      <body>
        <SessionProvider session={session}>
          {session ? (
            <div className="flex">
              {/* Sidebar */}
              <div className="bg-[#202123] max-w-xs h-screen overflow-y-auto md:min-w-[12rem]">
                <Sidebar />
              </div>
              {/* ClientProvider - Notification */}
              <div className="bg-[#343541] flex-1">{children}</div>
            </div>
          ) : (
            <Login />
          )}
        </SessionProvider>
      </body>
    </html>
  );
}
