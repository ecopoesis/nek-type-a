body-to-step: body.py
	cat body.py | docker run -i dcowden/cadquery:latest build --in_spec stdin --format STEP --out_spec stdout > body.step
