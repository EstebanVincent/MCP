# fal_ai_server Dockerfile

cd mcp/servers/fal_ai_server
docker build --platform linux/amd64 -t mcp-fal-ai .
docker tag mcp-fal-ai esvimcpacr.azurecr.io/mcp-fal-ai
az acr login --name esvimcpacr
docker push esvimcpacr.azurecr.io/mcp-fal-ai