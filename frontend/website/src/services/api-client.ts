// API client for backend communication

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

interface QueryRequest {
  query: string;
  selected_text?: string;
  session_id?: string;
  context_window?: number;
}

interface QueryResponse {
  response: string;
  sources: Array<{
    source_path: string;
    source_title: string;
    relevance_score: number;
  }>;
  session_id: string;
  followup_questions: string[];
}

interface IngestRequest {
  docs_path: string;
  chunk_size?: number;
  chunk_overlap?: number;
}

interface IngestResponse {
  status: string;
  chunks_processed: number;
  documents_processed: number;
  message: string;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async query(request: QueryRequest): Promise<QueryResponse> {
    const response = await fetch(`${this.baseUrl}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Query request failed: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async ingest(request: IngestRequest): Promise<IngestResponse> {
    const response = await fetch(`${this.baseUrl}/ingest`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Ingest request failed: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async refresh(request: IngestRequest): Promise<IngestResponse> {
    const response = await fetch(`${this.baseUrl}/ingest/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Refresh request failed: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async health(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/health`);

    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }
}

export default new ApiClient();