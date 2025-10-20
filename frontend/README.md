# FIAE AI Content Factory - Modern Frontend

## 🚀 Production-Ready Enterprise UI

This is the modern, professional frontend for the FIAE Agentic AI System. It provides a comprehensive dashboard for managing multi-agent workflows, real-time monitoring, and enterprise-grade content processing.

## ✨ Key Features

### 🎯 **Enterprise Dashboard**
- **Executive Overview**: Real-time system metrics and KPIs
- **Agent Workflow Visualization**: Live multi-agent orchestration display
- **Processing Queue Management**: Document processing pipeline monitoring
- **System Health Monitoring**: Real-time performance metrics and alerts

### 🤖 **Multi-Agent Integration**
- **CrewAI Orchestration**: Professional multi-agent coordination
- **RAG System Management**: Knowledge base and vector database control
- **LangGraph Workflows**: Intelligent state management visualization
- **Real-time Agent Status**: Live updates via WebSocket connections

### 📊 **Professional Analytics**
- **Performance Metrics**: Processing speed, success rates, quality scores
- **Content Intelligence**: Pattern recognition and quality prediction
- **Cost Monitoring**: Budget tracking and resource utilization
- **Human-in-the-Loop**: Approval workflows and review management

### 🔒 **Enterprise Features**
- **Production Monitoring**: Comprehensive system observability
- **Alert Management**: Real-time notifications and issue tracking
- **Security**: Type-safe API integration and error boundaries
- **Scalability**: Component-based architecture for future expansion

## 🏗️ Technical Architecture

### **Modern Tech Stack**
- **Next.js 14**: Latest App Router with TypeScript
- **React Query**: Professional API state management
- **Tailwind CSS**: Utility-first CSS with custom design system
- **WebSocket Integration**: Real-time communication with FastAPI backend
- **Production Ready**: Error boundaries, monitoring, and performance optimization

### **Design System**
- **Professional Color Scheme**: Red/black enterprise branding
- **Responsive Layout**: Mobile-first design with desktop optimization
- **Accessibility**: WCAG compliance and keyboard navigation
- **Component Library**: Reusable, tested UI components

## 🚦 Quick Start

### Prerequisites
- Node.js 18+ 
- npm 8+
- Existing FIAE FastAPI backend running

### Installation & Deployment

1. **Automated Deployment** (Recommended):
```bash
# From project root directory
scripts\build-and-deploy.bat
```

2. **Manual Development Setup**:
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

3. **Production Build**:
```bash
# Build for production
npm run build
npm run export

# Deploy to FastAPI static folder
npm run deploy
```

### Access the Application
- **Production**: http://localhost:8000/ (via FastAPI)
- **Development**: http://localhost:3000/ (Next.js dev server)
- **Direct Access**: http://localhost:8000/static/dist/

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx         # Root layout with providers
│   │   └── page.tsx           # Main dashboard page
│   ├── components/            # React components
│   │   ├── dashboard/         # Dashboard components
│   │   ├── agents/           # Agent workflow display
│   │   ├── processing/       # Processing queue management
│   │   ├── monitoring/       # System health monitoring
│   │   ├── alerts/           # Real-time alerts
│   │   ├── layout/           # Layout components
│   │   └── providers/        # Context providers
│   ├── hooks/                # Custom React hooks
│   │   ├── useApi.ts         # API integration hooks
│   │   └── useWebSocket.ts   # WebSocket hooks
│   ├── services/             # Service layer
│   │   ├── api-client.ts     # FastAPI integration
│   │   └── websocket.ts      # WebSocket service
│   ├── types/                # TypeScript definitions
│   │   └── index.ts          # System type definitions
│   └── styles/               # Global styles
│       └── globals.css       # Tailwind + custom styles
├── public/                   # Static assets
├── package.json             # Dependencies and scripts
├── next.config.js          # Next.js configuration
├── tailwind.config.js      # Design system configuration
└── tsconfig.json           # TypeScript configuration
```

## 🔌 API Integration

### **FastAPI Backend Integration**
The frontend seamlessly integrates with your existing FastAPI backend:

- **39+ API Endpoints**: Full integration with all existing endpoints
- **WebSocket Support**: Real-time updates via `/ws` endpoint
- **Authentication**: Token-based security (ready for implementation)
- **Error Handling**: Comprehensive error boundaries and retry logic

### **Key API Integrations**
```typescript
// System Health
GET /health
GET /monitoring/health
GET /monitoring/metrics

// Agent Management  
GET /crewai/status
POST /crewai/run-workflow
POST /crewai/run-single-agent/{type}

// Document Processing
POST /process-comprehensive-batch
GET /batch-status
POST /process-document
GET /discover-documents

// RAG System
GET /rag/status  
POST /rag/reset

// Human-in-the-Loop
GET /hitl/pending-approvals
POST /hitl/approve/{id}
POST /hitl/reject/{id}
```

## 🎨 Customization

### **Branding & Colors**
Edit `tailwind.config.js` to customize the design system:
```javascript
colors: {
  primary: '#dc2626',    // Red (customizable)
  secondary: '#1f2937',  // Black/Gray (customizable)
  // ... other colors
}
```

### **Layout & Components**
- Modify `src/components/` for UI changes
- Update `src/app/layout.tsx` for global layout
- Customize `src/styles/globals.css` for styling

### **API Configuration**
Update `src/services/api-client.ts`:
```typescript
baseURL: process.env.BACKEND_URL || 'http://localhost:8000'
```

## 📊 Monitoring & Analytics

### **Real-time Features**
- **WebSocket Integration**: Live agent status updates
- **Performance Metrics**: CPU, memory, response time monitoring
- **Alert System**: Real-time notifications and issue tracking
- **Processing Queue**: Live document processing status

### **Business Intelligence**
- **Quality Analytics**: Content quality trends and predictions
- **Performance Insights**: Processing efficiency and bottlenecks
- **Cost Tracking**: Resource utilization and budget monitoring
- **Success Metrics**: Completion rates and error tracking

## 🚀 Production Deployment

### **Performance Optimization**
- **Code Splitting**: Automatic route-based splitting
- **Asset Optimization**: Image and font optimization
- **Caching Strategy**: React Query with stale-while-revalidate
- **Bundle Analysis**: Webpack bundle analyzer integration

### **Security Features**
- **Type Safety**: Full TypeScript coverage
- **Input Validation**: Zod schema validation
- **Error Boundaries**: Graceful error handling
- **CORS Configuration**: Secure cross-origin requests

### **Monitoring & Debugging**
- **Development Tools**: React Query DevTools
- **Error Tracking**: Console logging and error boundaries
- **Performance Monitoring**: Core Web Vitals tracking
- **Debugging**: Source maps and development tools

## 🤝 Integration with Existing System

### **Zero Disruption**
- **Backward Compatible**: All existing APIs preserved
- **Gradual Migration**: Can run alongside current HTML interface
- **Data Compatibility**: Works with existing Google Drive/Sheets integration
- **Service Integration**: Seamless integration with RAG, CrewAI, LangGraph

### **Enhanced Capabilities**
- **Real-time Updates**: WebSocket integration for live data
- **Professional UI**: Enterprise-grade user experience
- **Better Monitoring**: Comprehensive system observability
- **Client Ready**: Professional presentation for client demos

## 📚 Documentation

### **Component Documentation**
Each component includes comprehensive JSDoc comments and TypeScript definitions.

### **API Documentation** 
FastAPI automatically generates API documentation at `/docs`

### **Type Safety**
Full TypeScript coverage ensures type safety across the entire application.

## 🛠️ Development

### **Development Commands**
```bash
npm run dev          # Start development server
npm run build        # Build for production  
npm run lint         # Run ESLint
npm run type-check   # TypeScript checking
npm run export       # Export static files
```

### **Code Quality**
- **ESLint**: Code linting and formatting
- **TypeScript**: Type checking and IntelliSense  
- **Prettier**: Code formatting (configured)
- **Husky**: Git hooks for quality checks

## 🎯 Next Steps

1. **Start Backend**: `python -m uvicorn app.main:app --reload`
2. **Deploy Frontend**: Run `scripts\build-and-deploy.bat`
3. **Access Dashboard**: Navigate to `http://localhost:8000/`
4. **Explore Features**: Use the professional dashboard interface
5. **Customize**: Adapt branding and features for your needs

---

**🎉 Congratulations! You now have a production-ready, enterprise-grade UI for your FIAE Agentic AI System.**

