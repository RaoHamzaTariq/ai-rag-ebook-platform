import "dotenv/config";
import express from "express";
import cors from "cors";
import { auth } from "./auth";
import { toNodeHandler } from "better-auth/node";

const app = express();
const port = process.env.PORT || 3001;

// CORS middleware must be registered before your routes
app.use(cors({
	origin: [
		"https://ai-ebook-platform.vercel.app",
		process.env.FRONTEND_URL || "http://localhost:3000"
	],
	credentials: true,
	methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
	allowedHeaders: ["Content-Type", "Authorization", "Cookie"]
}));

app.all("/api/auth/*", toNodeHandler(auth));

app.get("/", (req, res) => {
	res.json({ status: "ok" });
});

app.listen(port, () => {
	console.log(`Auth server listening on port ${port}`);
});