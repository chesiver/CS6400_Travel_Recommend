
.PHONY=help
help::
	@echo "Install virtualenv and dependencies first (see README)"
	@echo ""
	@echo "Then run:"
	@echo "make index #(re)create Elasticsearch index"
	@echo "make backend #Run backend service on http://localhost:5000"
	@echo "make frontend #Run frontend service on http://localhost:8000"
	@echo
	@echo "After performing the above, point your browser to http://localhost:8000"

.PHONY=frontend
frontend::
	(cd frontend && python -m http.server 8000)

.PHONY=backend
backend::
	python runFlask.py

.PHONY=index
index::
	curl -XDELETE http://localhost:9200/travelsearch; echo;
	curl -XPUT http://localhost:9200/travelsearch/?pretty -H 'Content-Type: application/json' -d @mapping.json; echo
	curl -XPUT http://localhost:9200/_bulk -H 'Content-Type: application/json' --data-binary @travel.data; echo

