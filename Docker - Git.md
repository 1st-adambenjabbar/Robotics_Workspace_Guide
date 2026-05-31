# Docker — Complete Guide
### Installation, Usage, Workflows & Tips
#### Ubuntu · Windows 11 · WSL2

> **Docker** packages your application and all its dependencies into a **container** — an isolated, reproducible environment that runs identically on every machine. Essential for robotics, ML pipelines, ROS2 development, and CI/CD.


## Table of Contents

- [What Is Docker?](#what-is-docker)
- [Core Concepts](#core-concepts)
- [Installation](#installation)
  - [Ubuntu — Docker Engine](#install--ubuntu-docker-engine)
  - [Windows 11 — Docker Desktop](#install--windows-11-docker-desktop)
  - [WSL2 — Docker Engine or Docker Desktop Integration](#install--wsl2)
- [Post-Installation Setup](#post-installation-setup)
- [Essential Docker Commands](#essential-docker-commands)
- [Images](#images)
- [Containers](#containers)
- [Volumes — Persistent Storage](#volumes--persistent-storage)
- [Networking](#networking)
- [Dockerfile — Build Your Own Image](#dockerfile--build-your-own-image)
- [Docker Compose](#docker-compose)
- [Docker with NVIDIA GPU (CUDA)](#docker-with-nvidia-gpu-cuda)
- [Useful Workflows](#useful-workflows)
- [Docker Registries](#docker-registries)
- [Managing Resources](#managing-resources)
- [Troubleshooting](#troubleshooting)
- [Quick Reference Card](#quick-reference-card)


## What Is Docker?

Traditional development problem: "it works on my machine." Docker solves this by bundling your code + runtime + libraries + config into a **container** that behaves identically everywhere.

```
Without Docker:               With Docker:
┌──────────────┐              ┌──────────────────────────┐
│ Your code    │              │ Container                │
│ + Python 3.9 │  → works     │  ├── Your code           │
│ + lib v1.2   │  here but    │  ├── Python 3.9          │  → works
│              │  not there   │  └── lib v1.2            │  everywhere
└──────────────┘              └──────────────────────────┘
```


## Core Concepts

| Term | Definition |
|------|-----------|
| **Image** | A read-only template — the blueprint for a container (e.g. `ubuntu:22.04`, `ros:humble`) |
| **Container** | A running instance of an image — isolated, ephemeral |
| **Dockerfile** | A script of instructions that builds a custom image |
| **Volume** | A persistent storage mount that survives container restarts |
| **Network** | A virtual network connecting containers |
| **Registry** | A service hosting images (Docker Hub, GHCR, NVIDIA NGC) |
| **Compose** | A tool for defining multi-container apps in a single YAML file |
| **Layer** | Each instruction in a Dockerfile adds a layer; layers are cached |

```
Registry (Docker Hub)
     │
     │ docker pull
     ▼
   Image  ──── docker run ────►  Container(s)
     ▲                                │
     │ docker build                   │ docker exec
  Dockerfile                          ▼
                                  Running process
```


## Installation

### Install — Ubuntu (Docker Engine)

Docker Engine is the lightweight server-side component — no GUI, no subscription required.

**1. Remove any old Docker packages:**

```bash
sudo apt remove docker docker-engine docker.io containerd runc 2>/dev/null
```

**2. Add Docker's official repository:**

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

**3. Install Docker Engine:**

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

**4. Verify:**

```bash
sudo docker run hello-world
# Should print: "Hello from Docker!"
```


### Install — Windows 11 (Docker Desktop)

Docker Desktop is the recommended way to use Docker on Windows. It includes Docker Engine, Compose, and a GUI.

**Prerequisites:**

- Windows 11 64-bit, version 23H2 (build 22631) or higher
- WSL 2 enabled (`wsl --install` if not already done)
- Virtualization enabled in BIOS
- WSL version ≥ 2.1.5 (`wsl --version` to check)

**Installation:**

1. Download Docker Desktop from [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
2. Run `Docker Desktop Installer.exe`
3. Ensure **"Use WSL 2 based engine"** is checked during setup
4. Accept the license and complete installation
5. Reboot when prompted

**Or via winget:**

```powershell
winget install Docker.DockerDesktop
```

**Verify:**

```powershell
docker --version
docker run hello-world
```

> ℹ️ **Docker Desktop is free for personal use, education, and open-source projects.** Commercial use in larger organizations requires a paid subscription.

**Configure WSL2 integration (Docker Desktop):**

1. Open Docker Desktop → Settings → Resources → WSL Integration
2. Enable **"Enable integration with my default WSL distro"**
3. Toggle on your Ubuntu distro
4. Click **Apply & Restart**

Now `docker` commands work from inside your WSL2 terminal.


### Install — WSL2

You have two options:

**Option A — Use Docker Desktop (recommended, easiest)**

Install Docker Desktop on Windows (see above), enable WSL integration. Done — `docker` is available inside WSL2 automatically.

**Option B — Native Docker Engine inside WSL2 (no Docker Desktop)**

For users who cannot or prefer not to use Docker Desktop:

```bash
# Inside your WSL2 Ubuntu terminal

# Remove old packages
sudo apt remove docker docker-engine docker.io containerd runc 2>/dev/null

# Add Docker repo (same as native Ubuntu)
sudo apt update
sudo apt install -y ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start Docker daemon manually (WSL2 doesn't use systemd by default)
sudo service docker start

# Add to .bashrc so Docker starts automatically with WSL2
echo "sudo service docker start > /dev/null 2>&1" >> ~/.bashrc
```

>  If your WSL2 distro has **systemd enabled** (Ubuntu 22.04+ on recent WSL), you can use `sudo systemctl enable docker` instead.


## Post-Installation Setup

### Run Docker without `sudo` (Linux / WSL2)

By default, Docker requires `sudo`. To run it as your regular user:

```bash
# Add yourself to the docker group
sudo groupadd docker
sudo usermod -aG docker $USER

# Apply the new group (or log out and back in)
newgrp docker

# Verify — no sudo needed
docker run hello-world
```

> ️ Members of the `docker` group have root-equivalent access. Only add trusted users.

### Enable Docker to start on boot (Ubuntu)

```bash
sudo systemctl enable docker
sudo systemctl enable containerd
```


## Essential Docker Commands

### Version and info

```bash
docker --version          # Docker version
docker info               # Full system info
docker version            # Client + server version details
```


## Images

Images are the starting point for every container.

```bash
# Search for images on Docker Hub
docker search ubuntu

# Pull an image
docker pull ubuntu:22.04

# Pull latest tag
docker pull nginx

# List local images
docker images
docker image ls

# Remove an image
docker rmi ubuntu:22.04
docker image rm ubuntu:22.04

# Remove all dangling images (untagged, unused)
docker image prune

# Remove all unused images
docker image prune -a

# Inspect image metadata
docker inspect ubuntu:22.04

# See image layers
docker history ubuntu:22.04

# Tag an image for a registry
docker tag myapp:latest myusername/myapp:v1.0.0
```


## Containers

```bash
# Run a container (pulls image if not local)
docker run ubuntu:22.04

# Run interactively with a terminal (-it = interactive + pseudo-TTY)
docker run -it ubuntu:22.04 bash

# Run in the background (detached)
docker run -d nginx

# Name a container
docker run --name my-nginx -d nginx

# Map a host port to a container port
docker run -d -p 8080:80 nginx
# Access at http://localhost:8080

# Set environment variables
docker run -e MY_VAR=hello ubuntu:22.04

# Mount a volume
docker run -v /host/path:/container/path ubuntu:22.04

# Run and automatically remove the container when it exits
docker run --rm ubuntu:22.04 echo "Hello"

# Limit CPU and memory
docker run --memory="512m" --cpus="1.0" ubuntu:22.04

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop a running container
docker stop my-nginx

# Start a stopped container
docker start my-nginx

# Restart a container
docker restart my-nginx

# Remove a stopped container
docker rm my-nginx

# Remove a running container (force)
docker rm -f my-nginx

# Remove all stopped containers
docker container prune

# Execute a command inside a running container
docker exec my-nginx ls /etc/nginx

# Open an interactive shell in a running container
docker exec -it my-nginx bash

# See container logs
docker logs my-nginx

# Follow logs in real time
docker logs -f my-nginx

# See last 50 lines of logs
docker logs --tail 50 my-nginx

# Inspect container details (IP, mounts, config)
docker inspect my-nginx

# See CPU / memory usage
docker stats

# Copy files between host and container
docker cp ./file.txt my-nginx:/etc/nginx/file.txt
docker cp my-nginx:/etc/nginx/nginx.conf ./nginx.conf
```


## Volumes — Persistent Storage

Containers are **ephemeral** — their filesystem is destroyed when removed. Use volumes for persistent data.

```bash
# Create a named volume
docker volume create mydata

# List volumes
docker volume ls

# Inspect a volume (see where it lives on disk)
docker volume inspect mydata

# Run a container with a named volume
docker run -d -v mydata:/var/lib/postgresql/data postgres:15

# Bind mount (maps a host directory directly)
docker run -d -v $(pwd)/data:/app/data myapp

# Remove a volume
docker volume rm mydata

# Remove all unused volumes
docker volume prune
```

**Volume vs Bind Mount:**

| | Named Volume | Bind Mount |
|-|-------------|------------|
| **Path** | Managed by Docker (`/var/lib/docker/volumes/`) | Explicit host path |
| **Portability** | Works anywhere | Tied to host path |
| **Best for** | Databases, persistent app data | Development (edit files on host, see changes live) |


## Networking

```bash
# List networks
docker network ls

# Create a custom network
docker network create mynet

# Run containers on the same network (they can reach each other by name)
docker run -d --name db --network mynet postgres:15
docker run -d --name app --network mynet myapp

# Inside 'app', you can reach 'db' at hostname 'db'

# Connect a running container to a network
docker network connect mynet my-nginx

# Disconnect from a network
docker network disconnect mynet my-nginx

# Remove a network
docker network rm mynet

# Inspect a network
docker network inspect mynet
```

**Default network modes:**

| Mode | Description |
|------|-------------|
| `bridge` | Default isolated network; containers talk via IP or name |
| `host` | Container shares the host network namespace (Linux only) |
| `none` | No network — fully isolated |


## Dockerfile — Build Your Own Image

A `Dockerfile` is a recipe for building a custom image.

### Basic structure

```dockerfile
# Base image
FROM ubuntu:22.04

# Metadata
LABEL maintainer="adam@example.com"

# Run commands during build (creates a new layer)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files from host into the image
COPY requirements.txt .

# Run pip install
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment variables
ENV PORT=8000

# Expose a port (documentation only — doesn't publish it)
EXPOSE 8000

# Default command when container starts
CMD ["python3", "app.py"]
```

### Build and run

```bash
# Build from Dockerfile in current directory
docker build -t myapp:latest .

# Build with a specific Dockerfile
docker build -f Dockerfile.prod -t myapp:prod .

# Build with build arguments
docker build --build-arg VERSION=1.2.3 -t myapp:1.2.3 .

# Run your image
docker run -d -p 8000:8000 myapp:latest
```

### Dockerfile best practices

```dockerfile
#  Combine RUN commands to reduce layers
RUN apt-get update && apt-get install -y git curl \
    && rm -rf /var/lib/apt/lists/*

#  Use .dockerignore (like .gitignore) to exclude unnecessary files
# Create .dockerignore:
# __pycache__/
# .git/
# *.pyc
# node_modules/

#  Use specific tags, not 'latest' in production
FROM python:3.11-slim

#  Use non-root user for security
RUN useradd -m appuser
USER appuser

#  Multi-stage builds — smaller final image
FROM python:3.11 AS builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim AS runtime
COPY --from=builder /root/.local /root/.local
COPY . .
CMD ["python3", "app.py"]
```


## Docker Compose

Docker Compose lets you define and run **multi-container applications** in a single `docker-compose.yml` file.

### Example: Python app + PostgreSQL database

```yaml
# docker-compose.yml
version: "3.9"

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: adam
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: mydb
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - app_net

  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://adam:secret@db:5432/mydb
    depends_on:
      - db
    volumes:
      - .:/app           # bind mount for live reloading
    networks:
      - app_net

volumes:
  db_data:

networks:
  app_net:
```

### Compose commands

```bash
# Start all services (build if needed)
docker compose up

# Start in the background
docker compose up -d

# Build and start
docker compose up --build

# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v

# View logs
docker compose logs

# Follow logs
docker compose logs -f app

# Scale a service
docker compose up -d --scale app=3

# Run a one-off command in a service
docker compose run app python manage.py migrate

# Execute in a running service
docker compose exec app bash

# List services
docker compose ps

# Restart a service
docker compose restart app

# Pull latest images
docker compose pull
```


## Docker with NVIDIA GPU (CUDA)

To use CUDA inside containers, install the **NVIDIA Container Toolkit**.

### Install NVIDIA Container Toolkit (Ubuntu / WSL2)

```bash
# Add the NVIDIA Container Toolkit repository
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt update
sudo apt install -y nvidia-container-toolkit

# Configure Docker to use the NVIDIA runtime
sudo nvidia-ctk runtime configure --runtime=docker

# Restart Docker
sudo systemctl restart docker
```

### Run a GPU-enabled container

```bash
# Pass all GPUs
docker run --gpus all nvidia/cuda:12.6.0-base-ubuntu22.04 nvidia-smi

# Pass a specific GPU
docker run --gpus '"device=0"' nvidia/cuda:12.6.0-base-ubuntu22.04 nvidia-smi

# Isaac Sim example
docker run --gpus all --rm -it \
  nvcr.io/nvidia/isaac-sim:5.1.0 \
  ./isaac-sim.sh --headless
```

### In docker-compose.yml

```yaml
services:
  ml_trainer:
    image: pytorch/pytorch:2.7.0-cuda12.8-cudnn9-runtime
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```


## Useful Workflows

### Development with live code reload (bind mount)

```bash
docker run -it --rm \
  -v $(pwd):/app \
  -w /app \
  -p 8000:8000 \
  python:3.11-slim \
  python app.py
```

Edit files on your host — changes appear immediately inside the container.


### ROS2 in Docker

```bash
# Pull official ROS2 Humble image
docker pull ros:humble

# Run with X11 forwarding (for GUI tools like RViz) on Linux
docker run -it --rm \
  --env DISPLAY=$DISPLAY \
  --volume /tmp/.X11-unix:/tmp/.X11-unix \
  ros:humble \
  bash

# Inside the container:
source /opt/ros/humble/setup.bash
ros2 topic list
```


### One-shot containers (clean, ephemeral)

```bash
# Run, use, and auto-remove
docker run --rm -it python:3.11 python3

# Quick Ubuntu shell
docker run --rm -it ubuntu:22.04 bash

# Run a Python script from your current directory
docker run --rm -v $(pwd):/app -w /app python:3.11 python3 script.py
```


### Debugging a failed build

```bash
# Build and stop at a specific layer (use the layer ID from build output)
docker run -it <layer-id> bash

# Build with no cache (force full rebuild)
docker build --no-cache -t myapp .
```


## Docker Registries

### Docker Hub (public default)

```bash
# Login
docker login

# Push an image
docker tag myapp:latest myusername/myapp:latest
docker push myusername/myapp:latest

# Pull someone else's image
docker pull myusername/myapp:latest
```

### GitHub Container Registry (GHCR)

```bash
# Login with a Personal Access Token
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Tag and push
docker tag myapp:latest ghcr.io/username/myapp:latest
docker push ghcr.io/username/myapp:latest
```

### NVIDIA NGC (for AI/robotics images)

```bash
# Login (requires NVIDIA developer account)
docker login nvcr.io

# Pull Isaac Sim
docker pull nvcr.io/nvidia/isaac-sim:5.1.0
```


## Managing Resources

```bash
# Show disk usage by Docker
docker system df

# Real-time resource usage (all containers)
docker stats

# Full cleanup — remove stopped containers, unused images, unused volumes, unused networks
docker system prune

# Also remove unused images (frees the most space)
docker system prune -a

# Remove only unused volumes
docker volume prune

# Limit container resources at runtime
docker run --memory="1g" --cpus="2.0" myapp
```


## Troubleshooting

### `Got permission denied while trying to connect to the Docker daemon socket`

**Fix (Linux / WSL2):** Add yourself to the docker group:

```bash
sudo usermod -aG docker $USER
newgrp docker
```


### `Cannot connect to the Docker daemon` (WSL2 without Docker Desktop)

Docker daemon is not running:

```bash
sudo service docker start
# or (with systemd):
sudo systemctl start docker
```


### Container exits immediately

```bash
# Check the exit logs
docker logs <container-name>

# Run interactively to debug
docker run -it myapp bash
```


### `port is already allocated`

Another process (or container) is already using that port:

```bash
# Find what's using the port
sudo lsof -i :8080        # Linux
netstat -aon | findstr 8080  # Windows PowerShell

# Stop the conflicting container
docker ps
docker stop <name>
```


### Out of disk space

```bash
docker system prune -a --volumes
```


### `image not found` / `pull access denied`

- Check the image name and tag spelling
- If a private registry: `docker login <registry-url>` first
- If NVIDIA NGC: `docker login nvcr.io`


### `CUDA not available` inside container

1. Make sure `nvidia-container-toolkit` is installed (see above)
2. Make sure you used `--gpus all` when running
3. Verify: `docker run --rm --gpus all nvidia/cuda:12.6.0-base-ubuntu22.04 nvidia-smi`


## Quick Reference Card

```
┌───────────────────────┬─────────────────────────────────────────┐
│ Action                │ Command                                 │
├───────────────────────┼─────────────────────────────────────────┤
│ Pull image            │ docker pull <image>                     │
│ List images           │ docker images                           │
│ Remove image          │ docker rmi <image>                      │
│ Run container         │ docker run <image>                      │
│ Run interactive       │ docker run -it <image> bash             │
│ Run detached          │ docker run -d <image>                   │
│ Run with port         │ docker run -p 8080:80 <image>           │
│ Run with volume       │ docker run -v /host:/container <image>  │
│ Run with GPU          │ docker run --gpus all <image>           │
│ List running          │ docker ps                               │
│ List all              │ docker ps -a                            │
│ Stop container        │ docker stop <name>                      │
│ Remove container      │ docker rm <name>                        │
│ Shell in container    │ docker exec -it <name> bash             │
│ View logs             │ docker logs -f <name>                   │
│ Build image           │ docker build -t <name> .                │
│ Compose up            │ docker compose up -d                    │
│ Compose down          │ docker compose down                     │
│ Compose logs          │ docker compose logs -f                  │
│ System cleanup        │ docker system prune -a                  │
│ Disk usage            │ docker system df                        │
│ Resource stats        │ docker stats                            │
└───────────────────────┴─────────────────────────────────────────┘
```


## Additional Resources

- [Docker Official Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/)
- [NVIDIA NGC — AI/Robotics Images](https://catalog.ngc.nvidia.com/)
- [Official ROS Docker Images](https://hub.docker.com/r/osrf/ros)
- [Docker Compose Reference](https://docs.docker.com/compose/reference/)
- [Play with Docker (online playground)](https://labs.play-with-docker.com/)


*Guide written for Docker Engine 27.x / Docker Desktop 4.x — Ubuntu · Windows 11 · WSL2. Last updated: May 2026.*
