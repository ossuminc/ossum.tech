# RIDDL MCP Server

The RIDDL MCP (Model Context Protocol) server provides AI assistants with
RIDDL language intelligence. It enables AI-assisted authoring of RIDDL
specifications by giving language models access to parsing, validation, and
context-aware generation capabilities.

## Overview

The MCP server acts as a bridge between AI assistants and the RIDDL compiler.
When an AI assistant needs to work with RIDDL, it can:

- **Parse** RIDDL specifications to understand their structure
- **Validate** models for syntax and semantic correctness
- **Generate** new RIDDL definitions based on context and descriptions
- **Complete** partial specifications with appropriate syntax

This enables workflows where domain experts describe what they want in natural
language, and AI assistants translate those descriptions into valid RIDDL.

## Setup

### Prerequisites

- Docker Desktop installed and running
- macOS, Linux, or Windows with WSL2

### Building the Docker Image

```bash
# Clone the repository
git clone https://github.com/ossuminc/riddl-mcp-server.git
cd riddl-mcp-server

# Build the Docker image
sbt Docker/publishLocal
```

### Running the Server

1. Open Docker Desktop Dashboard
2. Find the `riddl-mcp-server` image
3. Click **Run** → expand **Optional Settings**
4. Set **Host port** to `8080`
5. Click **Run**

Alternatively, from the command line:

```bash
docker run -p 8080:8080 riddl-mcp-server
```

### Verifying the Server

Check the server is running:

```bash
curl http://localhost:8080/health
# Should return: {"status":"ok"}
```

## Authentication

The server requires API key authentication. Three methods are supported:

### 1. X-API-KEY Header (Recommended)

```bash
curl -H "X-API-KEY: your-api-key" http://localhost:8080/api/validate
```

### 2. Query Parameter

Useful for clients that don't support custom headers:

```bash
curl "http://localhost:8080/api/validate?api_key=your-api-key"
```

### 3. Bearer Token

Standard Authorization header:

```bash
curl -H "Authorization: Bearer your-api-key" http://localhost:8080/api/validate
```

### Configuring API Keys

API keys are configured via environment variables when running the container:

```bash
docker run -p 8080:8080 -e API_KEYS="key1,key2,key3" riddl-mcp-server
```

## API Endpoints

### Health Check

```
GET /health
```

Returns server status. No authentication required.

**Response:**
```json
{"status": "ok"}
```

### Validate

```
POST /api/validate
Content-Type: application/json
X-API-KEY: your-api-key
```

Validates a RIDDL specification.

**Request Body:**
```json
{
  "url": "https://raw.githubusercontent.com/org/repo/main/model.riddl"
}
```

**Response:**
```json
{
  "valid": true,
  "messages": []
}
```

Or with errors:
```json
{
  "valid": false,
  "messages": [
    {
      "severity": "error",
      "message": "Undefined reference: Customer",
      "location": {"line": 42, "column": 12}
    }
  ]
}
```

### Parse

```
POST /api/parse
Content-Type: application/json
X-API-KEY: your-api-key
```

Parses RIDDL and returns the abstract syntax tree.

**Request Body:**
```json
{
  "content": "domain Foo { context Bar { ??? } }"
}
```

### Generate

```
POST /api/generate
Content-Type: application/json
X-API-KEY: your-api-key
```

Generates RIDDL definitions based on description and context.

**Request Body:**
```json
{
  "description": "An entity that tracks customer orders with status",
  "context": "domain ECommerce { context OrderManagement { } }",
  "type": "entity"
}
```

## Integration with AI Assistants

### Claude Desktop

Add to your Claude Desktop MCP configuration:

```json
{
  "mcpServers": {
    "riddl": {
      "url": "http://localhost:8080",
      "headers": {
        "X-API-KEY": "your-api-key"
      }
    }
  }
}
```

### IntelliJ AI Assistant

Configure in IntelliJ IDEA settings:

1. Go to **Settings** → **Tools** → **AI Assistant**
2. Add MCP server with URL: `http://localhost:8080?api_key=your-api-key`

See the [RIDDL IDEA Plugin](../riddl-idea-plugin/index.md) for additional
integration features.

### Other MCP Clients

Any MCP-compatible client can connect using:

- **Server URL**: `http://localhost:8080`
- **Authentication**: API key via header, query param, or bearer token

## Usage Example

The typical workflow for AI-assisted RIDDL authoring:

1. **Author describes** what they want in natural language
2. **AI sends** the description to the MCP server's generate endpoint
3. **Server returns** valid RIDDL syntax
4. **AI presents** the generated RIDDL to the author
5. **Author refines** the description if needed
6. **AI validates** the final specification

Example conversation:

> **Author**: I need an entity to track user sessions with login time,
> last activity, and expiration.
>
> **AI**: Here's the generated entity:
> ```riddl
> entity Session is {
>   state Active is {
>     loginTime: TimeStamp
>     lastActivity: TimeStamp
>     expiration: TimeStamp
>     userId: Id(User)
>   }
>   handler SessionHandler is {
>     on command CreateSession { ??? }
>     on command UpdateActivity { ??? }
>     on command ExpireSession { ??? }
>   }
> }
> ```

## Command Line Usage

The server includes a bridge script for command-line validation:

```bash
# Validate a RIDDL file from GitHub
./src/main/scripts/riddl-mcp-bridge.sh \
  "https://raw.githubusercontent.com/org/repo/main/model.riddl"
```

The URL should be a GitHub "raw" content URL in the format:
```
https://raw.githubusercontent.com/<org>/<repo>/refs/heads/<branch>/<path>
```

## Configuration

Environment variables for the Docker container:

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEYS` | Comma-separated list of valid API keys | (none) |
| `PORT` | Server port | 8080 |
| `LOG_LEVEL` | Logging verbosity (debug, info, warn, error) | info |

## Troubleshooting

### Server Not Starting

1. Check Docker Desktop is running
2. Verify port 8080 is not in use: `lsof -i :8080`
3. Check container logs in Docker Desktop

### Authentication Errors (401)

1. Verify your API key is correct
2. Check the authentication method matches server configuration
3. For IntelliJ, use query parameter: `?api_key=your-key`

### Validation Timeouts

For large RIDDL specifications:

1. Increase Docker container memory limits
2. Consider validating smaller portions
3. Check network connectivity to GitHub for URL-based validation

## Resources

- [GitHub Repository](https://github.com/ossuminc/riddl-mcp-server)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Author's Guide](../../guides/authors/index.md) - AI-assisted authoring workflow
- [RIDDL Language Reference](../../references/language-reference.md)
