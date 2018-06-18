all: body.step body.stl

body.step: body.py .docker-build
	cat body.py | docker run --name cadquery_stl --rm -v $(shell pwd):/opt/cadquery/build_data -i ecopoesis/cadquery:latest build --in_spec stdin --format STEP --out_spec stdout > body.step

body.stl: body.py .docker-build
	cat body.py | docker run --name cadquery_step --rm -v $(shell pwd):/opt/cadquery/build_data -i ecopoesis/cadquery:latest build --in_spec stdin --format STL --out_spec stdout > body.stl

.docker-build: Dockerfile
	docker build . -t ecopoesis/cadquery
	@touch $@