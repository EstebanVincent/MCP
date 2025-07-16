# Fal AI MCP Server

A Model Context Protocol (MCP) server that provides AI image generation capabilities using Fal.ai's FLUX.1 DEV model with a custom Esteban LoRA. This server includes intelligent prompt enhancement using Azure OpenAI to optimize image generation results.

## Features

- **AI Image Generation**: Generate high-quality images using FLUX.1 DEV model
- **Custom LoRA Support**: Includes personalized Esteban LoRA for character-specific generation
- **Intelligent Prompt Enhancement**: Uses Azure OpenAI to optimize user prompts for better results
- **Dockerized Deployment**: Easy setup and deployment with Docker
- **VS Code Integration**: Seamless integration with VS Code through MCP

## Tools Available

### `generate_image_with_lora`
Generate images using Fal AI's FLUX.1 DEV model with the Esteban LoRA.

**Parameters:**
- `prompt` (string): The text prompt for image generation
- `num_images` (int, optional): Number of images to generate (default: 1)

### `improve_user_query_for_flux`
Enhance user prompts using Azure OpenAI to optimize them for FLUX.1 image generation.

**Parameters:**
- `user_query` (string): The original user query to enhance

## Prerequisites

- Docker installed on your system
- VS Code with MCP extension
- Required API keys:
  - Fal.ai API key
  - Azure OpenAI API key
  - Esteban LoRA path

## Usage Examples

Once connected, you can use the tools through VS Code's MCP interface:

### Generate an Image
```
create an image of me as a cyberpunk hacker
```

### Enhanced Prompt Generation
The server automatically enhances prompts using Azure OpenAI to optimize them for FLUX.1, incorporating best practices for:
- Layered image composition
- Contrasting colors and aesthetics
- Transparent materials and textures
- Text incorporation in images
