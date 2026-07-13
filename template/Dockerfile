# Standalone microservice image for __PKG_DIST__.
# Build context = the package directory. The image contains ONLY this package
# and its declared dependencies — if the build needs anything else, the
# package is violating INDEPENDENCE.md.
FROM python:3.13-slim

RUN pip install --no-cache-dir uv

WORKDIR /app
COPY pyproject.toml README.md ./
COPY __PKG_MODULE__ ./__PKG_MODULE__

RUN uv pip install --system ".[standalone]"

EXPOSE 8080
CMD ["uvicorn", "__PKG_MODULE__.standalone.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8080"]
