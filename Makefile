body.step: body.py .docker-build
	cat body.py | docker run -i ecopoesis/cadquery:latest build --in_spec stdin --format STEP --out_spec stdout > body.step

.docker-build: Dockerfile
	docker build . -t ecopoesis/cadquery
	@touch $@