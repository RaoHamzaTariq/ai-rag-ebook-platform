import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { Pool } from "pg";

export const auth = betterAuth({
    database: new Pool({
        connectionString: process.env.DATABASE_URL,
    }),
    plugins: [
        jwt({
            // JWKS endpoint
        })
    ],
    emailAndPassword: {
        enabled: true,
    },
    user: {
        additionalFields: {
            role: {
                type: "string",
                required: false,
                defaultValue: "user"
            }
        }
    },
    trustedOrigins: [
        process.env.FRONTEND_URL || "http://localhost:3000"
    ],
    // ✅ Add cookie settings for cross‑site session
    cookie: {
        name: "better-auth-session",
        httpOnly: true,   // Browser JS cannot read the cookie
        sameSite: "none", // Allow cross‑site cookies
        secure: true,     // Required if using HTTPS (Back4App provides HTTPS)
        path: "/"
    }   
});
