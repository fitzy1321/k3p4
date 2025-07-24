default:
    just --list

# default:
#     ansible-playbook playbook.yaml -i inventory.yaml

# Run against local ollama
openwebui-run-mac:
    docker run -d --rm -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main

openwebui-run-pi:
    docker run -d --rm -p 3000:8080 -e OLLAMA_BASE_URL=http://raspi-ollama.ht.home:11434 -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main

openwebui-clear:
    docker stop open-webui
