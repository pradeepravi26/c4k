import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  env: {
    FASTAPI_BASE_URL: process.env.FASTAPI_BASE_URL,
  }
};

export default nextConfig;
