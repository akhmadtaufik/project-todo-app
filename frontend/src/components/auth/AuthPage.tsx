"use client";

import { motion, AnimatePresence } from "framer-motion";
import { useState, useEffect } from "react";
import LoginForm from "./LoginForm";
import RegisterForm from "./RegisterForm";
import dynamic from "next/dynamic";
import { Rocket } from "lucide-react";

// Lottie is client-side only
const Lottie = dynamic(() => import("lottie-react"), { ssr: false });

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [greeting, setGreeting] = useState("Good Morning");
  const [animationData, setAnimationData] = useState<any>(null);

  useEffect(() => {
    // Dynamic Greeting
    const hour = new Date().getHours();
    if (hour >= 5 && hour < 12) setGreeting("Good Morning");
    else if (hour >= 12 && hour < 18) setGreeting("Good Afternoon");
    else setGreeting("Evening Grind?");

    // use local fallback or icon only to prevent CORS/XML errors from external fetches
    // effectively skipping the fetch for reliability
  }, []);

  const toggleAuth = () => setIsLogin(!isLogin);

  const springTransition = { type: "spring" as const, stiffness: 100, damping: 20 };

  return (
    <div className="relative flex items-center justify-center min-h-screen p-4 overflow-hidden bg-slate-50 text-slate-900 selection:bg-blue-100">
      
      {/* --- KINETIC AMBIENT BACKGROUND --- */}
      
      {/* 1. Grid Pattern */}
      <div className="absolute inset-0 z-0 h-full w-full bg-[radial-gradient(#cbd5e1_1px,transparent_1px)] [background-size:32px_32px] opacity-40"></div>

      {/* 2. Aurora Orbs */}
      <motion.div
        animate={{ 
            x: [0, 50, 0],
            y: [0, -50, 0],
            scale: [1, 1.1, 1] 
        }}
        transition={{ duration: 15, repeat: Infinity, ease: "easeInOut" }}
        className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-blue-400/30 rounded-full blur-[100px] z-0"
      />

      <motion.div
        animate={{ 
            x: [0, -50, 0],
            y: [0, 50, 0],
            scale: [1, 1.2, 1] 
        }}
        transition={{ duration: 18, repeat: Infinity, ease: "easeInOut", delay: 2 }}
        className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-indigo-300/30 rounded-full blur-[100px] z-0"
      />

       {/* --- MAIN AUTH CARD --- */}
      <div className="relative w-full max-w-[1000px] h-[600px] bg-white/90 backdrop-blur-sm rounded-2xl shadow-2xl overflow-hidden flex ring-1 ring-slate-200/50 z-10 items-stretch">
        
        {/* LOGIN FORM CONTAINER (LEFT) */}
        <div className="absolute top-0 left-0 w-1/2 h-full flex items-center justify-center z-20">
            <div className={isLogin ? "w-full h-full" : "w-full h-full pointer-events-none opacity-0 transition-opacity duration-300 transform scale-95"}>
               <LoginForm />
            </div>
        </div>

        {/* REGISTER FORM CONTAINER (RIGHT) */}
        <div className="absolute top-0 right-0 w-1/2 h-full flex items-center justify-center z-20">
            <div className={!isLogin ? "w-full h-full" : "w-full h-full pointer-events-none opacity-0 transition-opacity duration-300 transform scale-95"}>
               <RegisterForm />
            </div>
        </div>

        {/* OVERLAY PANEL (The Sliding Cover) */}
        <motion.div
           className="absolute top-0 w-1/2 h-full bg-gradient-to-br from-blue-600 to-indigo-700 text-white z-40 flex flex-col items-center justify-center p-12 text-center"
           initial={{ left: "50%" }} 
           animate={{ left: isLogin ? "50%" : "0%" }} 
           transition={springTransition}
        >
           <motion.div 
             key={isLogin ? "login-text" : "register-text"}
             initial={{ opacity: 0, y: 10 }}
             animate={{ opacity: 1, y: 0 }}
             transition={{ delay: 0.2 }}
             className="space-y-6 max-w-xs flex flex-col items-center"
           >
              <h2 className="text-3xl font-bold tracking-tight">
                {isLogin ? "New here?" : "One of us?"}
              </h2>
              <p className="text-blue-100 font-medium leading-relaxed">
                  {isLogin 
                    ? `${greeting}! Enter your details and start your journey with us.` 
                    : "To keep connected with us please login with your personal info."}
              </p>
              
              <button 
                  onClick={toggleAuth}
                  className="mt-6 border-2 border-white/80 rounded-full px-8 py-3 font-semibold hover:bg-white hover:text-blue-600 transition-colors uppercase tracking-wider text-sm shadow-lg shadow-blue-900/20 backdrop-blur-sm"
              >
                  {isLogin ? "Sign Up" : "Sign In"}
              </button>

              {/* Lottie Container */}
              <div className="w-64 h-64 mt-6 flex items-center justify-center relative">
                 {animationData ? (
                   <Lottie animationData={animationData} loop={true} className="w-full h-full drop-shadow-lg" />
                 ) : (
                   <div className="flex flex-col items-center justify-center space-y-2 opacity-70 animate-pulse">
                      <Rocket className="w-24 h-24 text-white/50" strokeWidth={1} />
                   </div>
                 )}
              </div>
           </motion.div>
        </motion.div>

      </div>
    </div>
  );
}
