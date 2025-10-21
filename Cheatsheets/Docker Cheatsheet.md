Certainly! Here's a handy Docker command cheat sheet along with how to build and run a Docker image in a single command.

### Docker Command Cheat Sheet

#### Basic Commands
- **Check Docker version**:
  ```bash
  docker --version
  ```

- **List running containers**:
  ```bash
  docker ps
  ```

- **List all containers (including stopped ones)**:
  ```bash
  docker ps -a
  ```

- **List all images**:
  ```bash
  docker images
  ```

- **Remove a container**:
  ```bash
  docker rm <container_id>
  ```

- **Remove an image**:
  ```bash
  docker rmi <image_id>
  ```

#### Building and Running Containers
- **Build an image from a Dockerfile**:
  ```bash
  docker build -t <image_name>:<tag> .
  ```

- **Run a container from an image**:
  ```bash
  docker run -d -p <host_port>:<container_port> <image_name>:<tag>
  ```

#### Combine Build and Run in One Command
You can use the following command to build and run a container in one go:

```bash
docker run -d -p <host_port>:<container_port> --name <container_name> $(docker build -q -t <image_name>:<tag> .)
```

- Here, `$(docker build -q -t <image_name>:<tag> .)` builds the image and returns its ID, which is used to run the container.

#### Stopping and Starting Containers
- **Stop a running container**:
  ```bash
  docker stop <container_id>
  ```

- **Start a stopped container**:
  ```bash
  docker start <container_id>
  ```

- **Restart a container**:
  ```bash
  docker restart <container_id>
  ```

#### Docker Compose Commands
- **Start services defined in `docker-compose.yml`**:
  ```bash
  docker-compose up
  ```

- **Run services in detached mode**:
  ```bash
  docker-compose up -d
  ```

- **Stop services**:
  ```bash
  docker-compose down
  ```

- **View logs**:
  ```bash
  docker-compose logs
  ```

### Summary
This cheat sheet provides a quick reference to commonly used Docker commands. You can build and run images in a single command using the combination of `docker run` with inline image build, streamlining your workflow!
