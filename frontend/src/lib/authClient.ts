import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
	baseURL: "https://authserver1-r9l3i286.b4a.run",
	fetchOptions: {
		credentials: "include"
	},
	plugins: [
		jwtClient()
	]
});

export const { signIn, signUp, useSession, signOut } = authClient;