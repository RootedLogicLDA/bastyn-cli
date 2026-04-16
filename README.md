# bastyn-cli

Command-line installer for [BASTYN](https://bastyn.ai) on-premises deployments.

## Install

```bash
curl -sSL https://raw.githubusercontent.com/RootedLogicLDA/bastyn-cli/main/install.sh | bash
```

Or directly via pipx:

```bash
pipx install bastyn-cli
```

## Usage

You will receive a license token from your BASTYN account representative.

```bash
bastyn init              # activate + configure + authenticate to image registry
bastyn up                # pull images and start all services
bastyn status            # show service health
bastyn logs              # tail logs (all services)
bastyn logs backend      # tail logs for one service
bastyn restart           # restart all services
bastyn restart backend   # restart one service
bastyn down              # stop all services (data preserved)
bastyn down --volumes    # stop and DELETE all data
bastyn upgrade           # pull new image versions and restart
bastyn rotate-key        # rotate registry credentials
```

Run `bastyn COMMAND --help` for details on any command.

## What `bastyn init` does

1. Prompts for your license token
2. Contacts `api.bastyn.ai` to activate — provisions a dedicated, revocable image-pull credential for your organisation
3. Downloads the pinned deployment files (`docker-compose.yml`, `.env.example`, `litellm_config.yaml`, `nginx.conf`, `README.md`, `serena_config.yml`) into `./bastyn` (or `--install-dir`)
4. Runs `docker login` against `europe-west1-docker.pkg.dev`
5. Walks you through each `.env` value — auto-generating secrets where possible, prompting for your LLM provider keys
6. Saves local state to `~/.bastyn/` (license token, install path)

Your LLM keys and admin credentials **never leave your machine**. The activation service only sees the license token and basic client info (OS, hostname) for audit logging.

## Prerequisites

### Infrastructure

- Docker Desktop or Docker Engine + Compose plugin (v24+)
- Python 3.10+
- 4 CPU cores, 16 GB RAM, 50 GB disk
- Outbound HTTPS to `activate.bastyn.ai` and `europe-west1-docker.pkg.dev`

### Have ready before running `bastyn init`

| What | Where to get it | Used for |
|------|----------------|----------|
| **BASTYN license token** | Provided by your BASTYN account representative | Activating your deployment and provisioning registry credentials |
| **OpenAI API key** *or* **Azure OpenAI endpoint + key** | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) or Azure AI Studio | LLM-powered analysis (two models required: `gpt-4o-mini` + `gpt-5.1`) |
| **Admin email + password** | You choose these | First superuser account for the BASTYN UI |

The following are auto-generated for you during setup (no action needed):

| What | Purpose |
|------|---------|
| `SECRET_KEY` | JWT token signing |
| `POSTGRES_PASSWORD` | Database password |
| `LITELLM_MASTER_KEY` | Internal LLM proxy authentication |

See the bundled `README.md` inside your install directory for the full deployment guide, including Azure OpenAI configuration and parallelization tuning.

## Support

Contact your BASTYN account representative
Bal@Rootedlogic.ai
CLaudio@Rootedlogic.ai
