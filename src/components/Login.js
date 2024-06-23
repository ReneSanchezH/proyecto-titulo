"use client";
import { signIn } from "next-auth/react";
import Image from "next/image";

// login page
function Login() {
  return (
    <div className="bg-[#212121] h-screen flex flex-col items-center justify-center text-center">
      <h1 className="text-white font-bold text-3xl mb-4">
        Sorting algorithms app
      </h1>
      <div className="flex flex-col items-center">
        <Image src="/logo.png" alt="Login Image" width={100} height={100} />
        <div className="mt-4">
          {"  "}
          <button
            className="text-white font-bold text-3xl animate-pulse"
            onClick={() => signIn("google")}
          >
            Sign in
          </button>
        </div>
      </div>
    </div>
  );
}

export default Login;
