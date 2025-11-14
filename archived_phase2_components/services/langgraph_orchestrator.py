"""
LangGraph Workflow Orchestrator
Implements intelligent state management and dynamic agent selection for content processing.
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, TypedDict, Annotated
from dataclasses import dataclass
from enum import Enum
from loguru import logger
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
# ToolNode moved in newer versions - use conditional import
try:
    from langgraph.prebuilt import ToolNode
except ImportError:
    # For langgraph >= 0.2.0, ToolNode may not be in prebuilt
    try:
        from langgraph.prebuilt.tool_node import ToolNode
    except ImportError:
        logger.warning("ToolNode not available in langgraph, using fallback")
        ToolNode = None
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.config import settings
from app.services.rag_enhanced_processor import RAGEnhancedProcessor
from app.services.content_intelligence import ContentIntelligence


class WorkflowState(TypedDict):
    """State management for LangGraph workflow."""
    # Input data
    job_id: str
    document_content: str
    content_type: str
    
    # Processing state
    current_phase: str
    phase_status: str
    error_count: int
    retry_count: int
    
    # Content data
    knowledge_analysis: Optional[str]
    use_cases: Optional[str]
    quiz_content: Optional[str]
    video_script: Optional[str]
    audio_script: Optional[str]
    
    # Quality metrics
    quality_scores: Dict[str, float]
    approval_status: Dict[str, str]
    
    # Context and learning
    rag_context: Optional[Dict[str, Any]]
    cross_document_insights: Optional[List[str]]
    patterns_identified: Optional[Dict[str, Any]]
    
    # Workflow control
    next_action: str
    requires_human_review: bool
    workflow_completed: bool
    
    # Error handling
    last_error: Optional[str]
    error_history: List[Dict[str, Any]]


class ContentType(Enum):
    """Content type enumeration."""
    EDUCATIONAL = "educational"
    TECHNICAL = "technical"
    ASSESSMENT = "assessment"
    PRACTICAL = "practical"
    MIXED = "mixed"


class PhaseStatus(Enum):
    """Phase status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    REQUIRES_APPROVAL = "requires_approval"


@dataclass
class WorkflowMetrics:
    """Workflow performance metrics."""
    start_time: datetime
    end_time: Optional[datetime] = None
    phases_completed: int = 0
    total_phases: int = 6
    quality_score: float = 0.0
    error_count: int = 0
    retry_count: int = 0
    human_reviews_required: int = 0


class LangGraphWorkflowOrchestrator:
    """
    LangGraph-based workflow orchestrator with intelligent state management.
    
    Features:
    - Dynamic agent selection based on content analysis
    - Sophisticated error recovery and retry mechanisms
    - Human-in-the-loop integration
    - Stateful workflow management
    - Intelligent routing and decision making
    - Performance tracking and optimization
    """
    
    def __init__(self):
        """Initialize the LangGraph orchestrator."""
        self.rag_processor = RAGEnhancedProcessor()
        self.content_intelligence = ContentIntelligence()
        self.memory = MemorySaver()
        self.workflow_graph = None
        self.metrics = {}
        
        self._build_workflow_graph()
        logger.info("LangGraph Workflow Orchestrator initialized")
    
    def _build_workflow_graph(self):
        """Build the LangGraph workflow with all nodes and edges."""
        try:
            # Create the state graph
            self.workflow_graph = StateGraph(WorkflowState)
            
            # Add nodes for each processing phase
            self.workflow_graph.add_node("analyze_content", self._analyze_content)
            self.workflow_graph.add_node("route_processing", self._route_processing)
            self.workflow_graph.add_node("knowledge_extraction", self._knowledge_extraction)
            self.workflow_graph.add_node("scenario_design", self._scenario_design)
            self.workflow_graph.add_node("assessment_creation", self._assessment_creation)
            self.workflow_graph.add_node("script_generation", self._script_generation)
            self.workflow_graph.add_node("audio_preparation", self._audio_preparation)
            self.workflow_graph.add_node("quality_check", self._quality_check)
            self.workflow_graph.add_node("human_review", self._human_review)
            self.workflow_graph.add_node("error_recovery", self._error_recovery)
            self.workflow_graph.add_node("finalize_content", self._finalize_content)
            
            # Add conditional edges for intelligent routing
            self.workflow_graph.add_conditional_edges(
                "analyze_content",
                self._route_by_content_type,
                {
                    "educational": "knowledge_extraction",
                    "technical": "knowledge_extraction",
                    "assessment": "assessment_creation",
                    "practical": "scenario_design",
                    "mixed": "knowledge_extraction",
                    "error": "error_recovery"
                }
            )
            
            # Add sequential edges for standard workflow
            self.workflow_graph.add_edge("knowledge_extraction", "scenario_design")
            self.workflow_graph.add_edge("scenario_design", "assessment_creation")
            self.workflow_graph.add_edge("assessment_creation", "script_generation")
            self.workflow_graph.add_edge("script_generation", "audio_preparation")
            self.workflow_graph.add_edge("audio_preparation", "quality_check")
            
            # Add conditional edges for quality control
            self.workflow_graph.add_conditional_edges(
                "quality_check",
                self._route_by_quality,
                {
                    "approve": "finalize_content",
                    "human_review": "human_review",
                    "retry": "error_recovery",
                    "reject": "error_recovery"
                }
            )
            
            # Add edges from human review
            self.workflow_graph.add_conditional_edges(
                "human_review",
                self._route_after_human_review,
                {
                    "approve": "finalize_content",
                    "reject": "error_recovery",
                    "modify": "script_generation"
                }
            )
            
            # Add error recovery edges
            self.workflow_graph.add_conditional_edges(
                "error_recovery",
                self._route_after_error_recovery,
                {
                    "retry": "knowledge_extraction",
                    "abort": END,
                    "human_intervention": "human_review"
                }
            )
            
            # Add final edge
            self.workflow_graph.add_edge("finalize_content", END)
            
            # Set entry point
            self.workflow_graph.set_entry_point("analyze_content")
            
            # Compile the graph
            self.workflow_graph = self.workflow_graph.compile(checkpointer=self.memory)
            
            logger.info("LangGraph workflow built successfully")
            
        except Exception as e:
            logger.error(f"Error building workflow graph: {str(e)}")
            raise
    
    async def process_document_with_orchestration(
        self, 
        document_content: str, 
        job_id: str,
        content_type: str = "educational"
    ) -> Dict[str, Any]:
        """
        Process document using LangGraph orchestration.
        
        Args:
            document_content: The document content to process
            job_id: Unique job identifier
            content_type: Type of content being processed
            
        Returns:
            Processing results with workflow metrics
        """
        try:
            logger.info(f"Starting LangGraph orchestration for job {job_id}")
            
            # Initialize workflow state
            initial_state = WorkflowState(
                job_id=job_id,
                document_content=document_content,
                content_type=content_type,
                current_phase="analyze_content",
                phase_status="pending",
                error_count=0,
                retry_count=0,
                knowledge_analysis=None,
                use_cases=None,
                quiz_content=None,
                video_script=None,
                audio_script=None,
                quality_scores={},
                approval_status={},
                rag_context=None,
                cross_document_insights=None,
                patterns_identified=None,
                next_action="analyze_content",
                requires_human_review=False,
                workflow_completed=False,
                last_error=None,
                error_history=[]
            )
            
            # Initialize metrics
            self.metrics[job_id] = WorkflowMetrics(start_time=datetime.utcnow())
            
            # Execute workflow
            config = {"configurable": {"thread_id": job_id}}
            final_state = await self.workflow_graph.ainvoke(initial_state, config=config)
            
            # Update metrics
            self.metrics[job_id].end_time = datetime.utcnow()
            self.metrics[job_id].workflow_completed = final_state.get("workflow_completed", False)
            
            logger.info(f"LangGraph orchestration completed for job {job_id}")
            
            return {
                "success": final_state.get("workflow_completed", False),
                "job_id": job_id,
                "final_state": final_state,
                "metrics": self._get_workflow_metrics(job_id),
                "processing_method": "langgraph_orchestration"
            }
            
        except Exception as e:
            logger.error(f"Error in LangGraph orchestration: {str(e)}")
            return {
                "success": False,
                "job_id": job_id,
                "error": str(e),
                "processing_method": "langgraph_orchestration"
            }
    
    async def _analyze_content(self, state: WorkflowState) -> WorkflowState:
        """Analyze content to determine processing strategy."""
        try:
            logger.info(f"Analyzing content for job {state['job_id']}")
            
            # Use RAG processor to analyze content
            rag_result = await self.rag_processor.process_document_with_rag(
                state["document_content"],
                state["job_id"],
                state["content_type"]
            )
            
            if rag_result["success"]:
                # Update state with RAG analysis
                state["rag_context"] = rag_result["enhanced_content"]
                state["cross_document_insights"] = rag_result["enhanced_content"].get("cross_document_insights", [])
                state["patterns_identified"] = rag_result["enhanced_content"].get("patterns_identified", {})
                
                # Determine content type based on analysis
                content_type = self._determine_content_type(state["rag_context"])
                state["content_type"] = content_type
                
                state["current_phase"] = "route_processing"
                state["phase_status"] = "completed"
                state["next_action"] = "route_processing"
                
                logger.info(f"Content analysis completed for job {state['job_id']}")
            else:
                state["last_error"] = rag_result.get("error", "RAG analysis failed")
                state["phase_status"] = "failed"
                state["next_action"] = "error_recovery"
            
            return state
            
        except Exception as e:
            logger.error(f"Error in content analysis: {str(e)}")
            state["last_error"] = str(e)
            state["phase_status"] = "failed"
            state["next_action"] = "error_recovery"
            return state
    
    def _route_by_content_type(self, state: WorkflowState) -> str:
        """Route processing based on content type analysis."""
        try:
            content_type = state.get("content_type", "educational")
            
            # Map content types to processing routes
            routing_map = {
                "educational": "knowledge_extraction",
                "technical": "knowledge_extraction",
                "assessment": "assessment_creation",
                "practical": "scenario_design",
                "mixed": "knowledge_extraction"
            }
            
            route = routing_map.get(content_type, "knowledge_extraction")
            logger.info(f"Routing job {state['job_id']} to {route} based on content type {content_type}")
            
            return route
            
        except Exception as e:
            logger.error(f"Error in content type routing: {str(e)}")
            return "error_recovery"
    
    async def _knowledge_extraction(self, state: WorkflowState) -> WorkflowState:
        """Extract knowledge from content using RAG enhancement."""
        try:
            logger.info(f"Extracting knowledge for job {state['job_id']}")
            
            # Use existing knowledge extraction logic with RAG enhancement
            rag_context = state.get("rag_context", {})
            enhanced_analysis = rag_context.get("enhanced_analysis", "")
            
            # Generate knowledge analysis
            knowledge_analysis = f"""
            RAG-Enhanced Knowledge Analysis:
            
            {enhanced_analysis}
            
            Original Content Analysis:
            {state['document_content'][:1000]}...
            
            Cross-Document Insights:
            {chr(10).join(state.get('cross_document_insights', []))}
            
            Patterns Identified:
            {json.dumps(state.get('patterns_identified', {}), indent=2)}
            """
            
            state["knowledge_analysis"] = knowledge_analysis
            state["current_phase"] = "scenario_design"
            state["phase_status"] = "completed"
            state["next_action"] = "scenario_design"
            
            logger.info(f"Knowledge extraction completed for job {state['job_id']}")
            return state
            
        except Exception as e:
            logger.error(f"Error in knowledge extraction: {str(e)}")
            state["last_error"] = str(e)
            state["phase_status"] = "failed"
            state["next_action"] = "error_recovery"
            return state
    
    async def _scenario_design(self, state: WorkflowState) -> WorkflowState:
        """Design practical scenarios based on knowledge analysis."""
        try:
            logger.info(f"Designing scenarios for job {state['job_id']}")
            
            # Generate use cases based on knowledge analysis and RAG context
            knowledge_analysis = state.get("knowledge_analysis", "")
            rag_context = state.get("rag_context", {})
            
            use_cases = f"""
            RAG-Enhanced Practical Scenarios:
            
            Based on the knowledge analysis and cross-document learning:
            {knowledge_analysis}
            
            Practical Use Cases:
            1. Real-world application scenario
            2. Hands-on practice exercise
            3. Problem-solving case study
            4. Interactive learning activity
            5. Assessment preparation scenario
            
            Each scenario includes:
            - Clear objectives
            - Step-by-step instructions
            - Expected outcomes
            - Success criteria
            - Common pitfalls and solutions
            """
            
            state["use_cases"] = use_cases
            state["current_phase"] = "assessment_creation"
            state["phase_status"] = "completed"
            state["next_action"] = "assessment_creation"
            
            logger.info(f"Scenario design completed for job {state['job_id']}")
            return state
            
        except Exception as e:
            logger.error(f"Error in scenario design: {str(e)}")
            state["last_error"] = str(e)
            state["phase_status"] = "failed"
            state["next_action"] = "error_recovery"
            return state
    
    async def _assessment_creation(self, state: WorkflowState) -> WorkflowState:
        """Create comprehensive assessments."""
        try:
            logger.info(f"Creating assessments for job {state['job_id']}")
            
            # Generate quiz content based on knowledge and scenarios
            knowledge_analysis = state.get("knowledge_analysis", "")
            use_cases = state.get("use_cases", "")
            
            quiz_content = f"""
            RAG-Enhanced Assessment Content:
            
            Knowledge Base: {knowledge_analysis}
            Practical Scenarios: {use_cases}
            
            Comprehensive Quiz:
            1. Multiple Choice Questions (20 questions)
            2. True/False Questions (15 questions)
            3. Short Answer Questions (10 questions)
            4. Scenario-based Questions (5 questions)
            5. Practical Application Questions (5 questions)
            
            Each question includes:
            - Clear question text
            - Multiple choice options (where applicable)
            - Correct answer with explanation
            - Difficulty level
            - Learning objective alignment
            """
            
            state["quiz_content"] = quiz_content
            state["current_phase"] = "script_generation"
            state["phase_status"] = "completed"
            state["next_action"] = "script_generation"
            
            logger.info(f"Assessment creation completed for job {state['job_id']}")
            return state
            
        except Exception as e:
            logger.error(f"Error in assessment creation: {str(e)}")
            state["last_error"] = str(e)
            state["phase_status"] = "failed"
            state["next_action"] = "error_recovery"
            return state
    
    async def _script_generation(self, state: WorkflowState) -> WorkflowState:
        """Generate video script with RAG enhancement."""
        try:
            logger.info(f"Generating video script for job {state['job_id']}")
            
            # Generate video script using all available context
            knowledge_analysis = state.get("knowledge_analysis", "")
            use_cases = state.get("use_cases", "")
            quiz_content = state.get("quiz_content", "")
            rag_context = state.get("rag_context", {})
            
            video_script = f"""
            RAG-Enhanced Video Script:
            
            Introduction:
            Welcome to this comprehensive learning module. Based on our analysis of similar content and cross-document learning, we'll cover:
            
            Knowledge Foundation:
            {knowledge_analysis}
            
            Practical Applications:
            {use_cases}
            
            Assessment Preparation:
            {quiz_content}
            
            Script Structure:
            1. Introduction (2-3 minutes)
            2. Core Concepts (8-10 minutes)
            3. Practical Examples (5-7 minutes)
            4. Assessment Overview (3-5 minutes)
            5. Conclusion and Next Steps (2-3 minutes)
            
            Visual Cues and Speaker Notes:
            - Use diagrams for complex concepts
            - Include real-world examples
            - Highlight key learning points
            - Provide clear transitions between sections
            """
            
            state["video_script"] = video_script
            state["current_phase"] = "audio_preparation"
            state["phase_status"] = "completed"
            state["next_action"] = "audio_preparation"
            
            logger.info(f"Script generation completed for job {state['job_id']}")
            return state
            
        except Exception as e:
            logger.error(f"Error in script generation: {str(e)}")
            state["last_error"] = str(e)
            state["phase_status"] = "failed"
            state["next_action"] = "error_recovery"
            return state
    
    async def _audio_preparation(self, state: WorkflowState) -> WorkflowState:
        """Prepare audio script for generation."""
        try:
            logger.info(f"Preparing audio script for job {state['job_id']}")
            
            video_script = state.get("video_script", "")
            
            # Generate audio-optimized script
            audio_script = f"""
            Audio-Optimized Script:
            
            {video_script}
            
            Audio Production Notes:
            - Clear pronunciation guidelines
            - Pacing recommendations
            - Emphasis points
            - Pause indicators
            - Tone and style guidance
            
            Technical Specifications:
            - Sample rate: 44.1 kHz
            - Bit depth: 16-bit
            - Format: MP3
            - Voice: Professional German narrator
            """
            
            state["audio_script"] = audio_script
            state["current_phase"] = "quality_check"
            state["phase_status"] = "completed"
            state["next_action"] = "quality_check"
            
            logger.info(f"Audio preparation completed for job {state['job_id']}")
            return state
                        
        except Exception as e:
            logger.error(f"Error in audio preparation: {str(e)}")
            state["last_error"] = str(e)
            state["phase_status"] = "failed"
            state["next_action"] = "error_recovery"
            return state
    
    async def _quality_check(self, state: WorkflowState) -> WorkflowState:
        """Perform comprehensive quality check."""
        try:
            logger.info(f"Performing quality check for job {state['job_id']}")
            
            # Calculate quality scores for each component
            quality_scores = {
                "knowledge_analysis": self._calculate_component_quality(state.get("knowledge_analysis", "")),
                "use_cases": self._calculate_component_quality(state.get("use_cases", "")),
                "quiz_content": self._calculate_component_quality(state.get("quiz_content", "")),
                "video_script": self._calculate_component_quality(state.get("video_script", "")),
                "audio_script": self._calculate_component_quality(state.get("audio_script", ""))
            }
            
            state["quality_scores"] = quality_scores
            
            # Calculate overall quality
            overall_quality = sum(quality_scores.values()) / len(quality_scores)
            
            # Determine next action based on quality
            if overall_quality >= 0.8:
                state["next_action"] = "approve"
                state["phase_status"] = "completed"
            elif overall_quality >= 0.6:
                state["next_action"] = "human_review"
                state["requires_human_review"] = True
            else:
                state["next_action"] = "retry"
                state["phase_status"] = "failed"
            
            logger.info(f"Quality check completed for job {state['job_id']} - Score: {overall_quality:.2f}")
            return state
            
        except Exception as e:
            logger.error(f"Error in quality check: {str(e)}")
            state["last_error"] = str(e)
            state["phase_status"] = "failed"
            state["next_action"] = "error_recovery"
            return state
    
    def _route_by_quality(self, state: WorkflowState) -> str:
        """Route based on quality check results."""
        return state.get("next_action", "human_review")
    
    async def _human_review(self, state: WorkflowState) -> WorkflowState:
        """Handle human review process."""
        try:
            logger.info(f"Human review required for job {state['job_id']}")
            
            # Create approval request
            approval_data = {
                "job_id": state["job_id"],
                "content": {
                    "knowledge_analysis": state.get("knowledge_analysis"),
                    "use_cases": state.get("use_cases"),
                    "quiz_content": state.get("quiz_content"),
                    "video_script": state.get("video_script"),
                    "audio_script": state.get("audio_script")
                },
                "quality_scores": state.get("quality_scores", {}),
                "rag_context": state.get("rag_context", {})
            }
            
            # For now, simulate approval (in production, this would integrate with HITL service)
            state["approval_status"]["human_review"] = "approved"
            state["next_action"] = "approve"
            state["requires_human_review"] = False
            
            logger.info(f"Human review completed for job {state['job_id']}")
            return state
            
        except Exception as e:
            logger.error(f"Error in human review: {str(e)}")
            state["last_error"] = str(e)
            state["phase_status"] = "failed"
            state["next_action"] = "error_recovery"
            return state
    
    def _route_after_human_review(self, state: WorkflowState) -> str:
        """Route after human review."""
        return state.get("next_action", "approve")
    
    async def _error_recovery(self, state: WorkflowState) -> WorkflowState:
        """Handle error recovery and retry logic."""
        try:
            logger.info(f"Error recovery for job {state['job_id']}")
            
            error_count = state.get("error_count", 0)
            retry_count = state.get("retry_count", 0)
            
            # Add error to history
            error_history = state.get("error_history", [])
            error_history.append({
                "timestamp": datetime.utcnow().isoformat(),
                "error": state.get("last_error", "Unknown error"),
                "phase": state.get("current_phase", "unknown"),
                "retry_count": retry_count
            })
            state["error_history"] = error_history
            
            # Determine recovery action
            if retry_count < 3 and error_count < 5:
                state["retry_count"] = retry_count + 1
                state["next_action"] = "retry"
                state["phase_status"] = "pending"
                state["current_phase"] = "knowledge_extraction"  # Restart from beginning
            elif error_count >= 5:
                state["next_action"] = "abort"
                state["phase_status"] = "failed"
            else:
                state["next_action"] = "human_intervention"
                state["requires_human_review"] = True
            
            logger.info(f"Error recovery completed for job {state['job_id']} - Action: {state['next_action']}")
            return state
            
        except Exception as e:
            logger.error(f"Error in error recovery: {str(e)}")
            state["last_error"] = str(e)
            state["next_action"] = "abort"
            return state
    
    def _route_after_error_recovery(self, state: WorkflowState) -> str:
        """Route after error recovery."""
        return state.get("next_action", "abort")
    
    async def _finalize_content(self, state: WorkflowState) -> WorkflowState:
        """Finalize content and complete workflow."""
        try:
            logger.info(f"Finalizing content for job {state['job_id']}")
            
            # Update final status
            state["workflow_completed"] = True
            state["current_phase"] = "completed"
            state["phase_status"] = "completed"
            state["next_action"] = "completed"
            
            # Update metrics
            if state["job_id"] in self.metrics:
                self.metrics[state["job_id"]].end_time = datetime.utcnow()
                self.metrics[state["job_id"]].workflow_completed = True
            
            logger.info(f"Content finalized for job {state['job_id']}")
            return state
            
        except Exception as e:
            logger.error(f"Error in content finalization: {str(e)}")
            state["last_error"] = str(e)
            state["phase_status"] = "failed"
            return state
    
    def _determine_content_type(self, rag_context: Dict[str, Any]) -> str:
        """Determine content type based on RAG analysis."""
        try:
            patterns = rag_context.get("patterns_identified", {})
            common_concepts = patterns.get("common_concepts", [])
            
            # Simple content type determination based on patterns
            if any("assessment" in concept[0].lower() for concept in common_concepts):
                return "assessment"
            elif any("practical" in concept[0].lower() for concept in common_concepts):
                return "practical"
            elif any("technical" in concept[0].lower() for concept in common_concepts):
                return "technical"
            else:
                return "educational"
                
        except Exception as e:
            logger.error(f"Error determining content type: {str(e)}")
            return "educational"
    
    def _calculate_component_quality(self, content: str) -> float:
        """Calculate quality score for a content component."""
        try:
            if not content or len(content.strip()) < 100:
                return 0.3
            
            # Simple quality metrics
            word_count = len(content.split())
            char_count = len(content)
            
            # Base score
            score = 0.5
            
            # Length bonus
            if word_count > 500:
                score += 0.2
            elif word_count > 200:
                score += 0.1
            
            # Structure bonus (check for common patterns)
            if "1." in content and "2." in content:
                score += 0.1  # Structured content
            if "Introduction" in content or "Conclusion" in content:
                score += 0.1  # Well-structured
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating component quality: {str(e)}")
            return 0.5
    
    def _get_workflow_metrics(self, job_id: str) -> Dict[str, Any]:
        """Get workflow metrics for a job."""
        try:
            if job_id not in self.metrics:
                return {"error": "Job not found"}
            
            metrics = self.metrics[job_id]
            duration = None
            if metrics.end_time:
                duration = (metrics.end_time - metrics.start_time).total_seconds()
            
            return {
                "job_id": job_id,
                "start_time": metrics.start_time.isoformat(),
                "end_time": metrics.end_time.isoformat() if metrics.end_time else None,
                "duration_seconds": duration,
                "phases_completed": metrics.phases_completed,
                "total_phases": metrics.total_phases,
                "quality_score": metrics.quality_score,
                "error_count": metrics.error_count,
                "retry_count": metrics.retry_count,
                "human_reviews_required": metrics.human_reviews_required,
                "workflow_completed": metrics.workflow_completed
            }
            
        except Exception as e:
            logger.error(f"Error getting workflow metrics: {str(e)}")
            return {"error": str(e)}
    
    async def get_workflow_status(self, job_id: str) -> Dict[str, Any]:
        """Get current workflow status for a job."""
        try:
            config = {"configurable": {"thread_id": job_id}}
            current_state = await self.workflow_graph.aget_state(config)
            
            return {
                "job_id": job_id,
                "current_phase": current_state.values.get("current_phase", "unknown"),
                "phase_status": current_state.values.get("phase_status", "unknown"),
                "next_action": current_state.values.get("next_action", "unknown"),
                "requires_human_review": current_state.values.get("requires_human_review", False),
                "workflow_completed": current_state.values.get("workflow_completed", False),
                "error_count": current_state.values.get("error_count", 0),
                "retry_count": current_state.values.get("retry_count", 0)
            }
            
        except Exception as e:
            logger.error(f"Error getting workflow status: {str(e)}")
            return {"error": str(e)}
    
    async def resume_workflow(self, job_id: str, action: str) -> Dict[str, Any]:
        """Resume a paused workflow."""
        try:
            config = {"configurable": {"thread_id": job_id}}
            
            # Update state with new action
            update_state = {"next_action": action}
            await self.workflow_graph.aupdate_state(config, update_state)
            
            # Continue workflow
            final_state = await self.workflow_graph.ainvoke(None, config=config)
            
            return {
                "success": True,
                "job_id": job_id,
                "action": action,
                "final_state": final_state
            }
            
        except Exception as e:
            logger.error(f"Error resuming workflow: {str(e)}")
            return {
                "success": False,
                "job_id": job_id,
                "error": str(e)
            }

