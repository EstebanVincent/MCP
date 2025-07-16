import base64 as b64
import os
from dataclasses import dataclass
from typing import List

import fal_client
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.utilities.types import Image

# Create an MCP server
mcp = FastMCP("Fal AI")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


@dataclass
class FalAILora:
    """Configuration for Fal AI LoRA"""

    path: str
    scale: float = 1.0
    trigger_word: str = ""

    def to_dict(self):
        return {
            "path": self.path,
            "scale": self.scale,
        }


@dataclass
class Config:
    """Configuration for image generation"""

    prompt: str
    loras: List[FalAILora]
    sync_mode: bool = True
    image_size: str = "landscape_4_3"
    num_inference_steps: int = 28
    guidance_scale: float = 3.5
    num_images: int = 1
    enable_safety_checker: bool = True
    output_format: str = "png"

    def to_dict(self):
        return {
            "prompt": self.prompt,
            "loras": [lora.to_dict() for lora in self.loras],
            "sync_mode": self.sync_mode,
            "image_size": self.image_size,
            "num_inference_steps": self.num_inference_steps,
            "guidance_scale": self.guidance_scale,
            "num_images": self.num_images,
            "enable_safety_checker": self.enable_safety_checker,
            "output_format": self.output_format,
        }


@mcp.tool()
def generate_image_with_lora(
    prompt: str,
    num_images: int = 1,
) -> Image:
    """Generate an image using Fal AI with optional LoRA"""
    try:
        loras = [
            FalAILora(
                path=os.getenv("LORA_PATH"),
                trigger_word="Esteban",
            )
        ]

        # Create configuration
        config = Config(
            prompt=prompt,
            loras=loras,
            sync_mode=True,
            num_images=num_images,
        )

        # Generate image using Fal AI
        result = fal_client.subscribe(
            "fal-ai/flux-lora",
            arguments=config.to_dict(),
        )

        # Extract image data
        image_data = result["images"][0]
        image_url = image_data["url"]

        base64_data = image_url.split(",")[1]
        decoded_bytes = b64.b64decode(base64_data)
        return Image(data=decoded_bytes, format="png")

    except Exception as e:
        return f"Error generating image: {str(e)}"
