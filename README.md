# Hotel Login Flow

A full-stack login flow demo for hotel users, using Node.js/Express, PostgreSQL, JWT authentication, and a responsive HTML login page.

## Features

- Login page for users (email & password)
- Secure backend API (Express, bcrypt, JWT)
- Users stored in `hotel_users` table in PostgreSQL
- JWTs include hotel_id and expire after 1 hour
- Token is stored in localStorage on successful login
- Dashboard page (stub) shown after login

## Folder Structure

```
server/
  package.json
  server.js
  db.js
  routes/
    auth.js
  .env.example

public/
  index.html
  dashboard.html

README.md
```

## Getting Started

### 1. Clone and Install

```bash
git clone &lt;your-repo-url&gt;
cd &lt;repo&gt;
cd server
npm install
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

- `DATABASE_URL`: PostgreSQL connection string (e.g. `postgres://user:pass@localhost:5432/yourdb`)
- `JWT_SECRET`: A long random string for signing JWTs
- `PORT`: (Optional) Port to run the backend (default 3000)

Your database should have a table called `hotel_users` with at least these columns:
- `id` (primary key)
- `email` (unique, TEXT)
- `password_hash` (bcrypt hash, TEXT)
- `hotel_id` (INTEGER)

### 3. Run the Server

```bash
cd server
node server.js
```

The backend will serve static files from `../public/` and expose `/api/login`.

### 4. Open in Browser

- Go to [http://localhost:3000/](http://localhost:3000/)
- Login with a user from your `hotel_users` table

## Usage

- On successful login, a JWT token is saved in `localStorage` and the user is redirected to `/dashboard.html`.
- If credentials are wrong, an error is shown (no redirect).
- The dashboard is a placeholder. Protecting it with auth is not implemented yet.

## Dependencies

- express
- pg
- bcrypt
- jsonwebtoken
- dotenv
- cors

## Notes

- CORS is enabled for static files (same-origin).
- Passwords are compared using bcrypt.
- JWT payload includes: `{ hotel_id }`
- All code is commented for clarity.

---

MIT License