# AI Sheikh Agent Instructions

This document guides AI coding agents to effectively navigate and contribute to the AI Sheikh codebase.

## Project Overview

AI Sheikh is a general-purpose AI Agent system designed to run tools and operations in isolated sandbox environments. The system has three core components:

1.  **Frontend (Vue.js/TypeScript)**: Web interface for user interactions, located in the `frontend` directory.
2.  **Backend (Python/FastAPI)**: Core agent orchestration and business logic, located in the `backend` directory.
3.  **Sandbox (Docker)**: Isolated environment for tool execution, located in the `sandbox` directory.

## Key Architecture Patterns

### Domain-Driven Design (DDD)

The backend follows a strict DDD layered architecture:

-   `app/domain/`: Core business logic, models, and services. This is where the fundamental business rules are implemented.
-   `app/application/`: Orchestrates business processes by coordinating domain objects.
-   `app/interfaces/`: Defines external system interfaces, primarily the API routes for the frontend.
-   `app/infrastructure/`: Contains the technical implementations of external services like databases and third-party APIs.

### Real-time Communication Flow

-   **Frontend ↔ Backend**: Communication is handled via a REST API for standard requests and Server-Sent Events (SSE) for real-time updates from the agent.
-   **Backend → Sandbox**: The backend communicates with the sandbox via a REST API to execute tools and commands.
-   **Frontend ↔ Sandbox**: For interactive tools like the browser, the frontend connects to the sandbox via a WebSocket proxy for VNC and browser control.

## Development Workflows

### Initial Setup

To set up the development environment, follow these steps:

```bash
# Clone the repository
git clone https://github.com/simpleyyt/ai-sheikh.git
cd ai-sheikh

# Copy the example environment file and configure it
cp .env.example .env

# Start the development environment
./dev.sh up
```

This will start all services in reload mode with the following ports:

-   `5173`: Frontend
-   `8000`: Backend API
-   `8080`: Sandbox API
-   `5900`: Sandbox VNC
-   `9222`: Sandbox Chrome CDP

### Common Patterns

#### Adding New Tools

To add a new tool to the system, you need to:

1.  **Define the tool's API in the sandbox**: Add a new endpoint in `sandbox/app/api/v1/`.
2.  **Implement the tool's service in the backend**: Create a new service in the backend that calls the sandbox API.
3.  **Create a frontend visualization component (if needed)**: If the tool has a UI component, create it in `frontend/src/components/`.
4.  **Register the tool with the agent orchestration**: Integrate the new tool into the agent's workflow in the backend.

A good example to follow is the `ShellTool` implementation, which is present in all three components.

#### Sandbox Management

-   Each agent session is assigned an isolated sandbox container.
-   Tools are executed via the sandbox's API endpoints.
-   Browser automation is handled through the Chrome DevTools Protocol (CDP).
-   File and shell access are provided through the sandboxed API.

## Critical Files

-   `backend/app/main.py`: The application's entry point and lifecycle management.
-   `backend/app/domain/services/`: The core logic of the agent.
-   `sandbox/app/api/v1/`: The implementations of the tool APIs.
-   `frontend/src/components/`: The visualization components for the tools.

## Project Conventions

### Error Handling

-   Use domain-specific exceptions in the `app/domain` layer.
-   Register error handlers in `app/interfaces/errors`.
-   Propagate errors to the frontend for display using SSE.

### State Management

-   Session state is stored in MongoDB or Redis.
-   Real-time updates are sent to the frontend via SSE.
-   Browser state is managed through VNC and CDP.

### Testing

-   Unit tests are written with `pytest` and are located in the `tests/` directory.
-   End-to-end testing is performed using Docker Compose.

## Integration Points

### LLM Integration

-   The system is compatible with the OpenAI API interface.
-   The LLM must support `FunctionCall` and `JSON Format` output.

### External Services

-   **MongoDB**: Used for session storage.
-   **Redis**: Used for caching and real-time data.
-   **Docker**: Used for sandbox isolation.

## Common Tasks

### Debugging

If you encounter issues, you can rebuild the Docker images and restart the services:

```bash
# Stop and remove the containers
./dev.sh down -v

# Rebuild the images
./dev.sh build

# Start the services
./dev.sh up
```

### Deployment

To deploy the application, you can use the `run.sh` script:

```bash
# Set the image registry
export IMAGE_REGISTRY=your-registry

# Build the images
./run build

# Push the images
./run push
