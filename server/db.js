// server/db.js
import pkg from "pg";
import dotenv from "dotenv";
dotenv.config();

const { Pool } = pkg;

// Creates and exports a singleton pg Pool instance
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  // Add SSL config if using e.g. Heroku PG
  ssl: process.env.NODE_ENV === "production"
    ? { rejectUnauthorized: false }
    : false,
});

export default pool;