import { betterAuth } from "better-auth";
import { Pool } from "pg";

export const auth = betterAuth({
	baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL,
	database: new Pool({
		connectionString: process.env.DATABASE_URL,
		// CRITICAL: Give Neon time to wake up (15-30 seconds)
		connectionTimeoutMillis: 20000, 
		// CRITICAL: Neon requires SSL
		ssl: {
			rejectUnauthorized: false,
		},
	}),
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
		"https://ai-ebook-platform.vercel.app",
		process.env.FRONTEND_URL || "http://localhost:3000"
	],
	advanced: {
		defaultCookieAttributes: {
			sameSite: "none",
			secure: true,
		},
		useSecureCookies: true
	}
});
