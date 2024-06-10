import Sidebar from "@/components/Sidebar";
import "./globals.css";

export const metadata = {
  title: "Sorting Algorithms",
  description: "A visual representation of sorting algorithms",
};

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <div className="flex">
          {/* Sidebar */}
          <div className="bg-[#202123] max-w-xs h-screen overflow-y-auto md:min-w-[12rem]">
            <Sidebar />
          </div>
          {/* ClientProvider - Notification */}

          <div className="bg-[#343541] flex-1">{children}</div>
        </div>
      </body>
    </html>
  );
}
