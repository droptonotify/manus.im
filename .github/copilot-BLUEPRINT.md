# Copilot Instructions Blueprint

This document outlines the process used to generate the `.github/copilot-instructions.md` file for the Manus project.

## Objective

The primary goal was to analyze the Manus codebase to create a comprehensive set of instructions for AI coding agents. The instructions are intended to help agents quickly understand the project's architecture, conventions, and workflows, enabling them to be more effective contributors.

## Process

The following steps were taken to gather information and generate the instructions:

1.  **Initial Analysis**: The process began by reviewing the existing `.github/copilot-instructions.md` file to understand the baseline level of documentation.

2.  **Comprehensive Codebase Review**: To gain a deeper understanding of the project, the following key documents were reviewed:
    *   `README.md`: Provided a high-level overview of the project, its features, and deployment instructions.
    *   `backend/README.md`: Offered detailed insights into the backend's Domain-Driven Design (DDD) architecture, API endpoints, and development setup.
    *   `frontend/README.md`: Explained the frontend's structure, technology stack (Vue.js, TypeScript), and development process.
    *   `sandbox/README.md`: Detailed the sandbox's role in providing an isolated execution environment, its API, and the tools it supports.

3.  **Synthesis and Generation**: The information gathered from these documents was synthesized to create a new, more detailed `.github/copilot-instructions.md` file. The new instructions were structured to provide a clear and logical flow of information, starting with a high-level overview and then diving into more specific details.

## Key Findings

The analysis of the codebase revealed several key aspects of the project that were crucial to document in the instructions:

-   **Three-Part Architecture**: The project is divided into three distinct components: a `frontend`, a `backend`, and a `sandbox`. Understanding the role of each component and how they interact is fundamental to working on the project.
-   **Domain-Driven Design (DDD)**: The backend's use of DDD is a critical architectural pattern that developers and AI agents need to be aware of. The instructions highlight the different layers of the DDD architecture and their responsibilities.
-   **Communication Flow**: The communication patterns between the components (REST API, SSE, WebSockets) are essential for understanding how data flows through the system.
-   **Development Workflows**: The project has well-defined workflows for development, debugging, and deployment, which are documented in the instructions to help agents get started quickly.
-   **Tool Extensibility**: The process for adding new tools to the system is a key pattern that was important to document.

## Generated Instructions

The new `.github/copilot-instructions.md` file is organized into the following sections:

-   **Project Overview**: A high-level introduction to the project and its components.
-   **Key Architecture Patterns**: An explanation of the core architectural patterns used in the project.
-   **Development Workflows**: Step-by-step instructions for setting up the development environment and common development tasks.
-   **Critical Files**: A list of the most important files in the codebase.
-   **Project Conventions**: An overview of the project's coding conventions, including error handling and state management.
-   **Integration Points**: A description of how the project integrates with external services like LLMs and databases.
-   **Common Tasks**: Instructions for common tasks like debugging and deployment.

## Feedback Request

Please review the generated `.github/copilot-instructions.md` file. Any feedback on sections that are unclear, incomplete, or could be improved would be greatly appreciated. This will help to further refine the instructions and make them as useful as possible for AI agents.
