# Setup LLMS on a single raspberry pi

Install Ollama: `curl -fsSL https://ollama.com/install.sh | sh`

Wait for install, then run `ollama run <model-name>` or `ollama pull <model-name>` to get LLM models on the device

**Note**: to expose ollama to the local network, enter this

```sh
sudo systemctl stop ollama.service
sudo systemctl edit ollama.service
```

Add this text to the ollama.service file:

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_NUM_PARALLEL=4"
```

```sh
systemctl daemon-reload
systemctl restart ollama
systemctl enable ollama
```

Find network devices (i.e. pi hostnames): `arp -a`

## Run Open WebUI

**For Local Mac conection**:

- `docker stop open-webui`
- `just openwebui-run-mac`
- in browser, open <http://localhost:3000>

**Run with Raspberry Pi Ollama Server**:

- `docker stop open-webui`
- `just openwebui-run-pi`
  - this is configured to use <http://raspi-ollama.ht.home> url
