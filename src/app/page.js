import React from "react";
import Image from "next/image";

function Homepage() {
  return (
    <div className="flex flex-col items-center justify-center h-screen text-white">
      <Image src="/logo.png" alt="Logo" width={80} height={80} />

      <h1 className="text-5xl font-bold mb-20">Sorting algorithms app</h1>
    </div>
  );
}

export default Homepage;
