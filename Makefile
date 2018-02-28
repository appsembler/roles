.PHONY = docs-serve docs-build syntax-check

syntax-check:
	@ansible-playbook -i tests/inventory --syntax-check tests/test.yml

# =========== MkDocs ================= #
docs-serve:
	@mkdocs serve

docs-build:
	@mkdocs build
