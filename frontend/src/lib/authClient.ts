import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL as string || "http://localhost:3001",
	fetchOptions: {
		credentials: "include"
	},
  plugins: [
    jwtClient()
  ]
});

export const { signIn, signUp, useSession, signOut } = authClient;