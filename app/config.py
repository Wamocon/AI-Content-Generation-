"""
Configuration management for the AI-powered content creation factory.
Uses Pydantic settings for type-safe configuration with environment variables.
"""

from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", description="API host address")
    api_port: int = Field(default=8000, description="API port")
    api_title: str = Field(default="AI Content Factory", description="API title")
    api_version: str = Field(default="1.0.0", description="API version")
    
    # Google Cloud Configuration
    google_project_id: str = Field(default="wmc-automation-agents", description="Google Cloud Project ID")
    google_credentials_path: Optional[str] = Field(default="credentials/wmc-automation-agents-e6ce75b3daa2.json", description="Path to Google Cloud credentials JSON")
    google_drive_folder_id: str = Field(default="1j41S_PjWV84_NNjAeX9kzdSfkq1nvkQv", description="Google Drive main project folder ID")
    google_drive_content_source_folder_id: str = Field(default="1YtN3_CftdJGgK9DFGLSMIky7PbYfFsX5", description="Google Drive folder ID for source documents")
    google_drive_review_folder_id: str = Field(default="1aUwEuIcny7dyLctF-6YFQ28lJkz2PTyK", description="Google Drive folder ID for review documents")
    google_drive_done_folder_id: str = Field(default="1yG_8-wBK1wfrEjzs5J_rKRRaHBpOFPoK", description="Google Drive folder ID for completed content")
    google_sheets_id: str = Field(default="1d87xmQNbWlNwtvRfhaWLSk2FkfTRVadKm94-ppaASbw", description="Google Sheets ID for job tracking")
    
    # AI Model Configuration - Gemini 2.5 Pro (Latest Production Model)
    gemini_model_name: str = Field(default="gemini-2.5-pro", description="Gemini 2.5 Pro - Latest production model with enhanced capabilities")
    gemini_model_fallback: str = Field(default="gemini-2.5-flash", description="Gemini 2.5 Flash - Fast fallback model for high-volume processing")
    gemini_model_temperature: float = Field(default=0.7, description="Gemini model temperature for content generation")
    gemini_model_top_p: float = Field(default=0.9, description="Gemini model top_p for content generation")
    gemini_api_key: str = Field(default="your-gemini-api-key", description="Gemini API key")
    imagen_model_name: str = Field(default="imagegeneration@006", description="Imagen 2 model name")
    
    # Gamma AI Configuration
    gamma_api_key: str = Field(default="your-gamma-api-key", description="Gamma AI API key from Pro account")
    gamma_api_url: str = Field(default="https://api.gamma.app", description="Gamma AI API base URL")
    gamma_theme_name: str = Field(default="WMC", description="WMC custom theme for all presentations")
    gamma_export_format: str = Field(default="pptx", description="Gamma export format")
    gamma_rate_limit: int = Field(default=50, description="Gamma API rate limit per hour")
    gamma_poll_interval: int = Field(default=5, description="Gamma API polling interval in seconds")
    gamma_max_poll_attempts: int = Field(default=60, description="Gamma API max polling attempts (5 min timeout)")
    
    # Google Services Configuration
    google_application_credentials_json: Optional[str] = Field(default="credentials/wmc-automation-agents-e6ce75b3daa2.json", description="Google service account JSON credentials file path or JSON string")
    
    # Personal Google Account Configuration (ONLY)
    personal_google_account_enabled: bool = Field(default=True, description="Enable personal Google account for Google Drive access")
    personal_google_credentials_file: str = Field(default="personal_credentials.json", description="OAuth2 credentials file for personal Google account")
    personal_google_token_file: str = Field(default="personal_google_token.pickle", description="OAuth2 token file for personal Google account")
    use_service_account_fallback: bool = Field(default=False, description="Disable service account fallback - use only personal account")
    google_drive_api_version: str = Field(default="v3", description="Google Drive API version")
    google_sheets_api_version: str = Field(default="v4", description="Google Sheets API version")
    google_docs_api_version: str = Field(default="v1", description="Google Docs API version")
    
    # ElevenLabs Configuration
    elevenlabs_api_key: str = Field(default="your-elevenlabs-api-key", description="ElevenLabs API key")
    elevenlabs_voice_id: str = Field(default="21m00Tcm4TlvDq8ikWAM", description="ElevenLabs voice ID")
    
    # File Processing Configuration
    max_file_size_mb: int = Field(default=100, description="Maximum file size in MB (increased for large documents)")
    supported_file_types: str = Field(default=".docx,.pdf,.txt", description="Supported file types (comma-separated)")
    temp_dir: str = Field(default="/tmp", description="Temporary directory for file processing")
    
    # Large Document Processing
    max_document_words: int = Field(default=50000, description="Maximum document words to process")
    chunk_size: int = Field(default=10000, description="Chunk size for processing large documents")
    enable_chunking: bool = Field(default=True, description="Enable chunking for very large documents")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        description="Log format string"
    )
    
    # Retry Configuration
    max_retries: int = Field(default=3, description="Maximum number of retries for API calls")
    retry_delay: float = Field(default=1.0, description="Initial retry delay in seconds")
    retry_backoff_factor: float = Field(default=2.0, description="Retry backoff factor")
    
    # Language Configuration
    default_language: str = Field(default="de", description="Default language for content generation (de = German)")
    output_language: str = Field(default="de", description="Output language for all generated content")
    
    # Professional Production Configuration
    enable_monitoring: bool = Field(default=True, description="Enable professional monitoring and logging")
    enable_audit_logs: bool = Field(default=True, description="Enable audit logging for security")
    enable_access_logs: bool = Field(default=True, description="Enable access logging")
    enable_data_logs: bool = Field(default=True, description="Enable data processing logs")
    
    # Scalability Configuration
    max_concurrent_jobs: int = Field(default=5, description="Maximum concurrent processing jobs")
    queue_size: int = Field(default=100, description="Maximum queue size for pending jobs")
    timeout_seconds: int = Field(default=300, description="Timeout for job processing in seconds")
    
    # Cost Control Configuration
    budget_limit: float = Field(default=10.0, description="Monthly budget limit in EUR")
    budget_currency: str = Field(default="EUR", description="Budget currency")
    cost_alert_threshold: float = Field(default=8.0, description="Cost alert threshold (80% of budget)")
    auto_stop_services: bool = Field(default=True, description="Automatically stop services if budget exceeded")
    
    # Performance Configuration
    cache_ttl: int = Field(default=3600, description="Cache time-to-live in seconds")
    rate_limit_per_minute: int = Field(default=60, description="Rate limit per minute")
    enable_compression: bool = Field(default=True, description="Enable response compression")
    
    # n8n Integration Configuration (BACKUP - Use CrewAI for workflow automation)
    n8n_user: str = Field(default="", description="n8n username (deprecated - use CrewAI)")
    n8n_password: str = Field(default="", description="n8n password (deprecated - use CrewAI)")
    n8n_encryption_key: str = Field(default="", description="n8n encryption key (deprecated - use CrewAI)")
    n8n_postgres_password: str = Field(default="", description="n8n PostgreSQL password (deprecated - use CrewAI)")
    n8n_url: str = Field(default="http://localhost:5678", description="n8n URL (deprecated - use CrewAI)")
    ai_content_factory_url: str = Field(default="http://localhost:8000", description="AI Content Factory URL")
    
    # CrewAI Orchestration Configuration (RECOMMENDED)
    crewai_enabled: bool = Field(default=True, description="Enable CrewAI multi-agent workflow orchestration")
    crewai_verbose: bool = Field(default=True, description="Enable verbose logging for CrewAI agents")
    crewai_memory_enabled: bool = Field(default=True, description="Enable CrewAI memory for agent learning")
    openai_api_key: str = Field(default="", description="OpenAI API key for CrewAI embeddings (optional)")
    crewai_max_agents: int = Field(default=4, description="Maximum number of CrewAI agents")
    crewai_timeout_seconds: int = Field(default=4800, description="CrewAI workflow timeout in seconds")
    
    # LangGraph Orchestration Configuration
    langgraph_enabled: bool = Field(default=True, description="Enable LangGraph workflow orchestration")
    langgraph_timeout_seconds: int = Field(default=600, description="LangGraph workflow timeout in seconds")
    langgraph_max_iterations: int = Field(default=10, description="Maximum iterations for LangGraph workflows")
    langgraph_max_retries: int = Field(default=3, description="Maximum retries for LangGraph operations")
    
    # Advanced RAG Configuration
    rag_chunk_size: int = Field(default=512, description="RAG document chunk size for semantic processing")
    rag_chunk_overlap: int = Field(default=50, description="RAG chunk overlap for context preservation")
    rag_embedding_model: str = Field(default="all-mpnet-base-v2", description="Advanced embedding model for better semantic understanding")
    rag_quality_threshold: float = Field(default=0.3, description="Minimum relevance score for RAG retrieval")
    rag_max_retrieval_docs: int = Field(default=10, description="Maximum documents to retrieve for context")
    
    # Vector Database Optimization
    chromadb_space: str = Field(default="cosine", description="ChromaDB similarity space (cosine, l2, ip)")
    chromadb_anonymized_telemetry: bool = Field(default=False, description="Disable ChromaDB telemetry")
    
    # Performance Optimization
    max_concurrent_documents: int = Field(default=8, description="Maximum concurrent document processing")
    document_processing_timeout: int = Field(default=600, description="Document processing timeout in seconds")
    
    # Content Intelligence Settings
    content_intelligence_enabled: bool = Field(default=True, description="Enable content intelligence and pattern recognition")
    cross_document_learning: bool = Field(default=True, description="Enable cross-document learning and insights")
    predictive_quality_scoring: bool = Field(default=True, description="Enable predictive quality scoring")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Allow extra fields from environment


# Global settings instance
settings = Settings()
