import type { NextConfig } from "next";
import { config } from "dotenv";
import path from "path";

// Load .env from parent (root) directory
config({ path: path.resolve(__dirname, "../.env") });

const nextConfig: NextConfig = {
  env: {
    // Server-side API URL (Docker network)
    API_URL: process.env.API_URL,
    // Client-side API URL (Browser) - NEXT_PUBLIC_ prefix auto-exposes to client
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
};

export default nextConfig;
