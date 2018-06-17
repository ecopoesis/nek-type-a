body.step: body.py .docker-build
	docker stop cadquery || true && docker rm cadquery || true
	cat body.py | docker run --name cadquery -i ecopoesis/cadquery:latest build --in_spec stdin --format STEP --out_spec stdout > body.step

.docker-build: Dockerfile
	docker build . -t ecopoesis/cadquery
	@touch $@