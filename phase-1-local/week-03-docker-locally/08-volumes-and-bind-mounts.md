# 08 - Volumes and Bind Mounts

Docker containers are temporary by design.

If you remove a container, the data inside it can be lost.

To keep data safe, Docker uses:

```text id="ns7bq1"
Volumes
Bind Mounts
```

## Simple Explanation

```text id="7nsy0u"
Volume      → Docker-managed persistent storage
Bind Mount  → Mount a folder from your host machine into the container
```

Example:

```text id="ovaf0p"
Container removed
        ↓
Data still exists in volume
```

## Why Do We Need Volumes?

Containers should not store important data only inside the container filesystem.

Bad:

```text id="yq5m6b"
Container
└── Database files
```

If the container is deleted, the data may be deleted too.

Better:

```text id="n0b5so"
Container
└── Mounted Volume
    └── Database files
```

Now the data is stored outside the container lifecycle.

## Container Data Problem

Run a container:

```bash id="cff1zm"
docker run -d --name test-nginx nginx:alpine
```

Create a file inside it:

```bash id="9cp9zz"
docker exec test-nginx sh -c "echo hello > /tmp/test.txt"
```

Check the file:

```bash id="om4k4f"
docker exec test-nginx cat /tmp/test.txt
```

Remove the container:

```bash id="q1u41j"
docker rm -f test-nginx
```

The file is gone because it was inside the container.

## Docker Volume

A **Docker volume** is storage managed by Docker.

Docker stores it on your machine, but Docker controls the location.

Create a volume:

```bash id="ray2ms"
docker volume create app-data
```

List volumes:

```bash id="oao5do"
docker volume ls
```

Inspect volume:

```bash id="ary105"
docker volume inspect app-data
```

Remove volume:

```bash id="mkri4e"
docker volume rm app-data
```

## Run Container with Volume

Example with Nginx:

```bash id="xaapdi"
docker run -d \
  --name nginx-volume \
  -p 8080:80 \
  -v nginx-data:/usr/share/nginx/html \
  nginx:alpine
```

Meaning:

```text id="azn0id"
nginx-data              → Docker volume name
/usr/share/nginx/html   → Path inside the container
```

The volume is mounted into the container.

## Volume Diagram

```text id="ydo9nd"
Docker Volume: nginx-data
        ↓
Mounted inside container
        ↓
/usr/share/nginx/html
```

## Test Volume Persistence

Run a container with a volume:

```bash id="s2ps2r"
docker run -d \
  --name volume-test \
  -v app-data:/data \
  alpine sleep infinity
```

Create a file:

```bash id="35kqaw"
docker exec volume-test sh -c "echo persistent-data > /data/file.txt"
```

Check it:

```bash id="imruoo"
docker exec volume-test cat /data/file.txt
```

Remove the container:

```bash id="4rm3gk"
docker rm -f volume-test
```

Create a new container using the same volume:

```bash id="g5cmzw"
docker run --rm \
  -v app-data:/data \
  alpine cat /data/file.txt
```

You should see:

```text id="ej5i08"
persistent-data
```

This proves that the data stayed in the volume.

## Named Volume

A **named volume** has a clear name.

Example:

```bash id="iibcoi"
docker volume create postgres-data
```

Use it:

```bash id="l39qx3"
docker run -d \
  --name postgres-db \
  -e POSTGRES_PASSWORD=123abood \
  -v postgres-data:/var/lib/postgresql/data \
  postgres:16-alpine
```

Named volumes are good for:

```text id="g6ix0p"
Databases
Application uploads
Persistent app data
Docker Compose services
```

## Anonymous Volume

An anonymous volume has no custom name.

Example:

```bash id="wdgddw"
docker run -d \
  --name app \
  -v /data \
  alpine sleep infinity
```

Docker creates a random volume name.

This is less clear.

For learning and real projects, named volumes are easier to manage.

## Bind Mount

A **bind mount** connects a folder or file from your host machine to the container.

Example:

```bash id="bd5hr2"
docker run -d \
  --name nginx-bind \
  -p 8080:80 \
  -v $(pwd)/html:/usr/share/nginx/html \
  nginx:alpine
```

Meaning:

```text id="g45z13"
$(pwd)/html             → Folder on your machine
/usr/share/nginx/html   → Folder inside the container
```

## Bind Mount Diagram

```text id="y09j3q"
Host Machine Folder
./html
  ↓
Container Folder
/usr/share/nginx/html
```

If you edit files on your host machine, the container sees the change.

## Create Bind Mount Example

Create folder:

```bash id="db8nsv"
mkdir html
```

Create file:

```bash id="q3m591"
echo "Hello from bind mount" > html/index.html
```

Run Nginx:

```bash id="v7qfvu"
docker run -d \
  --name nginx-bind \
  -p 8080:80 \
  -v $(pwd)/html:/usr/share/nginx/html \
  nginx:alpine
```

Open:

```text id="qim5fm"
http://localhost:8080
```

You should see:

```text id="bh3j57"
Hello from bind mount
```

Now edit the file:

```bash id="mzftqr"
echo "Updated from host machine" > html/index.html
```

Refresh the browser.

The page changes without rebuilding the image.

## Volume vs Bind Mount

| Volume                       | Bind Mount                      |
| ---------------------------- | ------------------------------- |
| Managed by Docker            | Managed by host filesystem      |
| Stored in Docker area        | Stored anywhere on your machine |
| Good for persistent app data | Good for development            |
| Easier for databases         | Easier for live code editing    |
| More portable                | Depends on host path            |

## When to Use Volumes

Use volumes for:

```text id="f6w8ez"
Database data
Application uploads
Persistent container data
Production containers
Docker Compose services
```

Example:

```bash id="fsmrie"
-v postgres-data:/var/lib/postgresql/data
```

## When to Use Bind Mounts

Use bind mounts for:

```text id="yx55ge"
Development
Editing code live
Mounting config files
Mounting local project folder
Testing files from host
```

Example:

```bash id="zkhxpk"
-v $(pwd):/app
```

This mounts your current project folder into `/app` inside the container.

## Important Difference

With a bind mount, the host path matters.

Example:

```bash id="4e3ay9"
-v /home/abood/my-app:/app
```

If this path does not exist or is wrong, the container may not behave as expected.

With a named volume:

```bash id="27vjc5"
-v app-data:/app/data
```

Docker manages the storage.

## Using --mount Syntax

Docker also supports `--mount`.

Volume example:

```bash id="422ujv"
docker run -d \
  --name nginx-volume \
  --mount source=nginx-data,target=/usr/share/nginx/html \
  nginx:alpine
```

Bind mount example:

```bash id="d7hddq"
docker run -d \
  --name nginx-bind \
  --mount type=bind,source="$(pwd)/html",target=/usr/share/nginx/html \
  nginx:alpine
```

`--mount` is longer but clearer.

## -v vs --mount

| Option    | Meaning              |
| --------- | -------------------- |
| `-v`      | Short syntax         |
| `--mount` | More explicit syntax |

Example with `-v`:

```bash id="t8bl8u"
-v app-data:/data
```

Example with `--mount`:

```bash id="y0qtyg"
--mount source=app-data,target=/data
```

Both work.

## Read-Only Mount

You can mount a file or folder as read-only.

Example:

```bash id="g9hkae"
docker run -d \
  --name nginx-readonly \
  -p 8080:80 \
  -v $(pwd)/html:/usr/share/nginx/html:ro \
  nginx:alpine
```

The `:ro` means read-only.

```text id="ss8jtx"
Container can read files
Container cannot change files
```

This is useful for configuration files.

## Example with Config File

```bash id="xqan5q"
docker run -d \
  --name app \
  -v $(pwd)/config.yml:/app/config.yml:ro \
  my-app:1.0.0
```

The container can read the config, but cannot modify it.

## Docker Compose with Volume

Example `docker-compose.yml`:

```yaml id="wvvs6q"
services:
  postgres:
    image: postgres:16-alpine
    container_name: postgres-db
    environment:
      POSTGRES_USER: abood
      POSTGRES_PASSWORD: 123abood
      POSTGRES_DB: appdb
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

Run:

```bash id="nc27bu"
docker compose up -d
```

The database data is stored in the named volume `postgres-data`.

## Docker Compose with Bind Mount

Example for development:

```yaml id="7wxmm2"
services:
  web:
    image: python:3.12-slim
    container_name: dev-app
    working_dir: /app
    volumes:
      - .:/app
    command: python app.py
```

Meaning:

```text id="2l8u7t"
Current folder on host → /app inside container
```

This is useful while developing because code changes are visible inside the container.

## Docker Compose with Read-Only Bind Mount

```yaml id="t1grm8"
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html:ro
```

The container can serve the files but cannot change them.

## Database Volume Example

PostgreSQL stores data inside:

```text id="u60dpw"
/var/lib/postgresql/data
```

Run PostgreSQL with persistent volume:

```bash id="r603cn"
docker run -d \
  --name postgres-db \
  -e POSTGRES_USER=abood \
  -e POSTGRES_PASSWORD=123abood \
  -e POSTGRES_DB=mydb \
  -v postgres-data:/var/lib/postgresql/data \
  postgres:16-alpine
```

Stop and remove the container:

```bash id="5yvd20"
docker rm -f postgres-db
```

Run it again with the same volume:

```bash id="bjrmiy"
docker run -d \
  --name postgres-db \
  -e POSTGRES_USER=abood \
  -e POSTGRES_PASSWORD=123abood \
  -e POSTGRES_DB=mydb \
  -v postgres-data:/var/lib/postgresql/data \
  postgres:16-alpine
```

The database data remains.

## Flask Uploads Example

A Flask app may save uploaded files in:

```text id="rjr6di"
/app/uploads
```

Use a volume:

```bash id="wy8p2d"
docker run -d \
  --name uploader \
  -p 8080:8080 \
  -v uploads-data:/app/uploads \
  flask-uploader:1.0.0
```

Now uploaded files stay even if the container is recreated.

## Backup a Docker Volume

You can backup a volume using a temporary container.

Example:

```bash id="ks6xd9"
docker run --rm \
  -v uploads-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/uploads-backup.tar.gz -C /data .
```

Meaning:

```text id="vekgbq"
uploads-data → mounted at /data
current folder → mounted at /backup
tar creates backup file on host
```

## Restore a Docker Volume

Restore backup into a volume:

```bash id="wb0ekd"
docker run --rm \
  -v uploads-data:/data \
  -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/uploads-backup.tar.gz"
```

## Remove Volumes

Remove one volume:

```bash id="wlka5v"
docker volume rm uploads-data
```

Remove unused volumes:

```bash id="6p75uw"
docker volume prune
```

Be careful.

Removing a volume can delete important data.

## Check What Container Uses

Inspect container mounts:

```bash id="0qwi7e"
docker inspect CONTAINER_NAME
```

Filter mounts:

```bash id="ced08e"
docker inspect CONTAINER_NAME --format='{{json .Mounts}}'
```

You can also use:

```bash id="i71895"
docker volume inspect VOLUME_NAME
```

## Common Beginner Mistakes

### Storing Important Data Only Inside Container

Bad:

```text id="qp72ku"
Database files only inside container
```

Better:

```text id="lfwk05"
Use a named volume for database data
```

### Deleting Volumes by Mistake

This command removes unused volumes:

```bash id="vxg1e8"
docker volume prune
```

Check volumes first:

```bash id="k2q25b"
docker volume ls
```

### Using Wrong Host Path

Bad:

```bash id="fmzov8"
-v ./wrong-folder:/app
```

If the path is wrong, the app may not find files.

Check current path:

```bash id="0q95x2"
pwd
ls -la
```

### Mounting Over Important Container Files

If you mount an empty host folder over a container folder, it can hide files that were already in the image.

Example:

```bash id="m8zqkr"
-v $(pwd)/empty:/app
```

If `/app` had files inside the image, they may look missing because the bind mount covers them.

### Using Bind Mounts in Production Without Need

Bind mounts depend on the host machine path.

For production, named volumes are usually cleaner.

## Useful Commands

Create volume:

```bash id="7mt7gt"
docker volume create my-volume
```

List volumes:

```bash id="2pna2y"
docker volume ls
```

Inspect volume:

```bash id="irvl9s"
docker volume inspect my-volume
```

Remove volume:

```bash id="mbb62d"
docker volume rm my-volume
```

Run with volume:

```bash id="oqkis4"
docker run -v my-volume:/data alpine
```

Run with bind mount:

```bash id="rd8ndh"
docker run -v $(pwd):/app alpine
```

Remove unused volumes:

```bash id="lzr22t"
docker volume prune
```

Check container mounts:

```bash id="lfbsuz"
docker inspect CONTAINER_NAME
```

## Summary

```text id="2m0wqc"
Volume      → Docker-managed persistent storage
Bind Mount  → Host folder mounted into container
Named Volume → Volume with clear name
Anonymous Volume → Volume with random Docker name
Read-only mount → Container can read but not modify
```

```text id="3eunef"
Use volumes for persistent app data.
Use bind mounts for development and local files.
Use read-only mounts for config files.
Do not store important data only inside containers.
```

> Volumes and bind mounts allow Docker containers to store and share data outside the container lifecycle.

