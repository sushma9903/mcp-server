# MCP Tool Server

A lightweight **Model Context Protocol (MCP) Tool Server** built in Python that exposes real-world tools (weather, stock data, and internet search) over **STDIO transport**.
The server is designed to be discovered and invoked by MCP-compatible clients and future AI agents, and is validated using the official **MCP Inspector**.

---

## 🚀 Overview

This project demonstrates how to build a **correct and production-aligned MCP server** that:

* Exposes reusable tools via MCP
* Integrates real external APIs
* Uses clear tool schemas and contracts
* Separates protocol logic from backend logic
* Can be directly consumed by AI agents in the future

The focus of this project is the **tool layer**, not agent reasoning.
It intentionally stops at the MCP boundary.

---

## 🧠 Architecture & Approach

The design follows a clean separation of responsibilities:

```
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
```

* **MCP Server** handles protocol wiring and tool registration
* **Tools** define schemas and execution boundaries
* **Backend layer** contains all external API logic
* **No agent logic is included** (by design)

This mirrors how real AI platforms expose tools internally.

---

## 🛠️ Tools Implemented

### 🌦️ Weather Tool (`get_weather`)

* Fetches real-time weather data by city
* Powered by OpenWeatherMap
* Returns structured, agent-friendly JSON

### 📈 Stock Price Tool (`get_stock_price`)

* Retrieves stock market data for a given symbol
* Uses Stooq public market data (no API key required)
* Automatically normalizes symbols (e.g. `AAPL → aapl.us`)

### 🌐 Web Search Tool (`web_search`)

* Performs internet search using Google Custom Search
* Uses official Google APIs (no scraping)
* Returns clean search results with title, snippet, and link
* Result count is relevance-based and API-controlled

---

## 📂 Project Structure

```
TASK1-MCP-SERVER
│
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
```

---

## ⚙️ Prerequisites

* Python 3.10+
* Node.js (for MCP Inspector)
* OpenWeatherMap API key
* Google Custom Search API key + CSE ID

---

## 📦 Installation

```bash
# Clone repository
git clone <your-repo-url>
cd TASK1-MCP-SERVER

# Create virtual environment
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

Create a `.env` file in the project root:

```env
OPENWEATHER_API_KEY=your_openweather_api_key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_custom_search_engine_id
```

**Best practices:**

* `.env` is excluded from version control
* No secrets are hardcoded
* Server fails safely if keys are missing

---

## ▶️ Running the MCP Server

Start the server using the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector python server/main.py
```

The server runs over **STDIO** and exposes all tools automatically.

---

## 🧪 Testing with MCP Inspector

Using the Inspector UI:

1. Select **STDIO** transport
2. Point to `server/main.py`
3. Start the server
4. Invoke tools interactively

### Example Tool Invocations

#### 🌐 Web Search

**Input:**
```json
{
  "query": "Model Context Protocol MCP",
  "num_results": 5
}
```

**Output:**
```json
{
  "results": [
    {
      "title": "Model Context Protocol Documentation",
      "link": "https://modelcontextprotocol.io/",
      "snippet": "The Model Context Protocol (MCP) is an open protocol that standardizes how applications provide context to LLMs..."
    },
    {
      "title": "Introducing the Model Context Protocol",
      "link": "https://anthropic.com/news/model-context-protocol",
      "snippet": "Today, we're introducing the Model Context Protocol (MCP), a new standard for connecting AI assistants..."
    }
  ]
}
```

---

#### 🌦️ Weather Tool

**Input:**
```json
{
  "city": "San Francisco"
}
```

**Output:**
```json
{
  "city": "San Francisco",
  "temperature": 18.5,
  "conditions": "Clear sky",
  "humidity": 65,
  "wind_speed": 3.5
}
```

---

#### 📈 Stock Price Tool

**Input:**
```json
{
  "symbol": "AAPL"
}
```

**Output:**
```json
{
  "symbol": "AAPL",
  "price": 195.89,
  "currency": "USD",
  "timestamp": "2024-01-15T16:00:00",
  "change": "+2.34",
  "change_percent": "+1.21%"
}
```

---

## 🚧 Why STDIO Transport?

**STDIO was chosen because it provides the simplest, most reliable path for tool development and validation.**

### What STDIO Gives You

* **Zero configuration**: No ports, no networking, no HTTP servers to manage
* **Perfect for inspection**: MCP Inspector works flawlessly with STDIO
* **Deterministic lifecycle**: Process starts when called, exits when done
* **Secure by default**: No exposed endpoints or security concerns
* **Easy debugging**: Direct input/output makes testing and troubleshooting straightforward

### Why Not HTTP/SSE?

While HTTP and Server-Sent Events (SSE) transports are valid MCP options, they introduce unnecessary complexity for a tool server:

**HTTP Transport Issues:**
* Requires managing a persistent web server alongside MCP logic
* Adds lifecycle complexity (when to start/stop, connection pooling, etc.)
* Makes local testing harder - you need HTTP clients, manage ports, handle CORS
* Overkill for simple tool execution that doesn't need persistent connections

**SSE Transport Issues:**
* Designed for streaming real-time updates, not one-shot tool calls
* Requires long-lived connections and complex client-side stream handling
* Harder to debug tool execution due to streaming semantics
* More complex error recovery and retry logic
* Inspector support is less mature

### When to Use Other Transports

* **HTTP**: When you need remote deployment or multiple clients calling the server simultaneously
* **SSE**: When building streaming AI agents that need real-time, progressive responses

For a foundational tool server focused on correctness and reliability, STDIO is the right choice. You can always add HTTP transport later without changing any tool implementations.

---

## 💡 What This Project Intentionally Excludes

* AI agent logic
* LangChain / LangGraph workflows
* RAG pipelines
* Memory or planning systems

Those layers are meant to sit **on top of this server**, not inside it.

---

## 🔮 Future Extensions

This server can be extended with:

* AI agents that dynamically discover and call tools
* LangChain or LangGraph integration
* RAG pipelines grounded in web search
* Stateful or memory-based agents
* HTTP transport for remote deployment

No changes to existing tools are required.

---

## ✅ Key Takeaways

* Correct MCP server implementation using STDIO transport
* Real external integrations (weather, stocks, search)
* Clean tool contracts with clear input/output schemas
* Production-style separation of concerns
* Agent-ready foundation that can scale to complex workflows

---

## 📚 Additional Resources

* [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
* [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
* [OpenWeatherMap API](https://openweathermap.org/api)
* [Google Custom Search API](https://developers.google.com/custom-search)

---

