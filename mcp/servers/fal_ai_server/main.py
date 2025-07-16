import base64 as b64
import os
from dataclasses import dataclass
from typing import List

import fal_client
from openai import AzureOpenAI
from pydantic import BaseModel

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.utilities.types import Image

# Create an MCP server
mcp = FastMCP("Fal AI", host="0.0.0.0", port=8025)


class FluxGeneration(BaseModel):
    prompt: str


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
def improve_user_query_for_flux(
    user_query: str,
) -> str:
    """Use Azure OpenAI to improve the user query for FLUX.1 image generation.
    This use a specific trigger word to generate a prompt for FLUX.1 with a specific LoRA.
    The trigger word is 'Esteban' which is a person"""
    trigger_word = "Esteban"
    system_prompt = """
    You are an expert in Flux.1 prompting generation based on your understanding of the user query.
    Those query will be based on a trigger word that will be used to generate images using a specific LoRA.
    Your role is to generate a prompt using the trigger word that will be sent to FLUX.1 to generate images with a LoRA.
    Output should be in JSON format with a single key "prompt" and the value should be the prompt to be sent to FLUX.1.
    
    <FLUX PROMPTING GUIDE>
    FLUX.1 excels at processing **natural language instructions**, making it easy to generate high-quality images with well-structured prompts. Follow these best practices to achieve the best results.

    ## **General Prompting Tips**  
    The fundamental rules of prompt engineering still apply:  
    ✅ Be **precise, detailed, and direct**.  
    ✅ Describe not just the content but also **tone, style, color palette, and perspective**.  
    ✅ For **photorealistic images**, specify details like camera type (e.g., “shot on iPhone 16”), aperture, lens, and shot type.  

    ## **FLUX.1-Specific Techniques**  

    ### **1. Layered Image Composition**  
    FLUX.1 allows precise control over **foreground, middle ground, and background**. Structure your prompt logically:  
    - **First**, define foreground elements.  
    - **Then**, describe the middle ground.  
    - **Finally**, set the background scene.  

    ✅ **Good Example:**  
    *"In the foreground, a vintage car with a 'CLASSIC' plate is parked on a cobblestone street. Behind it, a bustling market scene with colorful awnings. In the background, an old castle stands atop a misty hill."*  

    ---

    ### **2. Contrasting Colors & Aesthetics**  
    High-contrast images are visually striking. Specify **where** each aesthetic applies and **how they transition**.  

    ✅ **Good Example:**  
    *"A single tree at the center. The left half is lush, green, and bathed in sunlight. The right half is frost-covered, under a dark stormy sky. The transition is a sharp split down the middle."*  

    ---

    ### **3. Transparent Materials & Textures**  
    FLUX.1 accurately renders objects behind **glass, ice, plastic, or water**, provided you structure your prompt well.  
    - Clearly specify **which object is in front** and **what is visible behind it**.  

    ✅ **Good Example:**  
    *"A hanging glass terrarium containing a miniature rainforest with orchids and waterfalls. Through the rain-streaked glass, a neon sign reading 'Rainforest Retreat' glows softly."*  

    ---

    ### **4. Incorporating Text in Images**  
    FLUX.1 can now generate **legible, stylized text** in images. For best results:  
    - **Describe font, size, color, placement, and effects** (e.g., shadow, glow, outline).  

    ✅ **Good Example:**  
    *"A vintage travel poster for Paris. The Eiffel Tower dominates the center, bathed in warm sunset hues. At the top, 'PARIS' is written in bold Art Deco font, golden with a slight 3D effect. At the bottom, 'City of Lights' glows in elegant cursive."*  
    </FLUX PROMPTING GUIDE>
    """
    with AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    ) as openai_client:
        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": f"trigger_word: {trigger_word}\nquery: {user_query}",
            },
        ]
        llm_response = openai_client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            response_format=FluxGeneration,
        )

        llm_response = llm_response.choices[0].message.parsed
    return llm_response.prompt


@mcp.tool()
def generate_image_with_lora(
    prompt: str,
    num_images: int = 1,
) -> Image:
    """Generate an image using Fal AI model FLUX.1 DEV with Esteban LoRA"""
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


if __name__ == "__main__":
    # streamable-http not yet supported by vscode, change in url /sse to /mcp
    # mcp.run(transport="streamable-http")
    mcp.run(transport="sse")
