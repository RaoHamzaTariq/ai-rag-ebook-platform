import "dotenv/config";

import express from "express";
import cors from "cors";
import { auth } from "./auth";
import { toNodeHandler } from "better-auth/node";

const app = express();
const port = process.env.PORT || 3001;

app.use(cors({
    origin: [process.env.FRONTEND_URL || "http://localhost:3000"],
    credentials: true,
    methods: ["GET","POST","PUT","DELETE","OPTIONS"],
    allowedHeaders: ["Content-Type","Authorization","Cookie"]
}));

app.all("/api/auth/*", toNodeHandler(auth));

app.listen(port, () => {
    console.log(`Auth server listening on port ${port}`);
});

app.get("/", (req, res) => {
  res.json({ status: "ok" });
});
