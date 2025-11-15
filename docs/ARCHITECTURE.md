# System Architecture - Prompt2Action AI Platform

## Table of Contents

1. [High-Level Architecture](#high-level-architecture)
2. [Component Architecture](#component-architecture)
3. [Data Flow](#data-flow)
4. [Agent Coordination](#agent-coordination)
5. [Database Schema](#database-schema)
6. [Technology Stack](#technology-stack)

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                          Client Layer                             │
│                                                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  ┌──────────┐ │
│  │  Web App    │  │  Mobile App │  │  CLI Tool  │  │ REST API │ │
│  │  (Browser)  │  │   (iOS/     │  │  (Python)  │  │  Client  │ │
│  │             │  │   Android)  │  │            │  │          │ │
│  └──────┬──────┘  └──────┬──────┘  └─────┬──────┘  └────┬─────┘ │
│         │                │                │              │       │
└─────────┼────────────────┼────────────────┼──────────────┼───────┘
          │                │                │              │
          └────────────────┴────────────────┴──────────────┘
                                  │
                                  │ HTTP/HTTPS
                                  │ WebSocket
                                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                        API Gateway Layer                          │
│                                                                    │
│  ┌──────────────────────┐     ┌───────────────────────────────┐  │
│  │  Django REST         │     │  Django Channels              │  │
│  │  Framework           │     │  (WebSocket Server)           │  │
│  │  - RESTful APIs      │     │  - Real-time updates          │  │
│  │  - Authentication    │     │  - Progress streaming         │  │
│  │  - Rate limiting     │     │  - Bi-directional comm        │  │
│  └──────────┬───────────┘     └───────────┬───────────────────┘  │
│             │                             │                        │
└─────────────┼─────────────────────────────┼────────────────────────┘
              │                             │
              ▼                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Multi-Agent Orchestration Layer                │
│                                                                    │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │           Coordinator Agent (Master Orchestrator)           │  │
│  │         • Chain of Responsibility Pattern                   │  │
│  │         • Task Distribution & Load Balancing                │  │
│  │         • Error Handling & Recovery                         │  │
│  └────────────┬───────────────────────────────────────────────┘  │
│               │                                                    │
│               ├──────┬─────────┬─────────┬─────────┬──────────┐  │
│               ▼      ▼         ▼         ▼         ▼          ▼  │
│  ┌─────────┐ ┌────┐ ┌──────┐ ┌────┐ ┌────────┐ ┌──────────┐   │
│  │ Planner │ │Dev │ │Review│ │Test│ │Document│ │ Quality  │   │
│  │  Agent  │ │Agt │ │Agent │ │Agt │ │  Agent │ │Assessment│   │
│  │         │ │    │ │      │ │    │ │        │ │  Agent   │   │
│  └─────────┘ └────┘ └──────┘ └────┘ └────────┘ └──────────┘   │
│                                                                    │
└─────────────┬──────────────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────────────────────┐
│                      Core Services Layer                          │
│                                                                    │
│  ┌──────────────────┐  ┌─────────────────┐  ┌────────────────┐  │
│  │ Workflow Engine  │  │  CCG Service    │  │ Quality        │  │
│  │                  │  │                 │  │ Assessment     │  │
│  │ • Workflow mgmt  │  │ • Code analysis │  │ Service        │  │
│  │ • Task queue     │  │ • Dependency    │  │                │  │
│  │ • State mgmt     │  │   mapping       │  │ • Code quality │  │
│  │ • Progress track │  │ • Complexity    │  │ • Test coverage│  │
│  │                  │  │   metrics       │  │ • Security scan│  │
│  └──────────────────┘  └─────────────────┘  └────────────────┘  │
│                                                                    │
│  ┌──────────────────┐  ┌─────────────────┐  ┌────────────────┐  │
│  │  Gemini API      │  │  Celery Worker  │  │  Logging &     │  │
│  │  Integration     │  │  Manager        │  │  Monitoring    │  │
│  │                  │  │                 │  │                │  │
│  │ • AI responses   │  │ • Background    │  │ • Error logs   │  │
│  │ • Context mgmt   │  │   tasks         │  │ • Performance  │  │
│  │ • Prompt eng     │  │ • Async jobs    │  │ • Metrics      │  │
│  └──────────────────┘  └─────────────────┘  └────────────────┘  │
└─────────────┬──────────────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Data & Cache Layer                             │
│                                                                    │
│  ┌──────────────────┐  ┌─────────────────┐  ┌────────────────┐  │
│  │   PostgreSQL     │  │     Redis       │  │  File Storage  │  │
│  │                  │  │                 │  │                │  │
│  │ • Workflows      │  │ • Session cache │  │ • Static files │  │
│  │ • Agents         │  │ • Celery broker │  │ • Media files  │  │
│  │ • Tasks          │  │ • Result backend│  │ • Generated    │  │
│  │ • Progress logs  │  │ • Channel layer │  │   artifacts    │  │
│  │ • Quality data   │  │ • Rate limiting │  │                │  │
│  │ • CCG data       │  │                 │  │                │  │
│  └──────────────────┘  └─────────────────┘  └────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. API Gateway Layer

```
Django Application (Port 8000)
├── REST API (Django REST Framework)
│   ├── Authentication & Authorization
│   ├── Request/Response Handling
│   ├── Rate Limiting
│   └── API Versioning
│
└── WebSocket Server (Django Channels + Daphne)
    ├── Real-time Progress Updates
    ├── Workflow Status Streaming
    ├── Agent Communication
    └── Live Notifications
```

### 2. Agent Coordination System

```
Coordinator Agent
    │
    ├─> Planner Agent
    │   ├─ Analyzes user prompt
    │   ├─ Creates execution plan
    │   └─ Defines task breakdown
    │
    ├─> Developer Agent
    │   ├─ Implements code
    │   ├─ Follows best practices
    │   └─ Generates documentation
    │
    ├─> Code Reviewer Agent
    │   ├─ Reviews code quality
    │   ├─ Suggests improvements
    │   └─ Ensures standards
    │
    ├─> Testing Agent
    │   ├─ Creates test cases
    │   ├─ Runs tests
    │   └─ Reports coverage
    │
    ├─> Documentation Agent
    │   ├─ Generates docs
    │   ├─ Creates README
    │   └─ API documentation
    │
    └─> Quality Assessment Agent
        ├─ Overall quality scoring
        ├─ Performance analysis
        └─ Security validation
```

### 3. Code Context Graph (CCG) Structure

```
CCG Node Types:
    - Module
    - Class
    - Function
    - Variable
    - Import

CCG Edge Types:
    - calls
    - inherits
    - imports
    - references
    - contains

Example CCG:
    Module_A ──imports──> Module_B
        │                     │
    contains              contains
        │                     │
        ▼                     ▼
    Class_X ──inherits──> Class_Y
        │                     │
    contains              contains
        │                     │
        ▼                     ▼
   Function_1 ──calls──> Function_2
```

---

## Data Flow

### Workflow Execution Flow

```
1. User submits prompt
   │
   ▼
2. Coordinator receives request
   │
   ├─> Creates Workflow object
   ├─> Validates input
   └─> Selects appropriate agents
   │
   ▼
3. Planner Agent analyzes
   │
   ├─> Breaks down into tasks
   ├─> Determines dependencies
   └─> Creates task queue
   │
   ▼
4. Tasks distributed to agents
   │
   ├─> Developer Agent
   ├─> Reviewer Agent
   ├─> Tester Agent
   └─> Documenter Agent
   │
   ▼
5. Real-time progress updates
   │
   ├─> WebSocket broadcasts
   ├─> Database logging
   └─> Client notifications
   │
   ▼
6. Quality Assessment
   │
   ├─> Code quality score
   ├─> Test coverage
   ├─> Documentation check
   ├─> Performance metrics
   └─> Security validation
   │
   ▼
7. Workflow completion
   │
   ├─> Results aggregation
   ├─> CCG generation
   └─> Final report
```

### Real-Time Communication Flow

```
Client                WebSocket               Channel Layer           Database
  │                      │                          │                    │
  │──Open WS Connection─>│                          │                    │
  │                      │──Subscribe to workflow──>│                    │
  │                      │                          │                    │
  │                      │                    [Task starts]               │
  │                      │                          │<──Create Progress──│
  │                      │<──Broadcast progress─────│                    │
  │<──Progress Update────│                          │                    │
  │                      │                          │                    │
  │                      │                    [Task completes]            │
  │                      │                          │<──Update Status────│
  │                      │<──Broadcast completion───│                    │
  │<──Completion Alert───│                          │                    │
  │                      │                          │                    │
```

---

## Database Schema

### Core Tables

```sql
-- Agents Table
CREATE TABLE agents_agent (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    agent_type VARCHAR(20) NOT NULL,
    description TEXT,
    capabilities JSONB DEFAULT '[]',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Workflows Table
CREATE TABLE agents_workflow (
    id SERIAL PRIMARY KEY,
    title VARCHAR(300) NOT NULL,
    description TEXT,
    user_id INTEGER REFERENCES auth_user(id),
    prompt TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    result_data JSONB DEFAULT '{}',
    error_message TEXT,
    code_context JSONB DEFAULT '{}'
);

-- Tasks Table
CREATE TABLE agents_task (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER REFERENCES agents_workflow(id),
    agent_id INTEGER REFERENCES agents_agent(id),
    name VARCHAR(300) NOT NULL,
    description TEXT,
    order INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'PENDING',
    progress_percentage INTEGER DEFAULT 0,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    result_data JSONB DEFAULT '{}',
    error_message TEXT
);

-- Progress Logs Table
CREATE TABLE agents_progresslog (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER REFERENCES agents_workflow(id),
    task_id INTEGER REFERENCES agents_task(id),
    message TEXT NOT NULL,
    log_level VARCHAR(20) DEFAULT 'INFO',
    metadata JSONB DEFAULT '{}',
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Quality Assessments Table
CREATE TABLE agents_qualityassessment (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER REFERENCES agents_workflow(id),
    task_id INTEGER REFERENCES agents_task(id),
    code_quality_score FLOAT DEFAULT 0.0,
    test_coverage_score FLOAT DEFAULT 0.0,
    documentation_score FLOAT DEFAULT 0.0,
    performance_score FLOAT DEFAULT 0.0,
    security_score FLOAT DEFAULT 0.0,
    overall_score FLOAT DEFAULT 0.0,
    feedback TEXT,
    recommendations JSONB DEFAULT '[]',
    assessed_at TIMESTAMP DEFAULT NOW(),
    assessed_by_id INTEGER REFERENCES agents_agent(id)
);

-- Code Context Graph Table
CREATE TABLE agents_codecontextgraph (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER UNIQUE REFERENCES agents_workflow(id),
    nodes JSONB DEFAULT '[]',
    edges JSONB DEFAULT '[]',
    metadata JSONB DEFAULT '{}',
    complexity_metrics JSONB DEFAULT '{}',
    dependencies JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## Technology Stack

### Backend Framework

```
Django 5.2.8
├── django-rest-framework 3.16.1  (REST API)
├── django-channels 4.3.1         (WebSockets)
├── django-cors-headers 4.9.0     (CORS)
└── daphne 4.2.1                  (ASGI Server)
```

### AI & ML

```
Google Gemini API
└── google-generativeai 0.8.5
```

### Task Queue & Caching

```
Celery 5.5.3
├── Redis 7.0.1                   (Broker & Backend)
└── channels-redis 4.3.0          (Channel Layer)
```

### Database

```
Development: SQLite3
Production:  PostgreSQL 15+
```

### Frontend

```
HTML5 + CSS3 + Vanilla JavaScript
└── WebSocket API for real-time updates
```

---

## Security Architecture

```
Security Layers:

1. Transport Security
   ├─ HTTPS (TLS 1.3)
   └─ WSS (WebSocket Secure)

2. Authentication
   ├─ Django Session Auth
   ├─ Token-based Auth (JWT)
   └─ API Key Authentication

3. Authorization
   ├─ Django Permissions
   ├─ Role-Based Access Control
   └─ Object-Level Permissions

4. Data Protection
   ├─ Environment Variables
   ├─ Secret Key Rotation
   └─ Database Encryption

5. API Security
   ├─ Rate Limiting
   ├─ CORS Configuration
   ├─ CSRF Protection
   └─ XSS Prevention
```

---

## Scalability Architecture

```
Horizontal Scaling:
    ├─ Multiple Django instances (Load Balanced)
    ├─ Celery worker pool
    └─ Redis cluster

Vertical Scaling:
    ├─ Database connection pooling
    ├─ Async task processing
    └─ Caching strategy

Performance Optimization:
    ├─ Database indexing
    ├─ Query optimization
    ├─ Static file CDN
    └─ Response compression
```

---

## Monitoring & Logging

```
Application Logging:
    ├─ Django logging (file + console)
    ├─ Celery task logs
    └─ Error tracking

Performance Monitoring:
    ├─ Response time tracking
    ├─ Database query analysis
    └─ Memory usage

Real-time Metrics:
    ├─ Active workflows
    ├─ Agent utilization
    ├─ Task queue length
    └─ WebSocket connections
```

---

**Created by:** Cavin Otieno  
**Contact:** cavin.otieno012@gmail.com  
**Last Updated:** November 2024
