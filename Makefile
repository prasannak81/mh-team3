IMG_NAME=quickpickup/chatops
IMG_VERSION=0.3.2
.DEFAULT_GOAL := test


.PHONY: build
build:
	docker build -t $(IMG_NAME):$(IMG_VERSION) . 

.PHONY: cli
cli:
	docker run -it \
		-v $(shell pwd):/local \
		-w /local \
		$(IMG_NAME):$(IMG_VERSION) bash

.PHONY: prod
prod:
	docker run -itd --env-file chat.env -p 5030:5030 $(IMG_NAME):$(IMG_VERSION)

.PHONY: test
test:	lint unit

.PHONY: lint
lint:
	@echo "Starting  lint"
# # Verify all Python files meet Black code style
	docker run -t -v $(shell pwd):/local $(IMG_NAME):$(IMG_VERSION) black --check ./
	@echo "Completed lint"

.PHONY: unit
unit:
	@echo "Starting Unit Tests"
	docker run -t -v $(shell pwd):/local $(IMG_NAME):$(IMG_VERSION) pytest -vvvv
	@echo "Completed Unit Tests"
