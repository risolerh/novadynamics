# Hello NovaDynamics — Schema Guardian

This is my solution for the technical assessment for recruiting at CMS Expert (Directus).

I add my intection with the model  claude opus "Building Schema Guardian Service.md" I only had one problem whith a route on de .py but sharing the error from "docker logs -f novadynamics-app-1
and I solve it the problem

On resume, I only generated the "PROMPT_LOG.md" file and all proyect was generated automatically by antigrabity IDE and OPUS model... expose my solution in my personal computer and I test it and works fine.




## Installation

```bash
# Clone the repository
git clone https://github.com/risolerh/novadynamics.git
cd novadynamics

# Install dependencies (requires uv)
uv sync

# Copy and configure environment variables
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY
```

## Usage

```bash
# Run the development server
make dev

# Run tests
make test

# Build Docker image
make build

# Deploy with Docker Compose
make deploy
```

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check — returns `{"status": "ok"}` |
| GET | `/schema_guardian` | Analyze schema and return metadata report |

## License

CMS Expert (Directus) Technical Assessment for Recruiting by Jose Ricardo Soler Hernandez

