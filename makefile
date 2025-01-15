run:
	uv run products_assistent

lint:
	uv run ruff format && uv run ruff check

commit_lint:
	uv run ruff check