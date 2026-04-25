"""FastAPI entrypoint for CORP-ENV (OpenEnv HTTP server)."""

from __future__ import annotations

import os

import uvicorn
from openenv.core.env_server.http_server import create_app

from corp_env.models import CorpAction, CorpObservation
from server.environment import CorpEnvironment

app = create_app(
    CorpEnvironment,
    CorpAction,
    CorpObservation,
    env_name="corp-env",
    max_concurrent_envs=4,
)


def main() -> None:
    port = int(os.environ.get("PORT", "7860"))
    uvicorn.run("server.app:app", host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
