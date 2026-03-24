# cmk-agent-receiver

A [FastAPI](https://fastapi.tiangolo.com/) service that acts as the HTTP
endpoint through which Checkmk agents and relays communicate with a Checkmk
site.
It is started automatically by `omd start` and served via
[Gunicorn](https://gunicorn.org/) with a custom
[Uvicorn](https://www.uvicorn.org/) worker.

## Architecture

The package exposes a single main app (`cmk.agent_receiver.main:main_app`)
that mounts two independent FastAPI sub-applications:

| Sub-app            | Mount path               | Purpose                                                                                                       |
| ------------------ | ------------------------ | ------------------------------------------------------------------------------------------------------------- |
| **agent-receiver** | `/<site>/agent-receiver` | Agent registration & pairing, certificate signing / renewal, monitoring-data upload                           |
| **relay**          | `/<site>/relays`         | Relay registration, mTLS certificate exchange, task management, config activation, monitoring-data forwarding |

Shared functionality (configuration, authentication, certificates, logging,
B3 trace-ID middleware) lives in `cmk/agent_receiver/lib/`.

The relay sub-app is only active on editions that support relays.

## Configuration

The service reads `agent_receiver_config.json` from `$OMD_ROOT` at startup.
If the file is absent, built-in defaults apply.

| Key                           | Type    | Default | Description                            |
| ----------------------------- | ------- | ------- | -------------------------------------- |
| `task_ttl`                    | `float` | `120.0` | Time-to-live for relay tasks (seconds) |
| `max_pending_tasks_per_relay` | `int`   | `10`    | Maximum pending tasks per relay        |

## Development

### Deploying local changes

From the package directory, run `f12`.
This builds the wheel via Bazel, pip-installs it into the site, and restarts the `agent-receiver` daemon.

### Running locally for debugging

```bash
omd stop agent-receiver
uvicorn cmk.agent_receiver.main:main_app
```

### Bazel targets

```bash
# run all tests
bazel test //packages/cmk-agent-receiver/...

# unit tests only
bazel test //packages/cmk-agent-receiver/tests/unit:unit

# component tests only
bazel test //packages/cmk-agent-receiver/tests/component:component

# type checking
bazel build --config=mypy //packages/cmk-agent-receiver/...

# formatting
bazel run //:format packages/cmk-agent-receiver

# linting
bazel lint //packages/cmk-agent-receiver/...

# build wheel
bazel build //packages/cmk-agent-receiver:wheel
```

<!-- CONTEXT
The main FastAPI app (main.py) mounts two distinct sub-apps:
  - agent-receiver (/<site>/agent-receiver) — handles agent registration, pairing, certificate renewal, and monitoring-data ingestion from Checkmk agents.
  - relay (/<site>/relays) — manages relay registration, task distribution, configuration activation, and forwarding of monitoring data from relays.
Both sub-apps share common library code under lib/.
The relay lifespan (startup logic) is defined on the main app because FastAPI does not propagate lifespan events to mounted sub-apps.
-->
