# 13 - Docker Debugging and Logs

Docker debugging means finding why a container is not working correctly.

A container may fail because of:

```text id="srnnuk"
Wrong command
Wrong port
Missing environment variable
Bad image
Application crash
Network problem
Volume problem
Permission problem
```

## Simple Explanation

When something breaks in Docker, do not guess.

Use Docker commands to check what is happening.

```text id="a3ovom"
docker ps
docker ps -a
docker logs
docker inspect
docker exec
docker events
docker stats
```

## Why Debugging Is Important

In real projects, containers may not always work from the first try.

Debugging helps you understand:

```text id="w1fg5c"
Why a container exited
Why an app is not reachable
Why logs show errors
Why a port is not working
Why containers cannot communicate
Why volumes are not mounted
Why environment variables are missing
```

## Basic Debugging Flow

When a container is not working, follow this order:

```text id="l17046"
1. Check container status
2. Check logs
3. Inspect container configuration
4. Enter the container
5. Check ports
6. Check environment variables
7. Check network
8. Check volumes
9. Restart or rebuild if needed
```

## 1. Check Running Containers

Show running containers:

```bash id="zvwqil"
docker ps
```

This shows only containers that are currently running.

Example output:

```text id="v56fbw"
CONTAINER ID   IMAGE          COMMAND       STATUS         PORTS
abc123         nginx:alpine   nginx ...     Up 10 seconds  0.0.0.0:8080->80/tcp
```

## 2. Check All Containers

If your container is not shown in `docker ps`, it may have stopped.

Show all containers:

```bash id="dixjc3"
docker ps -a
```

This shows:

```text id="czkq1v"
Running containers
Stopped containers
Exited containers
Created containers
```

Example:

```text id="go4g2e"
STATUS: Exited (1) 5 seconds ago
```

This means the container started but crashed.

## Container Status Meaning

| Status       | Meaning                           |
| ------------ | --------------------------------- |
| `Up`         | Container is running              |
| `Exited (0)` | Container stopped successfully    |
| `Exited (1)` | Container stopped with error      |
| `Created`    | Container created but not started |
| `Restarting` | Container keeps restarting        |
| `Paused`     | Container is frozen               |

## 3. Check Container Logs

Logs are the first place to check when an app fails.

```bash id="i0iqgy"
docker logs CONTAINER_NAME
```

Example:

```bash id="bwn1rt"
docker logs web
```

Follow logs live:

```bash id="r8ns5s"
docker logs -f web
```

Show last 50 lines:

```bash id="qmk2s9"
docker logs --tail 50 web
```

Show timestamps:

```bash id="kjru69"
docker logs -t web
```

## Why Logs Matter

Logs can show:

```text id="rl7btf"
Application errors
Missing files
Wrong environment variables
Database connection errors
Port binding problems
Permission errors
Startup failures
```

Example log:

```text id="mrp3ft"
Error: REDIS_HOST environment variable is missing
```

This tells you the problem is probably configuration.

## 4. Inspect a Container

`docker inspect` shows detailed information about a container.

```bash id="ybp9ss"
docker inspect web
```

It shows:

```text id="yxwyza"
Container state
Exit code
Image
Command
Environment variables
Mounts
Networks
IP address
Port mappings
Restart policy
```

## Inspect Container State

Show container state:

```bash id="l1xkmi"
docker inspect --format='{{.State.Status}}' web
```

Show exit code:

```bash id="b27404"
docker inspect --format='{{.State.ExitCode}}' web
```

Show error message:

```bash id="f16b61"
docker inspect --format='{{.State.Error}}' web
```

## Exit Codes

Exit codes help you understand why a container stopped.

```text id="gzjxkm"
0   → Success
1   → General error
125 → Docker command failed
126 → Command cannot execute
127 → Command not found
137 → Container killed, often memory issue
143 → Container stopped by SIGTERM
```

Example:

```text id="xup0zd"
Exited (127)
```

This often means the command inside the container was not found.

## 5. Enter a Running Container

Use `docker exec` to enter a running container.

```bash id="tvbywu"
docker exec -it web sh
```

For Ubuntu-based containers, you may use:

```bash id="bkuin4"
docker exec -it web bash
```

Inside the container, you can check:

```bash id="hud4pf"
pwd
ls -la
printenv
ps aux
cat /etc/os-release
```

Exit:

```bash id="g5au2t"
exit
```

## Important Note About exec

`docker exec` works only if the container is running.

If the container exited, this will not work:

```bash id="yhswkx"
docker exec -it broken-container sh
```

For stopped containers, check logs and inspect first:

```bash id="dvuo68"
docker logs broken-container
docker inspect broken-container
```

## 6. Debug a Stopped Container

If the container exits quickly, check:

```bash id="xbtpo6"
docker ps -a
docker logs CONTAINER_NAME
docker inspect CONTAINER_NAME
```

Example:

```bash id="i2udlb"
docker logs flask-app
```

If the app crashes because of a missing dependency, logs may show:

```text id="kl3u5l"
ModuleNotFoundError: No module named 'flask'
```

Fix:

```text id="vxf419"
Add flask to requirements.txt
Rebuild the image
Run the container again
```

## 7. Check Port Mapping

Sometimes the container is running, but the app is not reachable from the browser.

Check ports:

```bash id="rd1jmu"
docker ps
```

Example good output:

```text id="xbqaur"
0.0.0.0:8080->80/tcp
```

Meaning:

```text id="vxprw6"
Host port 8080 → Container port 80
```

Open:

```text id="pb5375"
http://localhost:8080
```

## Inspect Port Mapping

```bash id="ace2vd"
docker port web
```

Example:

```text id="is325c"
80/tcp -> 0.0.0.0:8080
```

## Common Port Problem

Bad:

```bash id="jhvq5s"
docker run -d --name web nginx:alpine
```

No port mapping.

The container is running, but the browser cannot reach it.

Better:

```bash id="ywg4ys"
docker run -d --name web -p 8080:80 nginx:alpine
```

## 8. Check Environment Variables

Inside a running container:

```bash id="kt49vs"
docker exec web printenv
```

Check one variable:

```bash id="r38tcq"
docker exec web printenv APP_ENV
```

Using inspect:

```bash id="csuo4h"
docker inspect web --format='{{range .Config.Env}}{{println .}}{{end}}'
```

## Common Environment Variable Problem

Application expects:

```text id="o0sv4e"
REDIS_HOST
```

But you passed:

```text id="bej4d3"
REDIS_SERVER
```

The app will fail because the variable name is wrong.

Fix:

```bash id="eo4kwz"
docker run -e REDIS_HOST=redis my-app:1.0.0
```

## 9. Check Container Network

List networks:

```bash id="x11dpk"
docker network ls
```

Inspect a network:

```bash id="x8fguz"
docker network inspect app-network
```

This shows which containers are connected to the network.

## Test Network Between Containers

Create a network:

```bash id="zu94fa"
docker network create debug-network
```

Run Redis:

```bash id="ziyafe"
docker run -d --name redis --network debug-network redis:7-alpine
```

Run Alpine client:

```bash id="b317xp"
docker run -it --rm --network debug-network alpine sh
```

Inside Alpine:

```bash id="dg40zl"
ping redis
```

Install netcat if needed:

```bash id="rg9qvw"
apk add --no-cache netcat-openbsd
```

Test Redis port:

```bash id="u7hrcl"
nc -zv redis 6379
```

## Common Network Problem

Bad:

```text id="tle7th"
Container A is on network app-network
Container B is on default bridge
```

They may not communicate by name.

Better:

```bash id="yizfed"
docker network create app-network

docker run -d --name web --network app-network my-app:1.0.0
docker run -d --name redis --network app-network redis:7-alpine
```

Now `web` can reach Redis using hostname:

```text id="k2zs10"
redis
```

## 10. Check Volumes and Mounts

Inspect mounts:

```bash id="emx3fa"
docker inspect web --format='{{json .Mounts}}'
```

Or use full inspect:

```bash id="q8ul8m"
docker inspect web
```

List volumes:

```bash id="va81ul"
docker volume ls
```

Inspect volume:

```bash id="gd7twv"
docker volume inspect app-data
```

## Common Volume Problem

You mount an empty folder over app files.

Example:

```bash id="quoj3n"
docker run -v $(pwd)/empty:/app my-app:1.0.0
```

If the image had files in `/app`, they may be hidden by the bind mount.

Check inside:

```bash id="j9zyay"
docker exec -it my-app sh
ls -la /app
```

## 11. Check Resource Usage

Use `docker stats`:

```bash id="qkv1xf"
docker stats
```

This shows:

```text id="h0gb88"
CPU usage
Memory usage
Network usage
Block I/O
```

Check one container:

```bash id="jo9nr0"
docker stats web
```

If memory is too high, the container may be killed.

Exit code may show:

```text id="js3o7k"
137
```

## 12. Check Processes Inside Container

Use:

```bash id="tvvbkk"
docker top web
```

This shows processes running inside the container.

Example:

```text id="huqsca"
nginx: master process
nginx: worker process
```

If your application process is not there, the app may have crashed.

## 13. Check Files Changed in Container

Use:

```bash id="d1cmng"
docker diff web
```

This shows filesystem changes inside the container.

Symbols:

```text id="b9mwej"
A → Added
C → Changed
D → Deleted
```

Example:

```text id="seya3f"
C /var/log/nginx/access.log
A /tmp/test.txt
```

## 14. Docker Events

Docker events show real-time Docker activity.

```bash id="asyj7b"
docker events
```

You can see:

```text id="n7uahp"
container start
container stop
container die
health_status
network connect
volume mount
```

This is useful when containers restart or become unhealthy.

## Docker Compose Debugging

If you use Docker Compose, use Compose commands.

Show services:

```bash id="jrdoaa"
docker compose ps
```

View logs:

```bash id="p60cmq"
docker compose logs
```

Follow logs:

```bash id="d0xvwq"
docker compose logs -f
```

Logs for one service:

```bash id="rnx259"
docker compose logs web
```

Restart service:

```bash id="zxbbjt"
docker compose restart web
```

Rebuild and start:

```bash id="s708hb"
docker compose up --build
```

Stop everything:

```bash id="n50y6n"
docker compose down
```

## Debug Docker Compose Networking

In Docker Compose, services can reach each other by service name.

Example:

```yaml id="py5sdl"
services:
  web:
    build: .
    environment:
      REDIS_HOST: redis

  redis:
    image: redis:7-alpine
```

The `web` container should connect to Redis using:

```text id="osy7dz"
redis
```

Not:

```text id="vml55b"
localhost
```

Inside Docker, `localhost` means the same container.

## Common Docker Compose Problem

Bad:

```text id="pyw6ux"
REDIS_HOST=localhost
```

Better:

```text id="oeeudu"
REDIS_HOST=redis
```

Because `redis` is the Compose service name.

## Debug Image Build Problems

If the image fails to build, read the error carefully.

Build:

```bash id="fl6qlv"
docker build -t my-app:1.0.0 .
```

Build without cache:

```bash id="tmfzmd"
docker build --no-cache -t my-app:1.0.0 .
```

Common build problems:

```text id="v911oa"
Wrong file path
Missing requirements.txt
Wrong COPY command
Package install failure
No internet connection
Dockerfile syntax error
```

## Check Dockerfile COPY Problems

Example Dockerfile:

```dockerfile id="psmlq9"
COPY requirements.txt .
```

If `requirements.txt` does not exist in the build context, build fails.

Check files:

```bash id="kme7r1"
ls -la
```

Check `.dockerignore`:

```bash id="o8kjiz"
cat .dockerignore
```

Maybe the file was ignored by mistake.

## Rebuild After Changing Dockerfile

If you change Dockerfile or dependencies, rebuild the image.

```bash id="o81leu"
docker build -t my-app:1.0.0 .
```

For Compose:

```bash id="oxzi0b"
docker compose up --build
```

Sometimes use:

```bash id="uy74gu"
docker compose down
docker compose up --build
```

## Debug Healthchecks

Check health status:

```bash id="szey2l"
docker inspect --format='{{.State.Health.Status}}' CONTAINER_NAME
```

Show health details:

```bash id="w6udx6"
docker inspect --format='{{json .State.Health}}' CONTAINER_NAME
```

Common healthcheck problems:

```text id="aw7rdu"
Wrong port
Wrong path
curl or wget not installed
App needs more time to start
Health endpoint returns error
```

## Example Debugging Scenario 1

Problem:

```text id="sx0r1i"
Container exits immediately.
```

Debug:

```bash id="ohqux4"
docker ps -a
docker logs CONTAINER_NAME
docker inspect --format='{{.State.ExitCode}}' CONTAINER_NAME
```

Possible reason:

```text id="nlx7ts"
Wrong command
App crashed
Missing dependency
Missing environment variable
```

## Example Debugging Scenario 2

Problem:

```text id="a1vz9i"
Container is running but browser cannot open app.
```

Debug:

```bash id="j32qa4"
docker ps
docker port CONTAINER_NAME
docker logs CONTAINER_NAME
```

Check:

```text id="xelq3k"
Is port mapped?
Is the app listening on 0.0.0.0?
Is the correct host port used?
```

Bad Flask example:

```python id="iqlqt5"
app.run(host="127.0.0.1", port=5000)
```

Better:

```python id="o0joc1"
app.run(host="0.0.0.0", port=5000)
```

## Example Debugging Scenario 3

Problem:

```text id="uznqvc"
Web container cannot connect to Redis.
```

Debug:

```bash id="xphdbl"
docker network ls
docker network inspect NETWORK_NAME
docker logs web
docker exec -it web sh
```

Check from inside web:

```bash id="wpjta4"
printenv REDIS_HOST
ping redis
nc -zv redis 6379
```

Fix:

```text id="rdyy9f"
Put both containers on the same network
Use REDIS_HOST=redis
Do not use localhost for another container
```

## Example Debugging Scenario 4

Problem:

```text id="amb5ow"
Files are missing inside container.
```

Debug:

```bash id="sgoq73"
docker exec -it CONTAINER_NAME sh
ls -la /app
```

Check mounts:

```bash id="to3nb0"
docker inspect CONTAINER_NAME --format='{{json .Mounts}}'
```

Possible reason:

```text id="yf94ge"
Wrong bind mount path
.dockerignore ignored needed files
COPY command is wrong
Volume mounted over existing files
```

## Practical Debugging Lab

Create a broken container:

```bash id="g2ldng"
docker run --name broken-alpine alpine wrong-command
```

Check all containers:

```bash id="z5468t"
docker ps -a
```

Check logs:

```bash id="saq3vn"
docker logs broken-alpine
```

Inspect exit code:

```bash id="v6hzwx"
docker inspect --format='{{.State.ExitCode}}' broken-alpine
```

You may see exit code:

```text id="ds7b7p"
127
```

Meaning:

```text id="uc0arz"
Command not found
```

Remove it:

```bash id="zrsmog"
docker rm broken-alpine
```

Run correct command:

```bash id="xj3o0c"
docker run --rm alpine echo "Container works"
```

## Practical Web Debugging Lab

Run Nginx without port mapping:

```bash id="cjzfek"
docker run -d --name nginx-debug nginx:alpine
```

Check:

```bash id="cfekyy"
docker ps
```

You will not see `0.0.0.0:8080->80/tcp`.

Try browser:

```text id="njtzrc"
http://localhost:8080
```

It will not work because no port is mapped.

Fix:

```bash id="chz2f4"
docker rm -f nginx-debug
docker run -d --name nginx-debug -p 8080:80 nginx:alpine
```

Open:

```text id="aop5u4"
http://localhost:8080
```

## Common Beginner Mistakes

### Checking Only docker ps

Bad:

```bash id="qck3gh"
docker ps
```

If the container exited, it will not show.

Better:

```bash id="f43seh"
docker ps -a
```

### Ignoring Logs

Logs usually show the real problem.

```bash id="dtx822"
docker logs CONTAINER_NAME
```

### Using localhost Between Containers

Bad:

```text id="xhje0m"
web connects to localhost:6379
```

Better:

```text id="wg54bp"
web connects to redis:6379
```

### Forgetting Port Mapping

Bad:

```bash id="aqctko"
docker run nginx:alpine
```

Better:

```bash id="h5fz69"
docker run -p 8080:80 nginx:alpine
```

### Not Rebuilding Image

If you changed code but did not rebuild the image, the container may still use old code.

Fix:

```bash id="n3ulcz"
docker build -t my-app:1.0.0 .
docker rm -f my-app
docker run ...
```

For Compose:

```bash id="zk3s8s"
docker compose up --build
```

## Useful Debugging Commands

Show running containers:

```bash id="jkz5g9"
docker ps
```

Show all containers:

```bash id="u9cgha"
docker ps -a
```

Show logs:

```bash id="r50hx5"
docker logs CONTAINER_NAME
```

Follow logs:

```bash id="onex3r"
docker logs -f CONTAINER_NAME
```

Inspect container:

```bash id="bm5dvg"
docker inspect CONTAINER_NAME
```

Enter container:

```bash id="hejpmz"
docker exec -it CONTAINER_NAME sh
```

Check ports:

```bash id="xbvbjw"
docker port CONTAINER_NAME
```

Check resource usage:

```bash id="vi4v7m"
docker stats
```

Check processes:

```bash id="dwoxey"
docker top CONTAINER_NAME
```

Check networks:

```bash id="r6vf85"
docker network ls
docker network inspect NETWORK_NAME
```

Check volumes:

```bash id="xlx7ly"
docker volume ls
docker volume inspect VOLUME_NAME
```

View Docker events:

```bash id="whspgc"
docker events
```

## Docker Compose Useful Commands

Show services:

```bash id="x0t35w"
docker compose ps
```

Show logs:

```bash id="agq5f5"
docker compose logs
```

Follow logs:

```bash id="t9g44g"
docker compose logs -f
```

Restart service:

```bash id="nbmduh"
docker compose restart SERVICE_NAME
```

Rebuild:

```bash id="bwxuut"
docker compose up --build
```

Stop:

```bash id="pe4rts"
docker compose down
```

## Summary

```text id="rbg946"
docker ps       → Show running containers
docker ps -a    → Show all containers
docker logs     → View container logs
docker inspect  → View detailed container information
docker exec     → Run command inside running container
docker port     → Show port mappings
docker stats    → Show CPU and memory usage
docker top      → Show processes inside container
docker diff     → Show filesystem changes
docker events   → Show Docker events
```

```text id="fpdjtn"
Debugging rule:
Check status first, then logs, then inspect, then enter the container.
```

> Docker debugging is the process of using logs, status, inspect, exec, ports, networks, and volumes to find why a container is not working.

