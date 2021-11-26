.PHONY: build clean image

COUNT := $(shell git rev-list --all --count)
TAG := $(shell git describe --tags --abbrev=0)
SHA1 := $(shell git log -1 --format=%h)
BRANCH := $(shell git branch --show-current | tr / _)
DATE := $(shell date)
DIFF := $(shell git rev-list --left-right --count  origin...main)

build:
	make clean
	@echo """Version: $(TAG)""" >> version.txt
	@echo """--------------------------------""" >> version.txt
	@echo """Build date: $(DATE)""" >> version.txt
	@echo """SHA1: $(SHA1)""" >> version.txt
	@echo """Branch: $(BRANCH)""" >> version.txt
	@echo """Code diff: Behind-Ahead --> $(DIFF)""" >> version.txt
	@echo """--------------------------------""" >> version.txt
	@echo "=== building files ==="
	python setup.py bdist_egg --exclude-source-files -k -b build/dist

	cp -v requirements.txt build/dist/app
	cp -v ./app/logging.conf build/dist/app
	cp -v ./app/*.env build/dist/app
	mv version.txt build/dist/app
	
	
clean:
	@echo "=== removing old build dir ===="
	# rm version.txt
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info

image:
	make build
	docker build -t listener-service-chat-pre-build -f Dockerfile.build .
	docker build -t vengagedockerhub/listener-service-chat:$(BRANCH)-$(TAG).$(COUNT) --build-arg GIT_COMMIT=$(SHA1) --build-arg BRANCH=$(BRANCH) .
	docker push vengagedockerhub/listener-service-chat:$(BRANCH)-$(TAG).$(COUNT)
