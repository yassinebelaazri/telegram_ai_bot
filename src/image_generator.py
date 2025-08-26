
"""
Image Generator module for Telegram AI Bot
Handles AI image generation using OpenAI DALL-E API
"""

import os
import logging
import asyncio
import aiohttp
from typing import Optional
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class ImageGenerator:
    def __init__(self):
        """Initialize the image generator with OpenAI client"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Initialize OpenAI client
        self.client = AsyncOpenAI(api_key=self.api_key)
        
        # Configuration
        self.model = "dall-e-3"  # Use DALL-E 3 for best quality
        self.size = "1024x1024"  # Standard square format
        self.quality = "standard"  # Can be "standard" or "hd"
        self.style = "vivid"  # Can be "vivid" or "natural"
        
        logger.info("Image generator initialized successfully")
    
    async def generate_image(self, prompt: str) -> Optional[str]:
        """
        Generate an image using OpenAI DALL-E API
        
        Args:
            prompt (str): Text description for image generation
            
        Returns:
            Optional[str]: URL of the generated image or None if failed
        """
        try:
            # Clean and validate prompt
            cleaned_prompt = self._clean_prompt(prompt)
            if not cleaned_prompt:
                logger.error("Invalid or empty prompt provided")
                return None
            
            logger.info(f"Generating image for prompt: {cleaned_prompt[:100]}...")
            
            # Call OpenAI DALL-E API
            response = await self.client.images.generate(
                model=self.model,
                prompt=cleaned_prompt,
                size=self.size,
                quality=self.quality,
                style=self.style,
                n=1  # Generate only one image
            )
            
            # Extract image URL from response
            if response.data and len(response.data) > 0:
                image_url = response.data[0].url
                logger.info(f"Image generated successfully: {image_url}")
                return image_url
            else:
                logger.error("No image data received from OpenAI API")
                return None
                
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return None
    
    def _clean_prompt(self, prompt: str) -> str:
        """
        Clean and validate the prompt for image generation
        
        Args:
            prompt (str): Raw prompt from user
            
        Returns:
            str: Cleaned prompt ready for API call
        """
        if not prompt or not isinstance(prompt, str):
            return ""
        
        # Remove extra whitespace and limit length
        cleaned = prompt.strip()
        
        # Limit prompt length (DALL-E has a limit of around 1000 characters)
        max_length = 1000
        if len(cleaned) > max_length:
            cleaned = cleaned[:max_length].rsplit(' ', 1)[0]  # Cut at word boundary
            logger.warning(f"Prompt truncated to {len(cleaned)} characters")
        
        # Add quality enhancement keywords if prompt is very short
        if len(cleaned) < 20:
            cleaned += ", high quality, detailed, professional"
        
        return cleaned

