FROM ghcr.io/stephanlensky/swayvnc-chrome:latest

ENV PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Make directory for the app
RUN mkdir /app
RUN chown $DOCKER_USER:$DOCKER_USER /app

# Switch to the non-root user
USER $DOCKER_USER

# Add a hotkey to swaywm config for starting next test (for truedriver_PAUSE_AFTER_TEST=true)
RUN echo 'bindsym Mod4+Return exec /app/tests/next_test.sh' >> ~/.config/sway/config

# Set the working directory
WORKDIR /app

# Install python
RUN uv python install 3.13

# Install the Python project's dependencies using the lockfile and settings
COPY --chown=$DOCKER_USER:$DOCKER_USER pyproject.toml uv.lock /app/
RUN --mount=type=cache,target=/home/$DOCKER_USER/.cache/uv,uid=$PUID,gid=$PGID \
    uv sync --frozen --no-install-project

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY --chown=$DOCKER_USER:$DOCKER_USER . /app

# Add binaries from the project's virtual environment to the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Sync the project's dependencies and install the project
RUN --mount=type=cache,target=/home/$DOCKER_USER/.cache/uv,uid=$PUID,gid=$PGID \
    uv sync --frozen

USER root
# Pass custom command to entrypoint script provided by the base image
ENTRYPOINT ["/entrypoint.sh", "./scripts/test.sh"]
