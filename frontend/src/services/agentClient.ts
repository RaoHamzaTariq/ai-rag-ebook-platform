// frontend/src/services/agentClient.ts

interface AgentRequest {
  agent_type: 'triage' | 'summarizer' | 'rag';
  query: string;
  current_page?: string;
  highlighted_text?: string;
  session_id?: string;
}

interface AgentResponse {
  message: string;
  sources?: Array<{slug: string; chapter_number: string; page_number: number; snippet: string}>;
  agent_used: string;
  timestamp: string;
}

class AgentClient {
  private baseUrl: string;

  constructor() {
    // ----------  fix starts  ----------
    // Docusaurus does NOT ship `process` to the browser, so we guard it.
    const maybeUrl =
      typeof process !== 'undefined' && process.env?.REACT_APP_BACKEND_URL
        ? process.env.REACT_APP_BACKEND_URL
        : undefined;

    this.baseUrl = maybeUrl || 'http://localhost:8000';
    // ----------  fix ends  ----------
  }

  async runAgent(request: AgentRequest): Promise<AgentResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/agents/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
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