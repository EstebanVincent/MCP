# fal_ai_server Dockerfile

cd mcp/servers/fal_ai_server
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
docker build --platform linux/amd64 -t mcp-fal-ai .
docker tag mcp-fal-ai esvimcpacr.azurecr.io/mcp-fal-ai:${TIMESTAMP}
docker tag mcp-fal-ai esvimcpacr.azurecr.io/mcp-fal-ai:latest
az acr login --name esvimcpacr
docker push esvimcpacr.azurecr.io/mcp-fal-ai:${TIMESTAMP}
docker push esvimcpacr.azurecr.io/mcp-fal-ai:latest