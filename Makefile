.PHONY: up test figures clean reproduce

up:
	docker compose up --build lab

test:
	docker compose run --rm test

figures:
	python -m src.run_all_benchmarks --output reports/benchmark.json --figures reports/

reproduce:
	python -m src.run_all_benchmarks --output reports/benchmark.json --figures reports/
	pytest tests/ -v

clean:
	rm -rf reports/*.png reports/*.json reports/*.pdf
