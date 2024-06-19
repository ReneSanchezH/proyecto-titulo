import Sidebar from "@/components/Sidebar";
import "./globals.css";
import { SessionProvider } from "./contexts/sessionProvider";
import { getServerSession } from "next-auth";
import { GET } from "./api/auth/[...nextauth]/route";
import Login from "@/components/Login";
import ClientProvider from "@/components/ClientProvider";

export const metadata = {
  title: "Sorting Algorithms",
  description: "A visual representation of sorting algorithms",
};

// Root layout for the application
// Sidebar and children are displayed if the user is logged in
// Otherwise, the login page is displayed

export default async function RootLayout({ children }) {
  const session = await getServerSession(GET);
  return (
    <html lang="es">
      <body>
        <SessionProvider session={session}>
          {session ? (
            <div className="flex">
              <div className="bg-[#171717] max-w-xs h-screen overflow-y-auto md:min-w-[12rem]">
                <Sidebar />
              </div>
              <ClientProvider />
              <div className="bg-[#212121] flex-1">{children}</div>
            </div>
          ) : (
            <Login />
          )}
        </SessionProvider>
      </body>
    </html>
  );
}
