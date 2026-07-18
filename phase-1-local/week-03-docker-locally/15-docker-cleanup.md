# 15 - Docker Cleanup

Docker cleanup means removing unused Docker resources from your machine.

Over time, Docker can use a lot of disk space because of:

```text id="29nlb2"
Stopped containers
Unused images
Dangling images
Unused volumes
Unused networks
Build cache
Old containers from labs
```

## Why Do We Need Docker Cleanup?

When you practice Docker a lot, your machine may become full.

You may create many containers and images while testing.

Example:

```text id="8cw9tp"
docker build
docker run
docker compose up
docker compose down
docker build again
docker run again
```

After some time, unused Docker resources stay on your machine.

Cleanup helps you:

```text id="kqne3g"
Free disk space
Remove old containers
Remove unused images
Remove unused volumes
Keep Docker clean
Avoid confusion from old resources
```

## Check Docker Disk Usage

Before deleting anything, check Docker disk usage.

```bash id="qjkr4m"
docker system df
```

This shows disk usage for:

```text id="4amj2s"
Images
Containers
Local volumes
Build cache
```

More detailed output:

```bash id="lznk59"
docker system df -v
```

## Check Running Containers

Show running containers:

```bash id="vkbkzn"
docker ps
```

Show all containers, including stopped ones:

```bash id="zkcj20"
docker ps -a
```

Stopped containers are common after testing.

## Remove One Container

Stop container:

```bash id="86ykpy"
docker stop CONTAINER_NAME
```

Remove container:

```bash id="rwbtnl"
docker rm CONTAINER_NAME
```

Example:

```bash id="c0r2eb"
docker stop web
docker rm web
```

## Force Remove a Container

If you want to stop and remove a container directly:

```bash id="hpyud8"
docker rm -f CONTAINER_NAME
```

Example:

```bash id="w5pyi3"
docker rm -f web
```

Be careful because this removes the container immediately.

## Remove All Stopped Containers

```bash id="gxmg56"
docker container prune
```

Docker will ask for confirmation.

This removes containers that are not running.

## Remove All Containers

Stop all running containers:

```bash id="yhghrr"
docker stop $(docker ps -q)
```

Remove all containers:

```bash id="7z7zp3"
docker rm $(docker ps -aq)
```

Or force remove all containers:

```bash id="77kw24"
docker rm -f $(docker ps -aq)
```

Use this carefully.

## Check Docker Images

List images:

```bash id="5llang"
docker images
```

or:

```bash id="q3o24l"
docker image ls
```

You may see old images from previous builds.

## Remove One Image

```bash id="j8ymzt"
docker rmi IMAGE_NAME:TAG
```

Example:

```bash id="4wsvmb"
docker rmi my-app:1.0.0
```

You can also remove by image ID:

```bash id="y4aj6n"
docker rmi IMAGE_ID
```

## Force Remove an Image

```bash id="7dckps"
docker rmi -f IMAGE_NAME:TAG
```

Use force only when you understand what depends on the image.

## Remove Dangling Images

Dangling images are images without a name or tag.

They may appear as:

```text id="shn1gw"
<none>   <none>
```

Remove dangling images:

```bash id="epdzgu"
docker image prune
```

## Remove All Unused Images

Remove all images not used by containers:

```bash id="y8fdb7"
docker image prune -a
```

This can remove many images.

Docker may need to download them again later.

## Check Docker Volumes

List volumes:

```bash id="m1xw2s"
docker volume ls
```

Inspect a volume:

```bash id="o64ftq"
docker volume inspect VOLUME_NAME
```

Volumes can contain important data.

Examples:

```text id="3sj6tj"
Database data
Uploaded files
Application data
PostgreSQL data
Redis data
```

## Remove One Volume

```bash id="7zcao8"
docker volume rm VOLUME_NAME
```

Example:

```bash id="lshq1j"
docker volume rm postgres-data
```

Only remove volumes when you are sure the data is not important.

## Remove Unused Volumes

```bash id="spjj8q"
docker volume prune
```

This removes volumes not used by any container.

Be careful.

Unused volume does not always mean unimportant data.

## Check Docker Networks

List networks:

```bash id="968eok"
docker network ls
```

Inspect a network:

```bash id="ny2g72"
docker network inspect NETWORK_NAME
```

## Remove One Network

```bash id="gkdp5t"
docker network rm NETWORK_NAME
```

Example:

```bash id="zmezf3"
docker network rm app-network
```

You cannot remove a network if containers are still using it.

## Remove Unused Networks

```bash id="sb6v16"
docker network prune
```

This removes networks not used by containers.

## Remove Build Cache

Docker keeps build cache to make future builds faster.

But it can use disk space.

Remove build cache:

```bash id="hw7lz1"
docker builder prune
```

Remove all build cache:

```bash id="blprri"
docker builder prune -a
```

Use this if Docker builds are taking too much space.

## Docker System Prune

`docker system prune` removes multiple unused resources.

```bash id="732vuq"
docker system prune
```

It removes:

```text id="g2il8t"
Stopped containers
Unused networks
Dangling images
Build cache
```

It does not remove volumes by default.

## Docker System Prune with Volumes

To also remove unused volumes:

```bash id="3epqgw"
docker system prune --volumes
```

Be very careful.

This can delete database data and uploaded files if they are in unused volumes.

## Aggressive Cleanup

This is a strong cleanup command:

```bash id="cbbqlx"
docker system prune -a --volumes
```

It removes:

```text id="t8ixcd"
Stopped containers
Unused networks
Unused images
Build cache
Unused volumes
```

Use this only when you are sure you do not need old Docker data.

## Safe Cleanup Workflow

A safer cleanup order:

```bash id="2f3dhe"
docker system df

docker ps -a
docker images
docker volume ls
docker network ls

docker container prune
docker image prune
docker network prune
docker builder prune
```

Only remove volumes after checking them:

```bash id="q7e25m"
docker volume ls
docker volume inspect VOLUME_NAME
docker volume rm VOLUME_NAME
```

## Docker Compose Cleanup

If you started containers using Docker Compose, clean them using Compose.

Stop and remove containers:

```bash id="y39093"
docker compose down
```

Remove containers and networks:

```bash id="rzr0fp"
docker compose down
```

Remove volumes too:

```bash id="92y0xh"
docker compose down -v
```

Be careful with `-v`.

It deletes Compose volumes.

## Docker Compose with Images Cleanup

Remove containers, networks, and images created by Compose:

```bash id="e2ikqq"
docker compose down --rmi local
```

Remove volumes also:

```bash id="m3fizh"
docker compose down --rmi local -v
```

## Important Difference

```text id="dd1d8z"
docker compose down     → Removes containers and networks
docker compose down -v  → Also removes volumes
```

Use `-v` only when you do not need the data.

## Example: Clean a Docker Compose Lab

Project:

```text id="9q8g7l"
flask-redis-lab/
├── docker-compose.yml
├── app.py
└── Dockerfile
```

Stop and remove lab containers:

```bash id="0jvkxt"
docker compose down
```

If you want to delete lab data too:

```bash id="a7du67"
docker compose down -v
```

Then check:

```bash id="hy5xoc"
docker ps -a
docker volume ls
```

## Remove Containers by Name Pattern

List containers:

```bash id="qk0xhe"
docker ps -a
```

Remove specific containers:

```bash id="0ba7gp"
docker rm -f web redis postgres
```

Remove containers from a lab:

```bash id="2hknvj"
docker rm -f flask-app redis-db postgres-db
```

## Remove Images by Name

Remove app images:

```bash id="j62gnl"
docker rmi my-app:1.0.0
docker rmi my-app:1.1.0
```

Remove old lab images:

```bash id="j6svyn"
docker rmi flask-healthcheck:1.0.0
docker rmi flask-multistage:1.0.0
```

## Remove Everything from a Lab

Example lab cleanup:

```bash id="lcf7dt"
docker rm -f web redis postgres
docker network rm app-network
docker volume rm postgres-data uploads-data
docker rmi my-app:1.0.0
```

Check after cleanup:

```bash id="zk8i57"
docker ps -a
docker images
docker volume ls
docker network ls
```

## Important Warning About Volumes

Volumes are the most dangerous part of cleanup.

A stopped container can be recreated.

An image can be rebuilt.

But volume data may be important.

```text id="cbagof"
Deleting a database volume can delete the database data.
Deleting an uploads volume can delete uploaded files.
```

Always check before deleting volumes.

## Backup Before Removing Volume

Backup a volume:

```bash id="davwcx"
docker run --rm \
  -v uploads-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/uploads-backup.tar.gz -C /data .
```

Then remove the volume:

```bash id="jzlowi"
docker volume rm uploads-data
```

## Restore Volume Backup

```bash id="npm6xg"
docker run --rm \
  -v uploads-data:/data \
  -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/uploads-backup.tar.gz"
```

## Common Beginner Mistakes

### Deleting Volumes Without Checking

Bad:

```bash id="z7h6lo"
docker system prune -a --volumes
```

without checking volume data.

Better:

```bash id="i51mvm"
docker volume ls
docker volume inspect VOLUME_NAME
```

### Thinking docker rm Deletes Volumes

This removes the container:

```bash id="pq03gt"
docker rm web
```

But named volumes usually remain.

Check:

```bash id="kv7424"
docker volume ls
```

### Thinking docker rmi Deletes Containers

This removes an image:

```bash id="w1u9ib"
docker rmi nginx:alpine
```

It does not remove running containers.

Check containers:

```bash id="09x1qw"
docker ps -a
```

### Removing Images Used by Containers

If a container uses an image, Docker may not remove it.

Fix:

```bash id="w0k7ng"
docker rm -f CONTAINER_NAME
docker rmi IMAGE_NAME:TAG
```

### Cleaning Too Much

Do not run aggressive cleanup randomly.

Bad habit:

```bash id="u2ztid"
docker system prune -a --volumes
```

Better habit:

```bash id="j10urc"
docker system df
docker ps -a
docker images
docker volume ls
```

Then delete only what you understand.

## Safe Daily Cleanup

For normal practice, this is usually safe:

```bash id="5ycb42"
docker container prune
docker image prune
docker network prune
docker builder prune
```

This avoids deleting volumes by default.

## Full Cleanup for Learning Labs

If you are sure all lab data can be deleted:

```bash id="j8ebev"
docker rm -f $(docker ps -aq)
docker system prune -a
```

If you also want to delete volumes:

```bash id="qbr1me"
docker system prune -a --volumes
```

Use the volume command only when you do not need any saved data.

## Useful Commands

Check Docker disk usage:

```bash id="8s7782"
docker system df
```

Detailed disk usage:

```bash id="g175xf"
docker system df -v
```

Remove stopped containers:

```bash id="xvxg3q"
docker container prune
```

Remove dangling images:

```bash id="auqh3h"
docker image prune
```

Remove unused images:

```bash id="gu9iit"
docker image prune -a
```

Remove unused networks:

```bash id="rwjmbl"
docker network prune
```

Remove unused volumes:

```bash id="91gopi"
docker volume prune
```

Remove build cache:

```bash id="5jy2t3"
docker builder prune
```

General cleanup:

```bash id="bkc0ec"
docker system prune
```

Aggressive cleanup:

```bash id="ukvphx"
docker system prune -a --volumes
```

## Summary

```text id="19tl6c"
docker system df        → Check Docker disk usage
docker container prune  → Remove stopped containers
docker image prune      → Remove dangling images
docker image prune -a   → Remove unused images
docker network prune    → Remove unused networks
docker volume prune     → Remove unused volumes
docker builder prune    → Remove build cache
docker system prune     → Remove multiple unused resources
```

```text id="p82ziy"
Containers can be recreated.
Images can be rebuilt.
Volumes may contain important data.
Always check volumes before deleting them.
```

> Docker cleanup keeps your machine clean by removing unused containers, images, networks, volumes, and build cache. Be careful with volumes because they may contain important data.

