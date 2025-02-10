install:
	curl -LsSf https://astral.sh/uv/install.sh | sh

run:
	uv run products_assistent

dev:
	uv run flask --app products_assistent run --debug

lint:
	uv run ruff format products_assistent && uv run ruff check products_assistent

commit_lint:
	uv run ruff format products_assistent --check && uv run ruff check products_assistent --exit-non-zero-on-fix