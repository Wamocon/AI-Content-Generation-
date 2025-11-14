"""
Simple Gemini Wrapper for Intelligent Content Generation
Optimized for direct prompt-based generation with chunking support
"""

import time
import asyncio
from typing import Optional
from loguru import logger
from app.services.gemini_ai_service import GeminiAIService, rate_limiter

class IntelligentGeminiService:
    """
    Simplified wrapper around GeminiAIService for intelligent content generation.
    Handles both single-pass and multi-pass generation based on content size.
    """
    
    def __init__(self):
        self.gemini_service = GeminiAIService()
    
    async def generate_from_prompt(
        self, 
        prompt: str, 
        content_type: str = "content",
        timeout: int = 120,
        max_retries: int = 3
    ) -> str:
        """
        Generate content from a direct prompt.
        Wrapper around the existing generate_content_with_retry method.
        
        Args:
            prompt: The complete prompt (including document context, instructions, etc.)
            content_type: Type of content being generated (for logging)
            timeout: Timeout in seconds
            max_retries: Maximum retry attempts
        
        Returns:
            Generated content as string
        """
        logger.info(f"[INTELLIGENT GEMINI] Generating {content_type}...")
        
        # The existing API expects: content_type, document_content, context_query
        # But actually only uses context_query (the prompt)
        # So we can pass the prompt as context_query
        result = self.gemini_service.generate_content_with_retry(
            content_type=content_type,
            document_content="",  # Not used by the actual implementation
            context_query=prompt,  # The actual prompt
            timeout=timeout,
            max_retries=max_retries
        )
        
        return result
    
    async def generate_with_chunking(
        self,
        prompt_template: str,
        document_content: str,
        analysis_data: dict,
        chunk_size: int = 6000,
        content_type: str = "content"
    ) -> str:
        """
        Generate content using chunking strategy for large documents.
        
        Strategy:
        1. If document < 10K chars: Single pass (fast)
        2. If document >= 10K chars: Multi-pass with chunk enhancement
        
        Args:
            prompt_template: Template with {doc_context} placeholder
            document_content: Full document content
            analysis_data: Dict with topics, requirements, etc.
            chunk_size: Size of chunks for multi-pass
            content_type: Type of content for logging
        
        Returns:
            Generated content (merged if multi-pass)
        """
        doc_length = len(document_content)
        
        if doc_length < 10000:
            # Single pass - simple and fast
            logger.info(f"[CHUNKING] Document small ({doc_length} chars), using single-pass generation")
            doc_context = document_content[:6000]  # Use first 6K chars
            prompt = prompt_template.format(doc_context=doc_context, **analysis_data)
            return await self.generate_from_prompt(prompt, content_type)
        
        else:
            # Multi-pass strategy
            logger.info(f"[CHUNKING] Document large ({doc_length} chars), using multi-pass generation")
            
            # Pass 1: Generate from summary + topics
            topics_summary = "\n".join([f"- {t}" for t in analysis_data.get('topics_list', [])])
            summary_context = f"""
DOCUMENT SUMMARY (First 3000 chars):
{document_content[:3000]}

KEY TOPICS IDENTIFIED:
{topics_summary}

DOCUMENT LENGTH: {doc_length} characters (large document)
"""
            
            prompt_pass1 = prompt_template.format(doc_context=summary_context, **analysis_data)
            logger.info("[CHUNKING] Pass 1: Generating from summary + topics...")
            result_pass1 = await self.generate_from_prompt(prompt_pass1, f"{content_type}_pass1", timeout=300)
            
            if not result_pass1 or len(result_pass1) < 500:
                logger.warning("[CHUNKING] Pass 1 failed, returning empty")
                return ""
            
            # Pass 2: Enhance with additional context from document chunks
            # Take middle and end sections for additional context
            middle_chunk = document_content[len(document_content)//3 : len(document_content)//3 + 2000]
            end_chunk = document_content[-2000:]
            
            enhancement_prompt = f"""
Based on the initial content generated, enhance it with additional details from these document sections:

MIDDLE SECTION:
{middle_chunk}

END SECTION:
{end_chunk}

INITIAL GENERATED CONTENT (to enhance):
{result_pass1[:2000]}...

TASK: Add 2-3 additional insights or details that weren't covered in the initial generation.
Keep the same structure, just add missing important details.
"""
            
            logger.info("[CHUNKING] Pass 2: Enhancing with additional context...")
            enhancement = await self.generate_from_prompt(enhancement_prompt, f"{content_type}_enhancement", timeout=90)
            
            # Merge: If enhancement successful, append it; otherwise return pass1
            if enhancement and len(enhancement) > 200:
                logger.info("[CHUNKING] Multi-pass successful, merging results")
                return f"{result_pass1}\n\n{enhancement}"
            else:
                logger.info("[CHUNKING] Enhancement failed, using pass1 only")
                return result_pass1
    
    def chunk_document(self, content: str, chunk_size: int = 2000, overlap: int = 400) -> list:
        """
        Chunk document intelligently at sentence boundaries.
        Borrowed from RAG processor but without storage.
        
        Args:
            content: Document content to chunk
            chunk_size: Target size of each chunk
            overlap: Overlap between chunks for context
        
        Returns:
            List of text chunks
        """
        if len(content) <= chunk_size:
            return [content]
        
        chunks = []
        start = 0
        
        while start < len(content):
            end = start + chunk_size
            
            # Try to break at sentence boundary
            if end < len(content):
                # Look for sentence endings within the last 200 characters
                search_start = max(start + chunk_size - 200, start)
                for i in range(end - 1, search_start, -1):
                    if content[i] in '.!?\n':
                        end = i + 1
                        break
            
            chunk = content[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
            if start >= len(content):
                break
        
        logger.info(f"[CHUNKING] Split {len(content)} chars into {len(chunks)} chunks")
        return chunks
