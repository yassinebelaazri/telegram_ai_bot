
"""
Content Filter module for Telegram AI Bot
Filters inappropriate and harmful content from user prompts
"""

import re
import logging
from typing import List, Set

logger = logging.getLogger(__name__)

class ContentFilter:
    def __init__(self):
        """Initialize content filter with banned words and patterns"""
        self.banned_words = self._load_banned_words()
        self.banned_patterns = self._load_banned_patterns()
        logger.info(f"Content filter initialized with {len(self.banned_words)} banned words")
    
    def _load_banned_words(self) -> Set[str]:
        """Load list of banned words and phrases"""
        # NSFW and inappropriate content
        nsfw_words = {
            'nude', 'naked', 'sex', 'porn', 'xxx', 'adult', 'erotic', 'sexual',
            'breast', 'penis', 'vagina', 'orgasm', 'masturbation', 'fetish',
            'bdsm', 'kinky', 'seductive', 'provocative', 'sensual', 'intimate',
            'lingerie', 'bikini', 'underwear', 'topless', 'bottomless',
            'explicit', 'graphic', 'mature', 'nsfw', 'not safe for work'
        }
        
        # Violence and harmful content
        violence_words = {
            'kill', 'murder', 'death', 'blood', 'gore', 'violence', 'weapon',
            'gun', 'knife', 'sword', 'bomb', 'explosion', 'war', 'fight',
            'attack', 'assault', 'torture', 'abuse', 'harm', 'hurt', 'pain',
            'suicide', 'self-harm', 'cutting', 'hanging', 'shooting',
            'stabbing', 'beating', 'punching', 'kicking', 'slapping'
        }
        
        # Hate speech and discrimination
        hate_words = {
            'nazi', 'hitler', 'racist', 'racism', 'hate', 'discrimination',
            'supremacist', 'extremist', 'terrorist', 'terrorism', 'radical'
        }
        
        # Illegal activities
        illegal_words = {
            'drug', 'cocaine', 'heroin', 'marijuana', 'cannabis', 'meth',
            'illegal', 'criminal', 'theft', 'robbery', 'fraud', 'scam'
        }
        
        # Combine all banned words
        all_banned = nsfw_words | violence_words | hate_words | illegal_words
        
        # Convert to lowercase for case-insensitive matching
        return {word.lower() for word in all_banned}
    
    def _load_banned_patterns(self) -> List[re.Pattern]:
        """Load regex patterns for more complex filtering"""
        patterns = [
            # Email addresses (to prevent spam)
            re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            
            # URLs (to prevent malicious links)
            re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'),
            
            # Phone numbers (to prevent spam)
            re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),
            
            # Excessive repetition (spam detection)
            re.compile(r'(.)\1{10,}'),  # Same character repeated 10+ times
        ]
        
        return patterns
    
    def is_safe_prompt(self, prompt: str) -> bool:
        """
        Check if prompt is safe for image generation
        
        Args:
            prompt (str): User input prompt
            
        Returns:
            bool: True if prompt is safe, False otherwise
        """
        if not prompt or not isinstance(prompt, str):
            return False
        
        # Normalize text for analysis
        normalized_text = prompt.lower().strip()
        
        # Check for banned words
        words = re.findall(r'\b\w+\b', normalized_text)
        for word in words:
            if word in self.banned_words:
                logger.warning(f"Banned word detected: {word}")
                return False
        
        # Check for banned patterns
        for pattern in self.banned_patterns:
            if pattern.search(prompt):
                logger.warning(f"Banned pattern detected in prompt")
                return False
        
        # Check for excessive length
        if len(prompt) > 1000:
            return False
        
        # Check for minimum length
        if len(prompt.strip()) < 3:
            return False
        
        return True

