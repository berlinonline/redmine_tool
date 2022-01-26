.PRECIOUS: data/json/tree_%.json
data/json/tree_%.json: data/json
	@$(eval NODEID := $(patsubst tree_%.json,%,$(@F)))
	@echo "extracting tree starting with node id $(NODEID)..."
	@echo "writing to $@ ..."
	@python issue_tree.py -r $(NODEID) | jq "." > $@

data/svg/tree_%.svg: data/json/tree_%.json data/svg
	@echo "drawing svg tree from $< ..."
	@echo "writing to $@ ..."
	@python tree2dot.py -i $< -p 6,51 -m 40 > $@

.PHONY: data/temp/date.txt
data/temp/date.txt: | data/temp
	@echo "write current date ..."
	@date "+Last changed: %Y-%m-%d" > $@

clean: clean-temp

clean-temp:
	@echo "deleting temp folder ..."
	@rm -rf data/temp

data/temp:
	@echo "creating temp directory ..."
	@mkdir -p data/temp

data/json:
	@echo "creating temp directory ..."
	@mkdir -p data/json

data/svg:
	@echo "creating temp directory ..."
	@mkdir -p data/svg

