"""
Content Quality Validator for FIAE AI Content Factory
"""

import re
from typing import Dict, Any, List
from loguru import logger


class ContentQualityValidator:
    """Validates generated content quality and structure"""
    
    def __init__(self):
        self.min_content_length = 100
        self.min_quality_score = 0.7
        
    def validate_generated_content(self, content: Dict[str, Any], content_depth: str = "comprehensive") -> Dict[str, Any]:
        """Validate generated content quality"""
        try:
            validation_results = {
                'overall_quality_score': 0.0,
                'meets_standards': False,
                'professional_grade': False,
                'sellable_quality': False,
                'section_scores': {},
                'issues': [],
                'recommendations': []
            }
            
            # Required content sections
            required_sections = ['knowledge_analysis', 'use_case_text', 'quiz_text', 'powerpoint_structure', 'google_slides_content', 'trainer_script']
            
            total_score = 0.0
            valid_sections = 0
            
            for section in required_sections:
                if section in content:
                    section_score = self._validate_section(content[section], section)
                    validation_results['section_scores'][section] = section_score
                    total_score += section_score
                    valid_sections += 1
                else:
                    validation_results['issues'].append(f"Missing required section: {section}")
            
            # Calculate overall quality score
            if valid_sections > 0:
                validation_results['overall_quality_score'] = total_score / valid_sections
            else:
                validation_results['overall_quality_score'] = 0.0
            
            # Determine quality levels
            quality_score = validation_results['overall_quality_score']
            
            if quality_score >= 0.9:
                validation_results['professional_grade'] = True
                validation_results['sellable_quality'] = True
                validation_results['meets_standards'] = True
            elif quality_score >= 0.8:
                validation_results['professional_grade'] = True
                validation_results['meets_standards'] = True
            elif quality_score >= 0.7:
                validation_results['meets_standards'] = True
            
            # Add recommendations
            if quality_score < 0.7:
                validation_results['recommendations'].append("Content quality below standards - regeneration recommended")
            elif quality_score < 0.8:
                validation_results['recommendations'].append("Content quality acceptable but could be improved")
            else:
                validation_results['recommendations'].append("Content quality meets professional standards")
            
            logger.info(f"[VALIDATOR] Content validation completed - Score: {quality_score:.1%}")
            return validation_results
            
        except Exception as e:
            logger.error(f"Error validating content: {e}")
            return {
                'overall_quality_score': 0.0,
                'meets_standards': False,
                'professional_grade': False,
                'sellable_quality': False,
                'section_scores': {},
                'issues': [f"Validation error: {str(e)}"],
                'recommendations': ["Content validation failed - manual review required"]
            }
    
    def _validate_section(self, content: Any, section_name: str) -> float:
        """Validate individual content section"""
        try:
            # Handle different content types
            if isinstance(content, list):
                # Convert list to string for validation
                content_text = '\n'.join(str(item) for item in content)
            elif isinstance(content, dict):
                content_text = str(content)
            else:
                content_text = str(content)
            
            # Basic length check
            if len(content_text.strip()) < self.min_content_length:
                logger.warning(f"[VALIDATOR] Section {section_name} too short: {len(content_text)} chars")
                return 0.3
            
            # Content quality checks
            score = 0.0
            
            # Length score (0-0.3)
            length_score = min(len(content_text) / 1000, 0.3)  # Max 0.3 for length
            score += length_score
            
            # Structure score (0-0.3)
            structure_score = self._check_structure(content_text, section_name)
            score += structure_score
            
            # Content relevance score (0-0.4)
            relevance_score = self._check_relevance(content_text, section_name)
            score += relevance_score
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error validating section {section_name}: {e}")
            return 0.0
    
    def _check_structure(self, content: str, section_name: str) -> float:
        """Check content structure quality"""
        try:
            score = 0.0
            
            # Check for proper formatting
            if section_name in ['knowledge_analysis', 'use_case_text', 'trainer_script']:
                # Should have headings
                if re.search(r'^#+\s+', content, re.MULTILINE):
                    score += 0.1
                
                # Should have bullet points or numbered lists
                if re.search(r'^[\*\-\+]\s+|\d+\.\s+', content, re.MULTILINE):
                    score += 0.1
                
                # Should have paragraphs
                if len(content.split('\n\n')) > 2:
                    score += 0.1
            
            elif section_name == 'quiz_text':
                # Should have questions
                if re.search(r'\?', content):
                    score += 0.15
                
                # Should have multiple choice or answers
                if re.search(r'[A-D]\)|Antwort|Lösung', content):
                    score += 0.15
            
            elif section_name in ['powerpoint_structure', 'google_slides_content']:
                # Should have slide structure
                if re.search(r'Folie|Slide|Titel', content, re.IGNORECASE):
                    score += 0.15
                
                # Should have bullet points
                if re.search(r'^[\*\-\+]\s+', content, re.MULTILINE):
                    score += 0.15
            
            return min(score, 0.3)
            
        except Exception as e:
            logger.error(f"Error checking structure: {e}")
            return 0.0
    
    def _check_relevance(self, content: str, section_name: str) -> float:
        """Check content relevance and quality"""
        try:
            score = 0.0
            
            # Check for German content (expected language)
            german_words = ['der', 'die', 'das', 'und', 'oder', 'mit', 'für', 'von', 'zu', 'in', 'auf', 'an']
            german_count = sum(1 for word in german_words if word in content.lower())
            if german_count >= 3:
                score += 0.1
            
            # Check for technical terms (indicates quality content)
            technical_terms = ['system', 'prozess', 'methode', 'technik', 'anwendung', 'implementierung', 'entwicklung']
            tech_count = sum(1 for term in technical_terms if term in content.lower())
            if tech_count >= 2:
                score += 0.1
            
            # Check for professional language
            professional_terms = ['analyse', 'bewertung', 'strategie', 'konzept', 'lösung', 'optimierung']
            prof_count = sum(1 for term in professional_terms if term in content.lower())
            if prof_count >= 2:
                score += 0.1
            
            # Check for actionable content
            action_terms = ['schritt', 'phase', 'methode', 'verfahren', 'prozess', 'workflow']
            action_count = sum(1 for term in action_terms if term in content.lower())
            if action_count >= 1:
                score += 0.1
            
            return min(score, 0.4)
            
        except Exception as e:
            logger.error(f"Error checking relevance: {e}")
            return 0.0


# Global validator instance
content_validator = ContentQualityValidator()




