import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { Pool } from "pg";

export const auth = betterAuth({
    database: new Pool({
        connectionString: process.env.DATABASE_URL,
    }),
    plugins: [
        jwt({
            // The JWT plugin will expose the JWKS endpoint automatically at /api/auth/jwks
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
    ]
});
