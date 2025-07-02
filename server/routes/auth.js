// server/routes/auth.js
import express from "express";
import pool from "../db.js";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";

const router = express.Router();

/**
 * POST /api/login
 * Body: { email, password }
 * Response: { token } or 401 Unauthorized
 */
router.post("/login", async (req, res) => {
  const { email, password } = req.body || {};
  // Basic validation
  if (!email || !password) {
    return res.status(400).json({ error: "Email and password required." });
  }
  try {
    // Look up user by email
    const result = await pool.query(
      "SELECT id, hotel_id, password_hash FROM hotel_users WHERE email = $1",
      [email]
    );
    if (result.rows.length === 0) {
      // User not found
      return res.status(401).json({ error: "Invalid credentials." });
    }
    const user = result.rows[0];

    // Compare supplied password to the bcrypt hash
    const match = await bcrypt.compare(password, user.password_hash);
    if (!match) {
      return res.status(401).json({ error: "Invalid credentials." });
    }

    // Create JWT containing hotel_id (and optionally user id)
    const token = jwt.sign(
      { hotel_id: user.hotel_id },
      process.env.JWT_SECRET,
      { expiresIn: "1h" }
    );

    // Respond with the token
    res.json({ token });
  } catch (err) {
    console.error("Login error:", err);
    res.status(500).json({ error: "Internal server error." });
  }
});

export default router;