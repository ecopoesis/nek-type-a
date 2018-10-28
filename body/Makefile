all: directories target/body.step target/body.stl target/plate.step target/plate.stl

CQ_SOURCES = body.py .docker-build build_data/*.svg build_data/*.py

target/body.step: $(CQ_SOURCES)
	cat body.py | docker run --name cadquery_stl --rm -v $(shell pwd)/build_data:/opt/cadquery/build_data -i ecopoesis/cadquery:latest build --in_spec stdin --format STEP --out_spec stdout > target/body.step

target/body.stl: $(CQ_SOURCES)
	cat body.py | docker run --name cadquery_step --rm -v $(shell pwd)/build_data:/opt/cadquery/build_data -i ecopoesis/cadquery:latest build --in_spec stdin --format STL --out_spec stdout > target/body.stl

target/plate.step: $(CQ_SOURCES)
	cat body.py | docker run --name cadquery_svg --rm -v $(shell pwd)/build_data:/opt/cadquery/build_data -i ecopoesis/cadquery:latest build --in_spec stdin --format STEP --out_spec stdout --params '{"shape": "plate"}' > target/plate.step

target/plate.stl: $(CQ_SOURCES)
	cat body.py | docker run --name cadquery_svg --rm -v $(shell pwd)/build_data:/opt/cadquery/build_data -i ecopoesis/cadquery:latest build --in_spec stdin --format STL --out_spec stdout --params '{"shape": "plate"}' > target/plate.stl

.docker-build: Dockerfile environment.yml conda_cq.sh cq_cmd.py
	docker build . -t ecopoesis/cadquery
	@touch $@

directories: target

target:
	mkdir -p target

clean:
	rm -f target/*
	rm -f .docker-build
