"""
Gemini AI Service for FIAE AI Content Factory - Robust Error Handling
"""

import os
import time
import asyncio
from typing import Dict, Any, Optional
from collections import deque
from loguru import logger
from app.config import settings

# Global rate limiter
class RateLimiter:
    def __init__(self, max_calls: int = 14, period: int = 60):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()
        # Remove calls older than period
        while self.calls and self.calls[0] < now - self.period:
            self.calls.popleft()
        
        # If we're at the limit, wait
        if len(self.calls) >= self.max_calls:
            sleep_time = self.period - (now - self.calls[0])
            if sleep_time > 0:
                logger.info(f"[RATE LIMIT] Waiting {sleep_time:.1f}s to avoid rate limit...")
                time.sleep(sleep_time)
        
        self.calls.append(time.time())

# Global rate limiter instance
rate_limiter = RateLimiter(max_calls=14, period=60)  # 14 calls per 60 seconds (safer than 15)

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("Google Generative AI not available - install google-generativeai")


class GeminiAIService:
    """Gemini AI service with robust error handling and retry logic"""
    
    def __init__(self):
        self.model = None
        self.initialized = False
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize Gemini AI service with fallback models"""
        if not GEMINI_AVAILABLE:
            logger.error("Gemini AI not available")
            return
            
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                
                # Try primary model first, then fallback
                try:
                    self.model = genai.GenerativeModel(settings.gemini_model_name)
                    logger.info(f"[OK] Gemini AI service initialized with {settings.gemini_model_name}")
                except Exception as e:
                    logger.warning(f"Primary model {settings.gemini_model_name} failed, trying fallback: {e}")
                    try:
                        self.model = genai.GenerativeModel(settings.gemini_model_fallback)
                        logger.info(f"[OK] Gemini AI service initialized with fallback {settings.gemini_model_fallback}")
                    except Exception as e2:
                        logger.error(f"Both models failed: {e2}")
                        return
                
                self.initialized = True
            else:
                logger.warning("GEMINI_API_KEY not found in environment")
        except Exception as e:
            logger.error(f"Gemini initialization failed: {e}")
    
    def generate_content_with_retry(self, content_type: str, document_content: str, context_query: str, timeout: int = 60, max_retries: int = 4) -> str:
        """
        Generate content with robust retry logic and timeout handling
        PRODUCTION FIX: Reduced prompt size, increased retries, better error handling
        """
        if not self.initialized or not self.model:
            return f"Error: Gemini service not initialized"
        
        # CRITICAL FIX: Limit document content size to prevent timeouts
        MAX_CONTENT_LENGTH = 30000  # 30k characters max
        if len(context_query) > MAX_CONTENT_LENGTH:
            logger.warning(f"[GEMINI] Prompt too large ({len(context_query)} chars), truncating to {MAX_CONTENT_LENGTH}")
            context_query = context_query[:MAX_CONTENT_LENGTH] + "\n\n[... Dokument gekürzt für bessere Verarbeitung ...]"
        
        for attempt in range(max_retries):
            try:
                # Apply rate limiting
                rate_limiter.wait_if_needed()
                
                logger.info(f"[GEMINI] Generating {content_type} (attempt {attempt + 1}/{max_retries})")
                
                # Create generation config with timeout
                generation_config = genai.types.GenerationConfig(
                    temperature=settings.gemini_model_temperature,
                    top_p=settings.gemini_model_top_p,
                    max_output_tokens=8192,  # Increased for better content
                    candidate_count=1
                )
                
                # Create safety settings
                safety_settings = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                ]
                
                # Generate content with explicit timeout
                start_time = time.time()
                
                # Use timeout parameter passed to function
                import asyncio
                import concurrent.futures
                
                # Run synchronous generate_content with timeout
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        self.model.generate_content,
                        context_query,
                        generation_config=generation_config,
                        safety_settings=safety_settings
                    )
                    try:
                        response = future.result(timeout=timeout)
                    except concurrent.futures.TimeoutError:
                        future.cancel()
                        raise Exception(f"504 The request timed out after {timeout}s. Please try again.")
                
                generation_time = time.time() - start_time
                
                if response and response.text:
                    content = response.text.strip()
                    
                    # Validate content quality
                    if self._validate_content_quality(content, content_type):
                        logger.info(f"[GEMINI] Successfully generated {content_type} ({len(content)} chars, {generation_time:.1f}s)")
                        return content
                    else:
                        logger.warning(f"[GEMINI] Low quality content for {content_type}, retrying...")
                        if attempt < max_retries - 1:
                            time.sleep(5)
                            continue
                        else:
                            logger.error(f"[GEMINI] Failed to generate quality {content_type} after {max_retries} attempts")
                            return f"Error: Unable to generate quality {content_type} content"
                else:
                    logger.warning(f"[GEMINI] Empty response for {content_type}, retrying...")
                    if attempt < max_retries - 1:
                        time.sleep(5)
                        continue
                    else:
                        return f"Error: Empty response for {content_type}"
                        
            except Exception as e:
                error_msg = str(e)
                logger.error(f"[GEMINI] Error generating {content_type} (attempt {attempt + 1}): {error_msg}")
                
                # Handle specific error types with better rate limiting
                if "503" in error_msg or "overloaded" in error_msg.lower():
                    wait_time = min(60, 20 * (attempt + 1))  # Longer exponential backoff
                    logger.warning(f"[GEMINI] Model overloaded, waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                elif "504" in error_msg or "timeout" in error_msg.lower() or "deadline" in error_msg.lower():
                    wait_time = min(40, 15 * (attempt + 1))
                    logger.warning(f"[GEMINI] Timeout error, waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                elif "429" in error_msg or "rate limit" in error_msg.lower():
                    wait_time = 30  # Fixed wait for rate limits
                    logger.warning(f"[GEMINI] Rate limit exceeded, waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                elif attempt < max_retries - 1:
                    time.sleep(10)
                    continue
                else:
                    logger.error(f"[GEMINI] All attempts failed for {content_type}")
                    return f"Error generating {content_type}: {error_msg}"
        
        return f"Error: Failed to generate {content_type} after {max_retries} attempts"
    
    def _validate_content_quality(self, content: str, content_type: str) -> bool:
        """Validate content quality and completeness"""
        if not content or len(content.strip()) < 100:
            return False
        
        # Check for error messages
        error_indicators = [
            "error generating",
            "timeout exceeded", 
            "model is overloaded",
            "503",
            "504",
            "deadline exceeded",
            "service unavailable"
        ]
        
        content_lower = content.lower()
        for indicator in error_indicators:
            if indicator in content_lower:
                logger.warning(f"[GEMINI] Content contains error indicator: {indicator}")
                return False
        
        # Content type specific validation
        if content_type == "use cases":
            return any(keyword in content_lower for keyword in ["anwendungsfall", "beispiel", "praxis", "aufgabe"])
        elif content_type == "quiz":
            return any(keyword in content_lower for keyword in ["frage", "quiz", "antwort", "richtig", "falsch"])
        elif content_type == "trainer script":
            return any(keyword in content_lower for keyword in ["slide", "präsentation", "trainer", "theorie"])
        
        return True
    
    def generate_content(self, content_type: str, document_content: str, context_query: str) -> str:
        """Legacy method for backward compatibility"""
        return self.generate_content_with_retry(content_type, document_content, context_query)