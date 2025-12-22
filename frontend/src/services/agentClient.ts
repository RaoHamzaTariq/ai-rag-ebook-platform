// frontend/src/services/agentClient.ts
import { authClient } from '../lib/authClient';

interface AgentRequest {
  agent_type: 'triage' | 'summarizer' | 'rag';
  query: string;
  current_page?: string;
  highlighted_text?: string;
  session_id?: string;
}

interface AgentResponse {
  message: string;
  sources?: Array<{ slug: string; chapter_number: string; page_number: number; snippet: string }>;
  agent_used: string;
  timestamp: string;
}

import siteConfig from '@generated/docusaurus.config';

class AgentClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = (siteConfig.customFields?.backendUrl as string) || 'http://localhost:8000';
  }

  async runAgent(request: AgentRequest): Promise<AgentResponse> {
    try {
      // Get the session to see if user is logged in
      const { data: session } = await authClient.getSession();

      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };

      // Simple Mode: Send user ID in a header if we have one
      if (session?.user?.id) {
        headers['X-User-ID'] = session.user.id;
        console.log(`Authenticated request for user: ${session.user.id}`);
      }

      // Still try to get the JWT token but handle failure gracefully
      try {
        const tokenResult = await authClient.token();

        if (tokenResult?.data?.token) {
          headers['Authorization'] = `Bearer ${tokenResult.data.token}`;
        }
      } catch (tokenErr) {
        console.log('JWT Fetch skipped or failed, using simple user identification', tokenErr);
      }

      const response = await fetch(`${this.baseUrl}/agents/run`, {
        method: 'POST',
        headers,
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Agent API error:', response.status, errorText);
        throw new Error(`Chatbot error (${response.status}). Please ensure backend is running.`);
      }

      return await response.json();
    } catch (err) {
      console.error('AgentClient error:', err);
      throw err;
    }
  }
}

export const agentClient = new AgentClient();
export type { AgentRequest, AgentResponse };