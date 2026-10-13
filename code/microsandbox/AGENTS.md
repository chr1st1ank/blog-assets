# Sandbox PoC

Only workspace/ is mounted at /workspace (agent-writable) and opencode/ at /root/.config/opencode (read-only). Keep sandbox policy, real credentials, toolchain inputs, and VM state outside the workspace. Never expose the host container socket.

Use the installed msb and task. The toolchain copies the existing host task and gh binaries via the host-tools build context; it does not download them. OpenCode config (opencode.json, tui.json) lives in ./opencode and is bind-mounted read-only — changes take effect on VM restart, not image rebuild. OpenCode v2 is pinned to @opencode/cli 2.0.23, published 2026-10-05.

Run outer tasks from this directory: doctor, image:build, image:load, vm:create, vm:shell, agent, test, boundary:check, app:up, app:down, vm:stop, vm:start. vm:create always loads secrets.yaml; Microsandbox validates the required host variables without a duplicate Task precondition. Actual values belong in the user's host environment or ignored secrets.env, never in secrets.yaml or either image.

The inner Taskfile provides test, serve, compose:up, and compose:down. Local app verification is `task --dir workspace test`; container tasks belong inside the VM. Keep the uv lockfile and seven-day dependency cooldown.

Podman is an example workload, not a second security boundary. The VM limits CPU/RAM and has an 8 GiB private container-storage disk. Its guest kernel lacks an iptables extension needed for bridge networking: builds use the guest network namespace and the app uses slirp4netns. HTTPS builds receive only the guest's public CA bundle as a build secret. There are no Podman health checks.

secrets.yaml defines destination-bound HTTP credential injection. Manual GitHub/credential checks and experiment results belong in the phase-2 research notes. Do not read or log real secrets or run billable model calls without approval.

Egress uses network.policy: public — public internet allowed, private/loopback/link-local/metadata blocked. Do not reintroduce a strict allow list: OpenCode fans out to several hosts (models.opencode.ai, console subdomains), and apex entries do not cover subdomains.

Microsandbox is installed with `uv tool install microsandbox`. Its bundled runtime and firmware are discovered automatically; no MSB_PATH or MSB_LIBKRUNFW_PATH override is needed. The earlier AUR runtime with the separate libkrunfw package failed guest power-off. VM state lives in ignored .msb/ and exported images in .artifacts/.

vm:create uses --replace: it discards the existing VM's guest state while leaving the mounted workspace intact. Agents must not execute replacement or deletion without explicit confirmation. The user reports graceful shutdown works after reinstalling through uv. vm:stop uses a bounded graceful timeout, not a forced stop. Only the empty diagnostic VM msb-stop-probe-20261013 was force-stopped, with explicit approval; its saved state was not deleted.

The validation VM msb-poc-v2 uses workspace/, synthetic credential bindings, and no host port forwarding. Its single test, boundary checks, placeholder checks, and Podman app build/run passed. The normal sandbox.yaml still forwards port 8000. Actual provider/GitHub authentication requires user-provided credentials and a fresh authenticated VM; the validation VM is not configured with real credentials.
