// Import the functions you need from the SDKs you need
import { initializeApp, getApps, getApp } from 'firebase/app';
import { getStorage } from 'firebase/storage';
import { getFirestore } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyA8g3WsotiCGR4fN1J54YiKLfLmEQHCtEg",
    authDomain: "lasalle-2f485.firebaseapp.com",
    projectId: "lasalle-2f485",
    storageBucket: "lasalle-2f485.appspot.com",
    messagingSenderId: "592680294736",
    appId: "1:592680294736:web:5c65bf3071d0cac3dbb455",
    measurementId: "G-S5L48D1BYN"
};

// Initialize Firebase
const app = !getApps().length ? initializeApp(firebaseConfig) : getApp();
const storage = getStorage();
const db = getFirestore();
const auth = getAuth();

export {app,db,storage,auth}



