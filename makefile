install:
	curl -LsSf https://astral.sh/uv/install.sh | sh

run:
	uv run products_assistent

lint:
	uv run ruff format products_assistent && uv run ruff check products_assistent

commit_lint:
	uv run ruff format products_assistent --check && uv run ruff check products_assistent --exit-non-zero-on-fix