all: body.step body.stl

CQ_SOURCES = body.py .docker-build right_top.svg left_top.svg

body.step: $(CQ_SOURCES)
	cat body.py | docker run --name cadquery_stl --rm -v $(shell pwd):/opt/cadquery/build_data -i ecopoesis/cadquery:latest build --in_spec stdin --format STEP --out_spec stdout > body.step

body.stl: $(CQ_SOURCES)
	cat body.py | docker run --name cadquery_step --rm -v $(shell pwd):/opt/cadquery/build_data -i ecopoesis/cadquery:latest build --in_spec stdin --format STL --out_spec stdout > body.stl

.docker-build: Dockerfile environment.yml conda_cq.sh
	docker build . -t ecopoesis/cadquery
	@touch $@

clean:
	rm -f body.stl
	rm -f body.step
	rm -f .docker-build
