"use client";

import { motion, Reorder } from "framer-motion";
import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, GripVertical } from "lucide-react";
import { cn } from "@/lib/utils";

// Dummy Data with Semantic Status
const initialTasks = [
  { id: "1", title: "Draft Proposal", status: "In Progress", color: "bg-amber-100 text-amber-700" },
  { id: "2", title: "Launch Campaign", status: "Done", color: "bg-emerald-100 text-emerald-700" },
  { id: "3", title: "Review Q3 Metrics", status: "Overdue", color: "bg-rose-100 text-rose-700" },
];

export default function Home() {
  const [tasks, setTasks] = useState(initialTasks);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-slate-50 text-slate-900 selection:bg-blue-100">
      {/* Subtle Dot Grid Background */}
      <div className="absolute inset-0 -z-10 h-full w-full bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_70%,transparent_100%)]"></div>

      <main className="container mx-auto px-6 flex flex-col lg:flex-row items-center justify-between gap-16 py-20">
        
        {/* Left: Typography & CTA */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="flex-1 space-y-8 text-center lg:text-left start-hero-anim"
        >
          <div className="space-y-4">
            <h1 className="text-5xl font-bold tracking-tight text-gray-900 sm:text-6xl leading-tight">
              Organize Projects.<br />
              Execute Tasks.<br />
              Repeat.
            </h1>
            <p className="text-xl text-gray-500 max-w-lg mx-auto lg:mx-0 font-normal">
              Experience the flow state. A minimalist toolkit for deep work and clarity.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4">
            <Link href="/auth">
              <Button size="lg" className="rounded-md bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-600/20 px-8 h-12 text-base font-medium transition-transform hover:translate-y-[-1px]">
                Get Started Free <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>
        </motion.div>

        {/* Right: Antigravity Playground (Interactive Component) */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="flex-1 w-full max-w-md"
        >
          {/* Floating Card */}
          <motion.div
            animate={{ y: [0, -10, 0] }}
            transition={{ repeat: Infinity, duration: 6, ease: "easeInOut" }}
            className="relative overflow-hidden rounded-2xl border border-white/50 bg-white/80 backdrop-blur-md p-6 shadow-xl shadow-blue-900/5 ring-1 ring-slate-900/5"
          >
            <div className="mb-6 flex items-center justify-between border-b border-slate-100 pb-4">
              <div className="flex items-center gap-2">
                 <div className="h-3 w-3 rounded-full bg-red-400"></div>
                 <div className="h-3 w-3 rounded-full bg-amber-400"></div>
                 <div className="h-3 w-3 rounded-full bg-green-400"></div>
              </div>
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">My Tasks</span>
            </div>
            
            <Reorder.Group axis="y" values={tasks} onReorder={setTasks} className="space-y-3">
              {tasks.map((task) => (
                <Reorder.Item 
                  key={task.id} 
                  value={task}
                  whileDrag={{ scale: 1.02, boxShadow: "0px 10px 20px rgba(0,0,0,0.05)" }}
                  className="group flex cursor-grab active:cursor-grabbing items-center justify-between rounded-lg border border-slate-100 bg-white px-4 py-3 shadow-sm transition-all hover:border-blue-200 hover:shadow-md"
                >
                  <span className="font-medium text-slate-700">{task.title}</span>
                  <div className="flex items-center gap-3">
                    <span className={cn("px-2.5 py-0.5 rounded-full text-[10px] font-semibold uppercase tracking-wide", task.color)}>
                      {task.status}
                    </span>
                    <GripVertical className="h-4 w-4 text-slate-300 group-hover:text-slate-500" />
                  </div>
                </Reorder.Item>
              ))}
            </Reorder.Group>

            {/* Decorative Elements to enhance "Flow" vibe */}
            <div className="mt-8 flex justify-between items-center text-xs text-slate-400 px-1">
               <span>3 tasks active</span>
               <span>Synced just now</span>
            </div>
          </motion.div>
        </motion.div>
      </main>
    </div>
  );
}
