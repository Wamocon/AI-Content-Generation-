"""
🧠 INTELLIGENT DOCUMENT ANALYZER
==================================
Dynamically analyzes source documents to determine optimal content generation strategy.
Ensures 100% topic coverage across all output types (use cases, quiz, trainer script, PowerPoint).

This module is the BRAIN of the two-phase automation system.
"""

import re
import logging
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field
import asyncio

logger = logging.getLogger(__name__)


@dataclass
class Topic:
    """Represents a single topic extracted from the document"""
    title: str
    subtopics: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    complexity: str = "medium"  # low, medium, high
    estimated_content_depth: int = 1  # 1-5 scale
    context: str = ""  # Surrounding context from document


@dataclass
class ContentRequirements:
    """Dynamic content requirements based on document analysis"""
    use_cases_count: int
    use_cases_topics: List[str]
    quiz_questions_count: int
    quiz_distribution: Dict[str, int]  # easy, medium, hard counts
    trainer_slides_count: int
    trainer_slide_topics: List[str]
    powerpoint_slides_count: int
    powerpoint_structure: List[Dict[str, Any]]
    estimated_total_pages: int
    coverage_map: Dict[str, List[str]]  # topic -> [use_case_id, quiz_id, slide_id]


@dataclass
class AnalysisResult:
    """Complete analysis result for a document"""
    document_name: str
    total_chars: int
    total_words: int
    topics: List[Topic]
    main_themes: List[str]
    complexity_score: float  # 0-10
    technical_depth: str  # conceptual, intermediate, advanced
    content_requirements: ContentRequirements
    analysis_confidence: float  # 0-1
    recommendations: List[str]


class DocumentAnalyzer:
    """
    🧠 Intelligent analyzer that determines optimal content generation strategy
    
    Key Features:
    - Extracts all topics, subtopics, and key concepts
    - Calculates complexity and depth scores
    - Determines dynamic counts for all content types
    - Ensures 100% topic coverage
    - Provides content generation recommendations
    """
    
    def __init__(self, gemini_service=None):
        self.gemini_service = gemini_service
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def analyze_document(
        self, 
        document_content: str, 
        document_name: str,
        use_ai: bool = True
    ) -> AnalysisResult:
        """
        Perform comprehensive analysis of document to determine content requirements
        
        Args:
            document_content: Full text content of the document
            document_name: Name of the document
            use_ai: Whether to use Gemini AI for enhanced analysis (recommended)
        
        Returns:
            AnalysisResult with complete analysis and content requirements
        """
        self.logger.info(f"🧠 Starting intelligent analysis of '{document_name}'")
        
        # Step 1: Basic statistics
        total_chars = len(document_content)
        total_words = len(document_content.split())
        
        self.logger.info(f"📊 Document stats: {total_words} words, {total_chars} chars")
        
        # Step 2: Extract topics (rule-based + AI-enhanced)
        if use_ai and self.gemini_service:
            topics = await self._extract_topics_with_ai(document_content, document_name)
        else:
            topics = self._extract_topics_rule_based(document_content)
        
        self.logger.info(f"📚 Extracted {len(topics)} main topics")
        
        # Step 3: Identify main themes and complexity
        main_themes = self._identify_main_themes(topics, document_content)
        complexity_score = self._calculate_complexity_score(document_content, topics)
        technical_depth = self._determine_technical_depth(complexity_score, topics)
        
        self.logger.info(f"🎯 Complexity: {complexity_score:.1f}/10, Depth: {technical_depth}")
        
        # Step 4: Calculate dynamic content requirements
        content_requirements = self._calculate_content_requirements(
            topics=topics,
            document_chars=total_chars,
            document_words=total_words,
            complexity_score=complexity_score,
            main_themes=main_themes
        )
        
        # Step 5: Generate recommendations
        recommendations = self._generate_recommendations(
            topics=topics,
            complexity_score=complexity_score,
            content_requirements=content_requirements
        )
        
        # Step 6: Calculate confidence score
        analysis_confidence = self._calculate_confidence(topics, document_content)
        
        result = AnalysisResult(
            document_name=document_name,
            total_chars=total_chars,
            total_words=total_words,
            topics=topics,
            main_themes=main_themes,
            complexity_score=complexity_score,
            technical_depth=technical_depth,
            content_requirements=content_requirements,
            analysis_confidence=analysis_confidence,
            recommendations=recommendations
        )
        
        self._log_analysis_summary(result)
        
        return result
    
    async def _extract_topics_with_ai(self, content: str, doc_name: str) -> List[Topic]:
        """Use Gemini AI to intelligently extract topics and subtopics"""
        self.logger.info("🤖 Using AI for topic extraction...")
        
        # Limit content to first 8000 chars for analysis
        analysis_content = content[:8000]
        
        prompt = f"""
Analysiere das folgende IT-Dokument und extrahiere ALLE wichtigen Themen, Unterthemen und Konzepte.

DOKUMENT: {doc_name}

INHALT:
{analysis_content}

AUFGABE:
1. Identifiziere ALLE Hauptthemen (Main Topics)
2. Für jedes Hauptthema: Liste alle Unterthemen auf
3. Für jedes Thema: Extrahiere wichtige Schlüsselwörter
4. Für jedes Thema: Bewerte die Komplexität (low/medium/high)
5. Für jedes Thema: Schätze die Tiefe ein (1-5 Skala)

ANTWORT im folgenden exakten Format (jedes Thema auf separaten Zeilen):

TOPIC: [Hauptthema-Titel]
SUBTOPICS: [Unterthema1] | [Unterthema2] | [Unterthema3]
KEYWORDS: [keyword1] | [keyword2] | [keyword3] | [keyword4] | [keyword5]
COMPLEXITY: [low/medium/high]
DEPTH: [1-5]
CONTEXT: [1-2 Sätze Kontext aus dem Dokument]
---

Sei SEHR gründlich. Identifiziere auch implizite Themen und Zusammenhänge.
"""
        
        try:
            response = self.gemini_service.generate_content_with_retry(
                content_type="topic_extraction",
                document_content=analysis_content,
                context_query=prompt,
                timeout=60,
                max_retries=2
            )
            
            if not response or len(response) < 100:
                self.logger.warning("⚠️ AI response too short, falling back to rule-based extraction")
                return self._extract_topics_rule_based(content)
            
            topics = self._parse_ai_topic_response(response)
            self.logger.info(f"✅ AI extracted {len(topics)} topics")
            return topics
            
        except Exception as e:
            self.logger.error(f"❌ AI topic extraction failed: {e}")
            self.logger.info("🔄 Falling back to rule-based extraction")
            return self._extract_topics_rule_based(content)
    
    def _parse_ai_topic_response(self, response: str) -> List[Topic]:
        """Parse Gemini AI response into Topic objects"""
        topics = []
        
        # Split by --- separator
        topic_blocks = response.split("---")
        
        for block in topic_blocks:
            if not block.strip():
                continue
            
            try:
                # Extract fields using regex
                topic_match = re.search(r'TOPIC:\s*(.+)', block)
                subtopics_match = re.search(r'SUBTOPICS:\s*(.+)', block)
                keywords_match = re.search(r'KEYWORDS:\s*(.+)', block)
                complexity_match = re.search(r'COMPLEXITY:\s*(\w+)', block)
                depth_match = re.search(r'DEPTH:\s*(\d+)', block)
                context_match = re.search(r'CONTEXT:\s*(.+)', block, re.DOTALL)
                
                if topic_match:
                    title = topic_match.group(1).strip()
                    subtopics = []
                    keywords = []
                    complexity = "medium"
                    depth = 3
                    context = ""
                    
                    if subtopics_match:
                        subtopics = [s.strip() for s in subtopics_match.group(1).split("|")]
                    
                    if keywords_match:
                        keywords = [k.strip() for k in keywords_match.group(1).split("|")]
                    
                    if complexity_match:
                        complexity = complexity_match.group(1).strip().lower()
                    
                    if depth_match:
                        depth = int(depth_match.group(1))
                    
                    if context_match:
                        context = context_match.group(1).strip()
                    
                    topic = Topic(
                        title=title,
                        subtopics=subtopics,
                        keywords=keywords,
                        complexity=complexity,
                        estimated_content_depth=depth,
                        context=context
                    )
                    topics.append(topic)
            
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to parse topic block: {e}")
                continue
        
        return topics
    
    def _extract_topics_rule_based(self, content: str) -> List[Topic]:
        """Fallback: Rule-based topic extraction using patterns and heuristics"""
        self.logger.info("📋 Using rule-based topic extraction...")
        
        topics = []
        
        # Pattern 1: Headers (common patterns: "1. Title", "## Title", "Title:", etc.)
        header_patterns = [
            r'^#+\s+(.+)$',  # Markdown headers
            r'^\d+\.\s+(.+)$',  # Numbered headers
            r'^[A-Z][A-Za-zäöüÄÖÜß\s]+:$',  # Capitalized lines ending with :
            r'^\*\*(.+)\*\*$',  # Bold text
        ]
        
        lines = content.split('\n')
        potential_topics = []
        
        for line in lines:
            line = line.strip()
            if not line or len(line) < 5 or len(line) > 100:
                continue
            
            for pattern in header_patterns:
                match = re.match(pattern, line, re.MULTILINE)
                if match:
                    title = match.group(1).strip() if match.groups() else line.strip()
                    potential_topics.append(title)
                    break
        
        # Pattern 2: Extract key noun phrases (simplified NLP)
        # Look for repeated capitalized terms
        capitalized_terms = re.findall(r'\b[A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+)*\b', content)
        term_frequency = {}
        for term in capitalized_terms:
            if len(term) > 3:  # Skip short terms
                term_frequency[term] = term_frequency.get(term, 0) + 1
        
        # Get most frequent terms as potential topics
        frequent_terms = sorted(term_frequency.items(), key=lambda x: x[1], reverse=True)[:15]
        potential_topics.extend([term for term, _ in frequent_terms])
        
        # Deduplicate and clean
        seen = set()
        unique_topics = []
        for topic in potential_topics:
            topic_clean = topic.lower().strip()
            if topic_clean not in seen and len(topic) > 5:
                seen.add(topic_clean)
                unique_topics.append(topic)
        
        # Create Topic objects
        for i, topic_title in enumerate(unique_topics[:20]):  # Max 20 topics
            # Estimate complexity based on length and technical terms
            tech_terms = len(re.findall(r'\b(?:API|System|Framework|Architektur|Protokoll|Datenbank)\b', topic_title, re.IGNORECASE))
            complexity = "high" if tech_terms > 0 else "medium" if len(topic_title) > 30 else "low"
            
            # Extract keywords from surrounding context
            keywords = self._extract_keywords_for_topic(content, topic_title)
            
            topic = Topic(
                title=topic_title,
                subtopics=[],
                keywords=keywords,
                complexity=complexity,
                estimated_content_depth=3,
                context=f"Found in document position {i+1}"
            )
            topics.append(topic)
        
        return topics
    
    def _extract_keywords_for_topic(self, content: str, topic_title: str) -> List[str]:
        """Extract relevant keywords for a topic from document"""
        # Find topic in content and extract surrounding words
        pattern = re.escape(topic_title)
        matches = list(re.finditer(pattern, content, re.IGNORECASE))
        
        keywords = set()
        for match in matches[:3]:  # First 3 occurrences
            start = max(0, match.start() - 200)
            end = min(len(content), match.end() + 200)
            context = content[start:end]
            
            # Extract capitalized terms and technical terms
            terms = re.findall(r'\b[A-ZÄÖÜ][a-zäöüß]{3,}\b', context)
            keywords.update(terms[:5])
        
        return list(keywords)[:8]
    
    def _identify_main_themes(self, topics: List[Topic], content: str) -> List[str]:
        """Identify overarching themes from topics"""
        # Group topics by similarity (simplified clustering)
        themes = []
        
        # Technical vs Conceptual
        technical_count = sum(1 for t in topics if t.complexity in ["medium", "high"])
        if technical_count > len(topics) * 0.5:
            themes.append("Technical Implementation")
        else:
            themes.append("Conceptual Understanding")
        
        # Check for common IT themes
        content_lower = content.lower()
        theme_keywords = {
            "Software Development": ["entwicklung", "software", "programmierung", "code"],
            "System Architecture": ["architektur", "system", "infrastruktur", "komponente"],
            "Database Management": ["datenbank", "sql", "daten", "speicher"],
            "Network & Security": ["netzwerk", "sicherheit", "protokoll", "firewall"],
            "Cloud & DevOps": ["cloud", "devops", "container", "kubernetes"],
            "AI & Machine Learning": ["künstliche intelligenz", "machine learning", "ai", "ki"],
        }
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                themes.append(theme)
        
        return themes[:5]  # Max 5 main themes
    
    def _calculate_complexity_score(self, content: str, topics: List[Topic]) -> float:
        """Calculate overall document complexity (0-10 scale)"""
        score = 5.0  # Base score
        
        # Factor 1: Topic complexity distribution
        complexity_scores = {"low": 1, "medium": 2, "high": 3}
        avg_topic_complexity = sum(complexity_scores[t.complexity] for t in topics) / len(topics) if topics else 2
        score += (avg_topic_complexity - 2) * 2  # Adjust by topic complexity
        
        # Factor 2: Technical terminology density
        tech_terms = len(re.findall(r'\b(?:API|Framework|Protokoll|Algorithmus|Architektur|Interface|Implementation|Konfiguration|System|Datenbank|Server|Client|Cache|Token|Session|Authentifizierung)\b', content, re.IGNORECASE))
        tech_density = tech_terms / (len(content.split()) + 1) * 1000
        score += min(tech_density / 2, 2)  # Max +2 points
        
        # Factor 3: Document length (longer = potentially more complex)
        if len(content) > 10000:
            score += 1
        if len(content) > 20000:
            score += 1
        
        # Factor 4: Topic count (more topics = more complex)
        if len(topics) > 10:
            score += 1
        if len(topics) > 20:
            score += 1
        
        # Clamp to 0-10 range
        return max(0.0, min(10.0, score))
    
    def _determine_technical_depth(self, complexity_score: float, topics: List[Topic]) -> str:
        """Determine technical depth level"""
        avg_depth = sum(t.estimated_content_depth for t in topics) / len(topics) if topics else 3
        
        if complexity_score < 4 and avg_depth < 2.5:
            return "conceptual"
        elif complexity_score > 7 or avg_depth > 4:
            return "advanced"
        else:
            return "intermediate"
    
    def _calculate_content_requirements(
        self,
        topics: List[Topic],
        document_chars: int,
        document_words: int,
        complexity_score: float,
        main_themes: List[str]
    ) -> ContentRequirements:
        """
        🎯 CORE LOGIC: Calculate dynamic content requirements to ensure 100% coverage
        """
        self.logger.info("🎯 Calculating dynamic content requirements...")
        
        topic_count = len(topics)
        
        # ===== USE CASES =====
        # NEW BUSINESS REQUIREMENT: Generate ONLY 1 comprehensive use case per document
        # This single use case should cover ALL major topics from the source document
        # Focus on quality over quantity - one perfect, detailed, professional use case
        use_cases_count = 1
        
        # Create comprehensive topic coverage for the single use case
        # List all major topics that should be covered
        use_cases_topics = self._create_comprehensive_topic_list(topics)
        
        # ===== QUIZ QUESTIONS =====
        # Rule: Minimum 2-3 questions per topic to ensure coverage
        quiz_questions_count = max(
            15,  # Minimum
            topic_count * 2,  # 2 questions per topic
            min(topic_count * 3, 40)  # Up to 3 questions per topic, max 40
        )
        
        # Distribution (35% easy, 45% medium, 20% hard)
        quiz_distribution = {
            "easy": int(quiz_questions_count * 0.35),
            "medium": int(quiz_questions_count * 0.45),
            "hard": int(quiz_questions_count * 0.20)
        }
        
        # Adjust remaining to reach total
        total_dist = sum(quiz_distribution.values())
        if total_dist < quiz_questions_count:
            quiz_distribution["medium"] += (quiz_questions_count - total_dist)
        
        # ===== TRAINER SCRIPT & POWERPOINT =====
        # Rule: Cover all topics with proper introduction, deep dive, examples, summary
        # Structure: Intro (2-3 slides) + Topics (1-2 slides each) + Summary (2-3 slides)
        
        intro_slides = 3  # Title, Overview, Learning Objectives
        topic_slides = topic_count * 2  # 2 slides per topic (theory + practice)
        example_slides = max(3, int(topic_count * 0.5))  # Real-life examples
        summary_slides = 3  # Summary, Q&A, Next Steps
        
        trainer_slides_count = intro_slides + topic_slides + example_slides + summary_slides
        
        # Adjust for complexity
        if complexity_score > 7:
            trainer_slides_count += 5  # More detailed explanations needed
        elif complexity_score < 4:
            trainer_slides_count = max(trainer_slides_count - 5, 15)
        
        # Clamp to reasonable range
        trainer_slides_count = max(15, min(trainer_slides_count, 35))
        
        # Create structured slide topics
        trainer_slide_topics = self._create_slide_structure(
            topics=topics,
            total_slides=trainer_slides_count,
            complexity=complexity_score
        )
        
        # PowerPoint has same slide count as trainer script
        powerpoint_slides_count = trainer_slides_count
        powerpoint_structure = self._create_powerpoint_structure(trainer_slide_topics)
        
        # ===== COVERAGE MAP =====
        # Map each topic to content items that cover it
        coverage_map = self._create_coverage_map(
            topics=topics,
            use_cases_topics=use_cases_topics,
            quiz_count=quiz_questions_count,
            slide_topics=trainer_slide_topics
        )
        
        # ===== ESTIMATED TOTAL PAGES =====
        # NEW: Single comprehensive use case is more detailed
        # Use case: 3-5 pages (comprehensive, detailed solutions)
        # Quiz: 0.4 pages per question (with explanations)
        # Trainer script: 1 page per slide
        # PowerPoint: Not counted (presentation file)
        
        estimated_pages = int(
            4.0 +  # Single comprehensive use case (longer, more detailed)
            quiz_questions_count * 0.4 +  # Quiz
            trainer_slides_count * 1.0  # Trainer script
        )
        
        requirements = ContentRequirements(
            use_cases_count=use_cases_count,
            use_cases_topics=use_cases_topics,
            quiz_questions_count=quiz_questions_count,
            quiz_distribution=quiz_distribution,
            trainer_slides_count=trainer_slides_count,
            trainer_slide_topics=trainer_slide_topics,
            powerpoint_slides_count=powerpoint_slides_count,
            powerpoint_structure=powerpoint_structure,
            estimated_total_pages=estimated_pages,
            coverage_map=coverage_map
        )
        
        self.logger.info(f"📊 Requirements: {use_cases_count} use cases, {quiz_questions_count} quiz Q's, {trainer_slides_count} slides, ~{estimated_pages} pages")
        
        return requirements
    
    def _create_comprehensive_topic_list(self, topics: List[Topic]) -> List[str]:
        """
        Create a comprehensive list of all major topics for the single use case.
        NEW: Supports single comprehensive use case generation.
        
        Returns:
            List with single entry containing all major topics
        """
        if not topics:
            return ["Comprehensive Use Case: General IT Concepts"]
        
        # Take top 8-10 most important topics (or all if fewer)
        major_topics = topics[:min(10, len(topics))]
        topic_names = [t.title for t in major_topics]
        
        # Create single comprehensive description
        if len(topic_names) <= 3:
            topics_str = ", ".join(topic_names)
        else:
            # List first few and indicate more
            topics_str = ", ".join(topic_names[:3]) + f" and {len(topic_names) - 3} more topics"
        
        return [f"Comprehensive Use Case covering: {topics_str}"]
    
    def _distribute_topics_to_use_cases(self, topics: List[Topic], use_cases_count: int) -> List[str]:
        """
        LEGACY METHOD: Kept for backward compatibility but no longer used.
        New implementation uses _create_comprehensive_topic_list for single use case.
        """
        use_cases_topics = []
        
        # Simple distribution: assign topics round-robin
        topics_per_case = len(topics) / use_cases_count if use_cases_count > 0 else len(topics)
        
        for i in range(use_cases_count):
            start_idx = int(i * topics_per_case)
            end_idx = int((i + 1) * topics_per_case)
            assigned_topics = topics[start_idx:end_idx]
            
            if assigned_topics:
                topic_names = ", ".join([t.title for t in assigned_topics])
                use_cases_topics.append(f"Use Case {i+1}: {topic_names}")
            else:
                use_cases_topics.append(f"Use Case {i+1}: Review and Synthesis")
        
        return use_cases_topics
    
    def _create_slide_structure(self, topics: List[Topic], total_slides: int, complexity: float) -> List[str]:
        """Create structured slide topics list"""
        slide_topics = []
        
        # Introduction slides (3)
        slide_topics.append("Titel und Übersicht")
        slide_topics.append("Lernziele und Agenda")
        slide_topics.append("Einführung und Kontext")
        
        # Topic slides (distributed)
        remaining_slides = total_slides - 6  # Minus intro (3) and summary (3)
        slides_per_topic = remaining_slides / len(topics) if topics else 1
        
        for topic in topics:
            # Each topic gets 1-2 slides depending on complexity
            slide_topics.append(f"{topic.title} - Grundlagen")
            if slides_per_topic >= 1.5 or topic.complexity == "high":
                slide_topics.append(f"{topic.title} - Praxis und Beispiele")
        
        # Summary slides (3)
        slide_topics.append("Zusammenfassung und Key Takeaways")
        slide_topics.append("Diskussion und Q&A")
        slide_topics.append("Nächste Schritte und Ressourcen")
        
        # Trim or pad to match total_slides
        if len(slide_topics) > total_slides:
            slide_topics = slide_topics[:total_slides]
        elif len(slide_topics) < total_slides:
            # Add more example slides
            for i in range(total_slides - len(slide_topics)):
                slide_topics.insert(-3, f"Real-World Beispiel {i+1}")
        
        return slide_topics
    
    def _create_powerpoint_structure(self, slide_topics: List[str]) -> List[Dict[str, Any]]:
        """Create PowerPoint structure with layout info"""
        structure = []
        
        for i, topic in enumerate(slide_topics):
            slide_info = {
                "slide_number": i + 1,
                "title": topic,
                "layout": "Title and Content" if i > 0 else "Title Slide",
                "content_type": "bullet_points",
                "has_notes": True
            }
            structure.append(slide_info)
        
        return structure
    
    def _create_coverage_map(
        self,
        topics: List[Topic],
        use_cases_topics: List[str],
        quiz_count: int,
        slide_topics: List[str]
    ) -> Dict[str, List[str]]:
        """
        Create map showing which content covers which topic.
        UPDATED: Now handles single comprehensive use case that covers all major topics.
        """
        coverage_map = {}
        
        for topic in topics:
            topic_name = topic.title
            coverage_map[topic_name] = []
            
            # NEW: Single comprehensive use case covers all major topics
            # Since we have only 1 use case, all major topics are covered by use_case_1
            if len(use_cases_topics) == 1:
                coverage_map[topic_name].append("use_case_1")
            else:
                # Fallback for legacy multi-use-case logic (if ever needed)
                for i, uc_topic in enumerate(use_cases_topics):
                    if topic_name in uc_topic:
                        coverage_map[topic_name].append(f"use_case_{i+1}")
            
            # Assume 2-3 quiz questions per topic
            quiz_per_topic = quiz_count // len(topics) if topics else 1
            for j in range(quiz_per_topic):
                coverage_map[topic_name].append(f"quiz_q{j+1}")
            
            # Find covering slides
            for i, slide_topic in enumerate(slide_topics):
                if topic_name in slide_topic:
                    coverage_map[topic_name].append(f"slide_{i+1}")
        
        return coverage_map
    
    def _generate_recommendations(
        self,
        topics: List[Topic],
        complexity_score: float,
        content_requirements: ContentRequirements
    ) -> List[str]:
        """Generate actionable recommendations for content generation"""
        recommendations = []
        
        # Complexity-based recommendations
        if complexity_score > 7:
            recommendations.append("⚠️ High complexity detected. Ensure beginner-friendly explanations with analogies.")
            recommendations.append("💡 Add more real-world examples to make advanced concepts accessible.")
        elif complexity_score < 4:
            recommendations.append("💡 Keep content engaging with practical applications despite lower complexity.")
        
        # Topic count recommendations  
        if len(topics) > 15:
            recommendations.append(f"📚 {len(topics)} topics detected. Focus on major topics in the comprehensive use case.")
        elif len(topics) < 5:
            recommendations.append(f"📚 Only {len(topics)} topics detected. Deep dive into each topic with detailed examples.")
        
        # Content generation recommendations - UPDATED for single use case
        recommendations.append(f"✅ Generate 1 comprehensive use case covering all major topics from the document.")
        recommendations.append(f"✅ Ensure use case includes extremely detailed, step-by-step solutions for every task.")
        recommendations.append(f"✅ Make use case beginner-friendly and easy to implement for learners.")
        recommendations.append(f"✅ Create {content_requirements.quiz_questions_count} quiz questions ensuring 100% topic coverage.")
        recommendations.append(f"✅ Structure presentation with {content_requirements.trainer_slides_count} slides following: Intro → Deep Dive → Examples → Summary.")
        
        # Quality recommendations - UPDATED
        recommendations.append("🎯 Professional formatting with proper spacing and clear structure.")
        recommendations.append("🎯 NO quality scores or bot mentions in the final document.")
        recommendations.append("🎯 Solutions should be detailed enough for trainers to compare learner work.")
        
        return recommendations
    
    def _calculate_confidence(self, topics: List[Topic], content: str) -> float:
        """Calculate confidence in analysis quality"""
        confidence = 0.5  # Base confidence
        
        # More topics extracted = higher confidence
        if len(topics) >= 8:
            confidence += 0.2
        elif len(topics) >= 5:
            confidence += 0.1
        
        # Topics with subtopics = better analysis
        topics_with_subtopics = sum(1 for t in topics if t.subtopics)
        if topics_with_subtopics > len(topics) * 0.5:
            confidence += 0.15
        
        # Topics with keywords = better analysis
        topics_with_keywords = sum(1 for t in topics if t.keywords)
        if topics_with_keywords > len(topics) * 0.7:
            confidence += 0.15
        
        # Clamp to 0-1
        return max(0.0, min(1.0, confidence))
    
    def _log_analysis_summary(self, result: AnalysisResult):
        """Log comprehensive analysis summary"""
        self.logger.info("=" * 80)
        self.logger.info(f"📄 DOCUMENT ANALYSIS SUMMARY: {result.document_name}")
        self.logger.info("=" * 80)
        self.logger.info(f"📊 Statistics: {result.total_words} words, {result.total_chars} chars")
        self.logger.info(f"📚 Topics Extracted: {len(result.topics)}")
        self.logger.info(f"🎯 Main Themes: {', '.join(result.main_themes)}")
        self.logger.info(f"🔢 Complexity Score: {result.complexity_score:.1f}/10 ({result.technical_depth})")
        self.logger.info(f"🎓 Confidence: {result.analysis_confidence:.1%}")
        self.logger.info("-" * 80)
        self.logger.info("📋 CONTENT REQUIREMENTS:")
        self.logger.info(f"   • Use Cases: {result.content_requirements.use_cases_count}")
        self.logger.info(f"   • Quiz Questions: {result.content_requirements.quiz_questions_count} ({result.content_requirements.quiz_distribution})")
        self.logger.info(f"   • Trainer Slides: {result.content_requirements.trainer_slides_count}")
        self.logger.info(f"   • PowerPoint Slides: {result.content_requirements.powerpoint_slides_count}")
        self.logger.info(f"   • Estimated Total Pages: {result.content_requirements.estimated_total_pages}")
        self.logger.info("-" * 80)
        self.logger.info("💡 RECOMMENDATIONS:")
        for rec in result.recommendations:
            self.logger.info(f"   {rec}")
        self.logger.info("=" * 80)
    
    def validate_coverage(
        self,
        analysis_result: AnalysisResult,
        generated_content: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        """
        Validate that generated content covers 100% of topics
        
        Args:
            analysis_result: Original analysis result
            generated_content: Dict with keys: use_cases, quiz, trainer_script, powerpoint
        
        Returns:
            (is_complete, missing_topics)
        """
        missing_topics = []
        
        # Check each topic is covered
        for topic in analysis_result.topics:
            topic_name = topic.title
            is_covered = False
            
            # Check in use cases
            use_cases_text = generated_content.get("use_cases", "")
            if topic_name.lower() in use_cases_text.lower():
                is_covered = True
            
            # Check in quiz
            quiz_text = generated_content.get("quiz", "")
            if topic_name.lower() in quiz_text.lower():
                is_covered = True
            
            # Check in trainer script
            trainer_text = generated_content.get("trainer_script", "")
            if topic_name.lower() in trainer_text.lower():
                is_covered = True
            
            if not is_covered:
                missing_topics.append(topic_name)
        
        is_complete = len(missing_topics) == 0
        
        if is_complete:
            self.logger.info("✅ 100% topic coverage achieved!")
        else:
            self.logger.warning(f"⚠️ Missing coverage for {len(missing_topics)} topics: {missing_topics}")
        
        return is_complete, missing_topics
