"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { motion, AnimatePresence } from "framer-motion";
import { Loader2, Eye, EyeOff, User, Mail, Lock } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import api from "@/lib/axios";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

// Zod Schema
const registerSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

type RegisterSchema = z.infer<typeof registerSchema>;

export default function RegisterForm() {
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const router = useRouter();

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
    setError
  } = useForm<RegisterSchema>({
    resolver: zodResolver(registerSchema),
  });

  const passwordValue = watch("password", "");

  const getStrength = (pass: string) => {
    let score = 0;
    if (!pass) return 0;
    if (pass.length > 8) score += 1;
    if (/[0-9]/.test(pass)) score += 1;
    if (/[^A-Za-z0-9]/.test(pass)) score += 1;
    return score;
  };

  const strength = getStrength(passwordValue);

  const onSubmit = async (data: RegisterSchema) => {
    setIsSubmitting(true);
    try {
      const response = await api.post("/api/auth/register", data);
      
      if (response.data.access_token) {
        // Auto login if token provided
        localStorage.setItem("access_token", response.data.access_token);
        localStorage.setItem("refresh_token", response.data.refresh_token);
        toast.success("Account created! Logging in...");
        router.push("/dashboard");
      } else {
        // Otherwise prompt login
        toast.success("Account created successfully. Please log in.");
        // Reload to reset state to login or just let user click
        window.location.reload(); 
      }
    } catch (err: any) {
        console.error("Registration Error:", err.response?.data || err);
        const errorMessage = err.response?.data?.error?.message || 
                           err.response?.data?.message || 
                           "Registration failed. Try again.";
                           
        setError("root", { 
           message: errorMessage
        });
        toast.error(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center w-full h-full px-12 bg-white">
      <div className="w-full max-w-sm space-y-8">
        <div className="text-center">
            <h2 className="text-3xl font-bold tracking-tight text-slate-900">Create Account</h2>
            <p className="text-sm text-slate-500 mt-2 font-medium">Start your productivity journey.</p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6 relative mt-4">
             <AnimatePresence>
                {errors.root && (
                  <motion.div 
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="p-3 bg-rose-50 text-rose-600 text-sm rounded-md text-center border border-rose-200 shadow-sm"
                  >
                    {errors.root.message}
                  </motion.div>
                )}
            </AnimatePresence>

             {/* Name Field */}
             <div className="relative group pt-2">
                <User className="absolute left-0 top-3.5 h-5 w-5 text-slate-400 z-10 transition-colors group-focus-within:text-blue-600" />
                <input
                  {...register("name")}
                  type="text"
                  id="reg-name"
                  className={cn(
                    "peer block w-full border-0 border-b-2 border-slate-300 bg-transparent pl-10 py-2.5 text-base text-slate-900 focus:border-blue-600 focus:outline-none focus:ring-0 focus:bg-blue-50/30 transition-all font-medium placeholder-transparent relative z-20",
                    errors.name && "border-rose-400 focus:border-rose-400 focus:bg-rose-50/10"
                  )}
                  placeholder=" " 
                />
                <label 
                  htmlFor="reg-name"
                  className={cn(
                    "absolute left-10 top-2.5 z-10 origin-[0] -translate-y-[24px] scale-75 transform text-sm text-slate-500 font-medium duration-300 peer-placeholder-shown:translate-y-0 peer-placeholder-shown:scale-100 peer-focus:-translate-y-[24px] peer-focus:scale-75 peer-focus:text-blue-600",
                     errors.name && "peer-focus:text-rose-500 text-rose-500"
                  )}
                >
                  Full Name
                </label>
                {errors.name && <span className="text-xs text-rose-500 font-medium absolute -bottom-5 left-0">{errors.name.message}</span>}
            </div>

            {/* Email Field */}
            <div className="relative group pt-4">
                <Mail className="absolute left-0 top-3.5 h-5 w-5 text-slate-400 z-10 transition-colors group-focus-within:text-blue-600" />
                <input
                  {...register("email")}
                  type="email"
                  id="reg-email"
                   className={cn(
                    "peer block w-full border-0 border-b-2 border-slate-300 bg-transparent pl-10 py-2.5 text-base text-slate-900 focus:border-blue-600 focus:outline-none focus:ring-0 focus:bg-blue-50/30 transition-all font-medium placeholder-transparent relative z-20",
                    errors.email && "border-rose-400 focus:border-rose-400 focus:bg-rose-50/10"
                  )}
                  placeholder=" " 
                />
                <label 
                  htmlFor="reg-email"
                  className={cn(
                    "absolute left-10 top-2.5 z-10 origin-[0] -translate-y-[24px] scale-75 transform text-sm text-slate-500 font-medium duration-300 peer-placeholder-shown:translate-y-0 peer-placeholder-shown:scale-100 peer-focus:-translate-y-[24px] peer-focus:scale-75 peer-focus:text-blue-600",
                     errors.email && "peer-focus:text-rose-500 text-rose-500"
                  )}
                >
                  Email Address
                </label>
                {errors.email && <span className="text-xs text-rose-500 font-medium absolute -bottom-5 left-0">{errors.email.message}</span>}
            </div>

            {/* Password Field */}
            <div className="relative group pt-4">
                <Lock className="absolute left-0 top-3.5 h-5 w-5 text-slate-400 z-10 transition-colors group-focus-within:text-blue-600" />
                <input
                  {...register("password")}
                   type={showPassword ? "text" : "password"}
                  id="reg-password"
                  className={cn(
                    "peer block w-full border-0 border-b-2 border-slate-300 bg-transparent pl-10 py-2.5 text-base text-slate-900 focus:border-blue-600 focus:outline-none focus:ring-0 focus:bg-blue-50/30 transition-all font-medium placeholder-transparent relative z-20 pr-10",
                    errors.password && "border-rose-400 focus:border-rose-400 focus:bg-rose-50/10"
                  )}
                  placeholder=" " 
                />
                 <label 
                  htmlFor="reg-password"
                  className={cn(
                    "absolute left-10 top-2.5 z-10 origin-[0] -translate-y-[24px] scale-75 transform text-sm text-slate-500 font-medium duration-300 peer-placeholder-shown:translate-y-0 peer-placeholder-shown:scale-100 peer-focus:-translate-y-[24px] peer-focus:scale-75 peer-focus:text-blue-600",
                    errors.password && "peer-focus:text-rose-500 text-rose-500"
                  )}
                >
                  Password
                </label>
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-0 top-3 text-slate-400 hover:text-blue-600 transition-colors z-30 bg-transparent p-1"
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
                
                {/* Strength Meter */}
                <div className="flex gap-1.5 mt-3 h-1.5 w-full">
                    <div className={cn("h-full flex-1 rounded-full transition-colors duration-300", strength > 0 ? "bg-rose-400" : "bg-slate-100")}></div>
                    <div className={cn("h-full flex-1 rounded-full transition-colors duration-300", strength > 1 ? "bg-amber-400" : "bg-slate-100")}></div>
                    <div className={cn("h-full flex-1 rounded-full transition-colors duration-300", strength > 2 ? "bg-emerald-400" : "bg-slate-100")}></div>
                </div>

                {errors.password && <span className="text-xs text-rose-500 font-medium absolute -bottom-5 left-0">{errors.password.message}</span>}
            </div>

            <Button 
                type="submit" 
                className="w-full h-12 rounded-md bg-blue-600 hover:bg-blue-700 text-white font-semibold tracking-wide shadow-lg shadow-blue-600/20 transition-all hover:scale-[1.02] active:scale-[0.98] mt-10 text-base"
                disabled={isSubmitting}
            >
               {isSubmitting ? <Loader2 className="animate-spin h-5 w-5" /> : "Create Account"}
            </Button>
        </form>
      </div>
    </div>
  );
}
