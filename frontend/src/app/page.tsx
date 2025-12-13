"use client";

import { motion, Reorder } from "framer-motion";
import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, CheckCircle2, GripVertical } from "lucide-react";

export default function Home() {
  const [items, setItems] = useState(["Draft Proposal", "Review Metrics", "Launch Campaign"]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-background text-foreground selection:bg-primary/20">
      <div className="absolute inset-0 -z-10 h-full w-full bg-[linear-gradient(to_right,#8080800a_1px,transparent_1px),linear-gradient(to_bottom,#8080800a_1px,transparent_1px)] bg-[size:14px_24px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]"></div>
      
      <main className="container mx-auto px-4 flex flex-col lg:flex-row items-center justify-between gap-12 py-20">
        
        {/* Helper/Hero Section */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="flex-1 space-y-6 text-center lg:text-left"
        >
          <div className="inline-block rounded-full bg-secondary px-3 py-1 text-sm font-medium text-secondary-foreground">
            v1.0 Antigravity
          </div>
          <h1 className="text-5xl font-extrabold tracking-tight sm:text-7xl">
            <span className="block">Organize Projects.</span>
            <span className="block text-primary/60">Execute Tasks.</span>
            <span className="block text-primary/30">Repeat.</span>
          </h1>
          <p className="mx-auto lg:mx-0 max-w-2xl text-lg text-muted-foreground">
            Experience the flow state. A friction-free task management tool designed for kinetic productivity.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 pt-4">
            <Link href="/login">
              <Button size="lg" className="rounded-full text-base font-semibold px-8 h-12">
                Get Started <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
            <Link href="/register">
              <Button variant="outline" size="lg" className="rounded-full text-base px-8 h-12">
                Create Account
              </Button>
            </Link>
          </div>
        </motion.div>

        {/* Interactive Demo (Antigravity Hook) */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="flex-1 w-full max-w-md"
        >
          <div className="relative overflow-hidden rounded-2xl border bg-card/50 backdrop-blur-xl p-8 shadow-2xl">
            <div className="mb-6 flex items-center justify-between">
              <h3 className="font-semibold text-foreground">Playground</h3>
              <span className="text-xs text-muted-foreground">Try dragging items</span>
            </div>
            
            <Reorder.Group axis="y" values={items} onReorder={setItems} className="space-y-3">
              {items.map((item) => (
                <Reorder.Item 
                  key={item} 
                  value={item}
                  whileDrag={{ scale: 1.05, boxShadow: "0px 10px 30px rgba(0,0,0,0.1)" }}
                  className="group flex cursor-grab active:cursor-grabbing list-none items-center justify-between rounded-xl border bg-card px-4 py-3 shadow-sm transition-colors hover:border-primary/50"
                >
                  <div className="flex items-center gap-3">
                    <div className="rounded-full border p-1 text-muted-foreground transition-colors group-hover:text-primary">
                      <CheckCircle2 className="h-4 w-4" />
                    </div>
                    <span className="font-medium">{item}</span>
                  </div>
                  <GripVertical className="h-4 w-4 text-muted-foreground/50" />
                </Reorder.Item>
              ))}
            </Reorder.Group>

            <div className="mt-6 flex justify-center">
               <motion.div 
                 className="h-1 w-20 rounded-full bg-primary/20"
                 layoutId="underline"
               />
            </div>
          </div>
        </motion.div>
      </main>
    </div>
  );
}
