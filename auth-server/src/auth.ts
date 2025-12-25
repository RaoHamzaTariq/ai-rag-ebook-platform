import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { Pool } from "pg";

export const auth = betterAuth({
	baseURL: process.env.BASE_URL || "https://authserver1-r9l3i286.b4a.run",
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