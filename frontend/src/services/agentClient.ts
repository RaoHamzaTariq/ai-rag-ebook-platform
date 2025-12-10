// frontend/src/services/agentClient.ts

// Define TypeScript interfaces for request and response
interface AgentRequest {
  agent_type: 'triage' | 'summarizer' | 'rag';
  query: string;
  current_page?: string;
  highlighted_text?: string;
  session_id?: string;
}

interface AgentResponse {
  message: string;
  sources?: Array<{slug: string, chapter_number: string, page_number: number, snippet: string}>;
  agent_used: string;
  timestamp: string;
}

class AgentClient {
  private baseUrl: string;

  constructor() {
    // Use environment variable or default to development backend
    this.baseUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
  }

  async runAgent(request: AgentRequest): Promise<AgentResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/agents/run`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: AgentResponse = await response.json();
      return data;
    } catch (error) {
      console.error('Error calling agent API:', error);
      throw error;
    }
  }
}

// Create a singleton instance
export const agentClient = new AgentClient();

// Export the types for use in other components
export type { AgentRequest, AgentResponse };