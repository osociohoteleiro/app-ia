// server/server.js
import express from "express";
import dotenv from "dotenv";
import cors from "cors";
import path from "path";
import { fileURLToPath } from "url";

import authRouter from "./routes/auth.js";

// Load environment variables from .env (if present)
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Enable JSON request parsing
app.use(express.json());

// Enable CORS (default allows same-origin, which is fine for static/public)
app.use(cors());

// Mount /api routes
app.use("/api", authRouter);

// Serve static files from public/
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
app.use(express.static(path.join(__dirname, "../public")));

// Fallback: serve index.html for root
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "../public/index.html"));
});

// Start server
app.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}`);
});