# 03 - Container Lifecycle

A **container lifecycle** means the stages a Docker container goes through from creation until deletion.

A container is not always running.

It can be:

```text id="r93s8q"
Created
Running
Paused
Stopped
Deleted
```

## Simple Explanation

A Docker image is like a template.

A Docker container is a running or stopped copy of that image.

```text id="6pi6u9"
Docker Image
     ↓
Docker Container
     ↓
Container Lifecycle
```

Example:

```text id="x52dfl"
nginx image → nginx container
```

## Why Learn Container Lifecycle?

You need to understand container lifecycle because Docker containers are not permanent machines.

They can be started, stopped, restarted, removed, and recreated.

This helps you understand:

```text id="g8x2mk"
How containers run
How to stop containers safely
How to restart containers
How to debug stopped containers
How to clean unused containers
How Docker behaves in real projects
```

## Main Container Lifecycle States

```text id="r2g4yb"
Image
  ↓
Created
  ↓
Running
  ↓
Stopped
  ↓
Removed
```

More detailed:

```text id="i5mczz"
Created → Running → Paused → Running → Stopped → Removed
```

## 1. Image

Before creating a container, you need an image.

Example image:

```text id="ip1v3a"
nginx:alpine
```

Pull the image:

```bash id="s5wfvi"
docker pull nginx:alpine
```

List images:

```bash id="tt8gvi"
docker images
```

## 2. Created State

A container is in **Created** state when Docker creates it but does not start it yet.

Create a container:

```bash id="dm29np"
docker create --name my-nginx nginx:alpine
```

Check containers:

```bash id="wzugsj"
docker ps -a
```

You will see the container exists, but it is not running yet.

```text id="ifz04x"
STATUS: Created
```

## 3. Running State

A container is in **Running** state when the main process inside the container is running.

Start the created container:

```bash id="fvlk6d"
docker start my-nginx
```

Check running containers:

```bash id="yfkpky"
docker ps
```

Now the container is running.

```text id="igam7c"
STATUS: Up
```

## Create and Run Directly

Most of the time, you use `docker run`.

`docker run` does two things:

```text id="e10qgg"
docker create
docker start
```

Example:

```bash id="sebpva"
docker run -d --name web -p 8080:80 nginx:alpine
```

Meaning:

```text id="rt06yd"
-d          → Run in background
--name web  → Container name is web
-p 8080:80  → Host port 8080 to container port 80
nginx:alpine → Image name
```

Open in browser:

```text id="bdfokr"
http://localhost:8080
```

## 4. Paused State

A paused container is still alive, but its processes are frozen.

Pause a container:

```bash id="ftwwpt"
docker pause web
```

Check:

```bash id="reeb27"
docker ps
```

You may see:

```text id="knkj1o"
STATUS: Up ... (Paused)
```

Unpause it:

```bash id="y3lp7s"
docker unpause web
```

Use pause when you want to temporarily freeze a container without stopping it.

## 5. Stopped State

A stopped container is not running, but it still exists.

Stop a container safely:

```bash id="mm3tk8"
docker stop web
```

Check all containers:

```bash id="qqnnmb"
docker ps -a
```

You may see:

```text id="f736dh"
STATUS: Exited
```

A stopped container can be started again:

```bash id="fjo64o"
docker start web
```

## Stop vs Kill

### docker stop

```bash id="e8d78s"
docker stop web
```

This stops the container safely.

Docker gives the container time to shut down properly.

### docker kill

```bash id="g3t9gx"
docker kill web
```

This stops the container immediately.

Use `kill` only when the container is stuck and does not stop normally.

## 6. Restarting a Container

Restart means stop and start again.

```bash id="iidrg0"
docker restart web
```

This is useful when:

```text id="r9fecw"
You changed configuration
The app is stuck
You want to reload the container
```

## 7. Removed State

When you remove a container, it is deleted from Docker.

First stop it:

```bash id="ek97qu"
docker stop web
```

Then remove it:

```bash id="jbry06"
docker rm web
```

Or force remove it:

```bash id="n3m532"
docker rm -f web
```

Be careful.

Removing a container deletes the container itself.

## Container Lifecycle Diagram

```text id="rbxtge"
docker pull
    ↓
Image
    ↓ docker create
Created
    ↓ docker start
Running
    ↓ docker pause
Paused
    ↓ docker unpause
Running
    ↓ docker stop
Stopped
    ↓ docker rm
Removed
```

## Important Command Difference

| Command          | Meaning                        |
| ---------------- | ------------------------------ |
| `docker create`  | Create container only          |
| `docker start`   | Start existing container       |
| `docker run`     | Create and start container     |
| `docker stop`    | Stop container safely          |
| `docker kill`    | Stop container immediately     |
| `docker restart` | Stop and start again           |
| `docker rm`      | Remove stopped container       |
| `docker rm -f`   | Force remove running container |

## Check Container Status

Show running containers:

```bash id="srrrnz"
docker ps
```

Show all containers:

```bash id="fyfx8r"
docker ps -a
```

Show only container IDs:

```bash id="du3t6h"
docker ps -q
```

Show all container IDs:

```bash id="h0rzkl"
docker ps -aq
```

## Inspect a Container

Use `docker inspect` to see detailed container information.

```bash id="z9d3qo"
docker inspect web
```

This shows:

```text id="p0j7mc"
Container ID
Image
Network settings
Mounts
Environment variables
State
IP address
```

## View Container Logs

Logs help you understand what happened inside the container.

```bash id="uutkel"
docker logs web
```

Follow logs live:

```bash id="hqjz2k"
docker logs -f web
```

Show last lines:

```bash id="zsb77b"
docker logs --tail 20 web
```

## Execute Commands Inside a Running Container

Use `docker exec` to run a command inside a running container.

```bash id="gp335j"
docker exec -it web sh
```

Meaning:

```text id="anjtgq"
exec → Run command inside container
-it  → Interactive terminal
sh   → Shell
```

Exit the container shell:

```bash id="fu6crs"
exit
```

## Run a Temporary Container

Sometimes you need a container only for testing.

Example:

```bash id="wtiiv0"
docker run --rm alpine echo "Hello from Alpine"
```

Meaning:

```text id="z62sn7"
--rm → Remove the container automatically after it exits
```

This is useful for short tasks.

## Detached vs Interactive Containers

### Detached Mode

Detached mode runs the container in the background.

```bash id="mkw1mg"
docker run -d --name web nginx:alpine
```

Use this for servers.

### Interactive Mode

Interactive mode opens a shell inside the container.

```bash id="bfsoqi"
docker run -it --name test alpine sh
```

Use this for testing and debugging.

## Container Main Process

A container stays running while its main process is running.

Example:

```bash id="b7jg12"
docker run alpine echo "hello"
```

This container starts, prints `hello`, then stops.

Why?

Because the main process finished.

To keep Alpine running:

```bash id="laq3z4"
docker run -d --name alpine-test alpine sleep infinity
```

Now the container stays running.

## Restart Policy

A restart policy tells Docker what to do if the container stops.

Example:

```bash id="pm5uy2"
docker run -d --name web --restart unless-stopped nginx:alpine
```

Common restart policies:

```text id="w6pxfz"
no              → Do not restart automatically
always          → Always restart
unless-stopped  → Restart unless manually stopped
on-failure      → Restart only if it exits with error
```

## Example with Restart Policy

```bash id="e78bd0"
docker run -d \
  --name web \
  --restart unless-stopped \
  -p 8080:80 \
  nginx:alpine
```

This is useful for services that should keep running.

## Clean Up Containers

Stop one container:

```bash id="krlajq"
docker stop web
```

Remove one container:

```bash id="fke24p"
docker rm web
```

Stop all running containers:

```bash id="yqwl85"
docker stop $(docker ps -q)
```

Remove all stopped containers:

```bash id="p6xafp"
docker container prune
```

Remove all containers:

```bash id="gpbih8"
docker rm -f $(docker ps -aq)
```

Use cleanup commands carefully.

## Practical Lab

Run Nginx:

```bash id="h1e4xi"
docker run -d --name lifecycle-nginx -p 8080:80 nginx:alpine
```

Check it:

```bash id="pf8b6f"
docker ps
```

Open:

```text id="ro5hz3"
http://localhost:8080
```

Pause it:

```bash id="m8mx2i"
docker pause lifecycle-nginx
```

Unpause it:

```bash id="a2oljt"
docker unpause lifecycle-nginx
```

Restart it:

```bash id="hr5w09"
docker restart lifecycle-nginx
```

View logs:

```bash id="lm7hpk"
docker logs lifecycle-nginx
```

Stop it:

```bash id="npu1q9"
docker stop lifecycle-nginx
```

Start it again:

```bash id="bclfcx"
docker start lifecycle-nginx
```

Remove it:

```bash id="sucmn4"
docker rm -f lifecycle-nginx
```

## Common Beginner Mistakes

### Thinking a Stopped Container Is Deleted

A stopped container still exists.

Check:

```bash id="qf6ghf"
docker ps -a
```

Remove it:

```bash id="dj30xp"
docker rm CONTAINER_NAME
```

### Using docker ps Only

`docker ps` shows only running containers.

To see stopped containers:

```bash id="w5zohi"
docker ps -a
```

### Using docker run Again and Again

If you run:

```bash id="rj40cg"
docker run --name web nginx:alpine
```

and then try it again with the same name, Docker will complain because the name already exists.

Fix:

```bash id="sp29yh"
docker rm web
```

Or use another name.

### Forgetting Port Mapping

This runs Nginx, but you cannot access it from the browser:

```bash id="hpct47"
docker run -d --name web nginx:alpine
```

Better:

```bash id="rdzflg"
docker run -d --name web -p 8080:80 nginx:alpine
```

### Removing Important Containers

Before deleting containers, check:

```bash id="ccx1tm"
docker ps -a
```

Do not remove containers that contain important data unless the data is stored in volumes.

## Summary

```text id="uid1r9"
docker create  → Create container
docker start   → Start existing container
docker run     → Create and start container
docker pause   → Freeze container
docker unpause → Resume container
docker stop    → Stop container safely
docker kill    → Stop container immediately
docker restart → Restart container
docker rm      → Remove container
docker ps      → Show running containers
docker ps -a   → Show all containers
docker logs    → Show container logs
docker exec    → Run command inside container
```

> A container lifecycle is the journey of a Docker container from creation, to running, to stopping, and finally removal.

