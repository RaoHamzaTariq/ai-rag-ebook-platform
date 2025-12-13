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
      console.log('Sending request to:', `${this.baseUrl}/agents/run`, 'with data:', request);
      const response = await fetch(`${this.baseUrl}/agents/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
      });

      console.log('Response status:', response.status);
      if (!response.ok) {
        const errorText = await response.text();
        console.error('API Error Response:', errorText);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }
      const result = await response.json();
      console.log('API Response:', result);
      return result;
    } catch (err) {
      console.error('AgentClient error:', err);
      // Re-throw with more context
      if (err instanceof Error) {
        throw new Error(`AgentClient error: ${err.message}. Please check that your backend is running at ${this.baseUrl}`);
      }
      throw err;
    }
  }
}

export const agentClient = new AgentClient();
export type { AgentRequest, AgentResponse };