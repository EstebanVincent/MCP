# Esteban's MCP Server Collection

A comprehensive repository containing Model Context Protocol (MCP) servers, clients, and workspace configurations. This collection provides various AI-powered tools and services that integrate seamlessly with VS Code and other MCP-compatible applications.

## Repository Structure

```
mcp/
├── clients/          # MCP client implementations
├── servers/          # MCP server implementations
│   └── fal_ai_server/ # AI image generation server
├── workspace/        # Shared workspace configurations
└── README.md        # This file
```

## What is MCP?

The Model Context Protocol (MCP) is an open standard for connecting AI assistants to external data sources and tools. It enables secure, controlled integration between AI systems and various services, databases, and applications.

## Servers Available

### 🎨 Fal AI Server (`fal_ai_server`)
**Location**: `mcp/servers/fal_ai_server/`

An AI image generation server powered by Fal.ai's FLUX.1 DEV model with custom LoRA support.

**Features:**
- High-quality image generation with FLUX.1 DEV
- Custom Esteban LoRA for personalized character generation
- Intelligent prompt enhancement using Azure OpenAI
- Dockerized deployment for easy setup

**Tools:**
- `generate_image_with_lora`: Generate images with custom LoRA
- `improve_user_query_for_flux`: Enhance prompts for better results

[📖 Full Documentation](./mcp/servers/fal_ai_server/README.md)

## Getting Started

### Prerequisites

- **Docker**: Required for containerized server deployment
- **VS Code**: With MCP extension for seamless integration
- **UV**: Python package manager for dependency management
- **Python 3.12+**: Runtime environment

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd mcp
   ```

2. **Choose a server to set up**
   ```bash
   cd mcp/servers/fal_ai_server  # Example: Fal AI server
   ```

3. **Build the Docker image**
   ```bash
   docker build -t mcp-fal-ai .
   ```

4. **Configure VS Code MCP settings**
   - Copy the server configuration to your `.vscode/mcp.json`
   - Provide required API keys when prompted

5. **Start the server in VS Code**
   - Open Command Palette (`Cmd+Shift+P`)
   - Run "MCP: Connect to Server"
   - Select your server and enjoy!

## Development Philosophy

This repository follows these core principles:

### 🔧 **One Project Per MCP Server**
Each MCP server is a self-contained project with its own:
- Dependencies managed by UV
- Docker configuration
- Documentation
- Configuration files

### 📦 **UV for Dependency Management**
All Python projects use [UV](https://github.com/astral-sh/uv) for:
- Fast dependency resolution
- Reproducible builds
- Lock file management
- Virtual environment handling

### 🐳 **Docker-First Deployment**
Each server includes:
- Optimized Dockerfile
- Multi-stage builds where appropriate
- Minimal production images
- Clear port configurations

### 📋 **Comprehensive Documentation**
Every server includes:
- Detailed README with setup instructions
- API documentation for available tools
- Configuration examples
- Troubleshooting guides

## Project Architecture

### Dependency Management with UV

Each server project includes:
- `pyproject.toml`: Project configuration and dependencies
- `uv.lock`: Locked dependency versions for reproducibility

Example workflow:
```bash
# Install dependencies
uv sync

# Add new dependency
uv add package-name

# Run the server
uv run mcp run main.py:mcp
```

### Docker Integration

Standard Dockerfile pattern across all servers:
```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /app
WORKDIR /app
RUN uv sync --locked

EXPOSE <port>
CMD ["uv", "run", "mcp", "run", "main.py:mcp"]
```

### VS Code Integration

Each server provides an MCP configuration for seamless VS Code integration:
- Environment variable management
- Input prompts for API keys
- Docker container orchestration
- Port forwarding configuration

## Adding New Servers

To add a new MCP server to this collection:

1. **Create server directory**
   ```bash
   mkdir -p mcp/servers/your-server-name
   cd mcp/servers/your-server-name
   ```

2. **Initialize UV project**
   ```bash
   uv init
   uv add "mcp[cli]>=1.11.0"
   ```

3. **Create server implementation**
   ```python
   # main.py
   from mcp.server.fastmcp import FastMCP
   
   mcp = FastMCP("Your Server Name")
   
   @mcp.tool()
   def your_tool():
       """Tool description"""
       return "Tool result"
   ```

4. **Add Dockerfile**
   ```dockerfile
   FROM python:3.12-slim
   COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
   
   ADD . /app
   WORKDIR /app
   RUN uv sync --locked
   
   EXPOSE 8080
   CMD ["uv", "run", "mcp", "run", "main.py:mcp"]
   ```

5. **Configure VS Code MCP settings**
    - Update `.vscode/mcp.json`
    - Provide required API keys and configurations
  
6. **Create documentation**
   - Add comprehensive README.md
   - Include setup instructions
   - Document all available tools

7. **Update this README**
   - Add server to the "Servers Available" section
   - Include brief description and features
