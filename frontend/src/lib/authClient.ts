import { createAuthClient } from "better-auth/react";

import siteConfig from '@generated/docusaurus.config';

export const authClient = createAuthClient({
  baseURL: siteConfig.customFields?.betterAuthUrl as string || "http://localhost:3001",
	fetchOptions: {
		credentials: "include"
	}
});

export const { signIn, signUp, useSession, signOut } = authClient;