'use client';
import { Toaster } from "react-hot-toast";

// main component for the client side of the application
function ClientProvider() {
  return (
    <>
      <Toaster position="top-right" />
    </>
  );
}

export default ClientProvider;
