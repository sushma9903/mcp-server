MCP Tool Server

A lightweight Model Context Protocol (MCP) Tool Server built in Python that exposes real-world tools (weather, stock data, and internet search) over STDIO transport.
The server is designed to be discovered and invoked by MCP-compatible clients and future AI agents, and is validated using the official MCP Inspector.

🚀 Overview

This project demonstrates how to build a correct and production-aligned MCP server that:

Exposes reusable tools via MCP

Integrates real external APIs

Uses clear tool schemas and contracts

Separates protocol logic from backend logic

Can be directly consumed by AI agents in the future

The focus of this project is the tool layer, not agent reasoning.
It intentionally stops at the MCP boundary.

🧠 Architecture & Approach

The design follows a clean separation of responsibilities:

MCP Client / Inspector
        │
        │  (STDIO)
        ▼
MCP Server (server/main.py)
        │
        ├── Tool Definitions (server/tools/)
        │       ├── Weather Tool
        │       ├── Stock Price Tool
        │       └── Web Search Tool
        │
        └── Backend Logic (server/backend/data_store.py)
                ├── OpenWeather API
                ├── Stooq Market Data
                └── Google Custom Search


MCP Server handles protocol wiring and tool registration

Tools define schemas and execution boundaries

Backend layer contains all external API logic

No agent logic is included (by design)

This mirrors how real AI platforms expose tools internally.

🛠️ Tools Implemented
🌦️ Weather Tool (get_weather)

Fetches real-time weather data by city

Powered by OpenWeatherMap

Returns structured, agent-friendly JSON

📈 Stock Price Tool (get_stock_price)

Retrieves stock market data for a given symbol

Uses Stooq public market data (no API key required)

Automatically normalizes symbols (e.g. AAPL → aapl.us)

🌐 Web Search Tool (web_search)

Performs internet search using Google Custom Search

Uses official Google APIs (no scraping)

Returns clean search results with title, snippet, and link

Result count is relevance-based and API-controlled

📂 Project Structure
TASK1-MCP-SERVER
│
├── client/
│   └── mcp_client.py
│
├── server/
│   ├── main.py                  # MCP server entry point
│   │
│   ├── backend/
│   │   └── data_store.py         # External API integrations
│   │
│   ├── tools/
│   │   ├── get_weather.py
│   │   ├── get_stock_price.py
│   │   └── web_search.py
│
├── .env                          # API keys (not committed)
├── requirements.txt
└── README.md

⚙️ Prerequisites

Python 3.10+

Node.js (for MCP Inspector)

OpenWeatherMap API key

Google Custom Search API key + CSE ID

📦 Installation
# Clone repository
git clone <your-repo-url>
cd TASK1-MCP-SERVER

# Create virtual environment
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

🔐 Environment Configuration

Create a .env file in the project root:

OPENWEATHER_API_KEY=your_openweather_api_key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_custom_search_engine_id


Best practices:

.env is excluded from version control

No secrets are hardcoded

Server fails safely if keys are missing

▶️ Running the MCP Server

Start the server using the MCP Inspector:

npx @modelcontextprotocol/inspector python server/main.py


The server runs over STDIO and exposes all tools automatically.

🧪 Testing with MCP Inspector

Using the Inspector UI:

Select STDIO transport

Point to server/main.py

Start the server

Invoke tools interactively

Example: Web Search
{
  "query": "Model Context Protocol MCP",
  "num_results": 5
}

💡 Why STDIO Transport?

Ideal for local development and inspection

No open ports or network configuration

Secure and deterministic

Easily replaceable with HTTP transport later

🚧 What This Project Intentionally Excludes

AI agent logic

LangChain / LangGraph workflows

RAG pipelines

Memory or planning systems

Those layers are meant to sit on top of this server, not inside it.

🔮 Future Extensions

This server can be extended with:

AI agents that dynamically discover and call tools

LangChain or LangGraph integration

RAG pipelines grounded in web search

Stateful or memory-based agents

HTTP transport for remote deployment

No changes to existing tools are required.

✅ Key Takeaways

Correct MCP server implementation

Real external integrations

Clean tool contracts

Production-style separation of concerns

Agent-ready foundation