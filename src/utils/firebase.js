import { getApp, getApps, initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

// web app's Firebase configuration
const firebaseConfig = {
    apiKey: process.env.FIREBASE_API_KEY,
    authDomain: "app-sorting-be0fa.firebaseapp.com",
    projectId: "app-sorting-be0fa",
    storageBucket: "app-sorting-be0fa.appspot.com",
    messagingSenderId: "390966987793",
    appId: "1:390966987793:web:459621d3936c3bcff9f5b0"
  };

// Initialize Firebase
const app = getApps().length ? getApp() : initializeApp(firebaseConfig);
const db = getFirestore(app);

export { db };
