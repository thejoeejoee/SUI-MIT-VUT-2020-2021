LOGIN = xkolar71

TMP_DIR = pack
SUPL_NAME = supplementary
SUPL_DIR = $(TMP_DIR)/$(SUPL_NAME)
AI_DIR = dicewars/ai
ML_DIR = dicewars/ml
SERVER_DIR = dicewars/server
TMP_AI = $(SUPL_DIR)/$(AI_DIR)
TMP_ML = $(SUPL_DIR)/$(ML_DIR)
TMP_SERVER = $(SUPL_DIR)/$(SERVER_DIR)
PDF_NAME = $(LOGIN).pdf

.PHONY: pack_supplement pack_simple pack_clean pack_test

all: pack_supplement

pack_simple: pack_clean
	zip -r $(LOGIN) $(AI_DIR)/$(LOGIN) doc/$(PDF_NAME) $(AI_DIR)/xkolar71_orig.py $(AI_DIR)/xkolar71_2.py $(AI_DIR)/xkolar71_3.py $(AI_DIR)/xkolar71_4.py $(ML_DIR)/__init__.py  $(ML_DIR)/game.py $(SERVER_DIR)/game.py requirements.txt ml-scripts -x '*.gitignore'

pack_supplement: pack_clean
	# prepare
	mkdir -p $(TMP_AI) $(TMP_ML) $(TMP_SERVER)
	# doc
	cp doc/$(PDF_NAME)  $(TMP_DIR)
	# ai
	cp -r $(AI_DIR)/$(LOGIN) $(TMP_DIR)
	# supplementary
	cp -r ml-scripts $(SUPL_DIR)
	cp $(SERVER_DIR)/game.py $(TMP_SERVER)
	cp $(AI_DIR)/xkolar71_orig.py $(AI_DIR)/xkolar71_2.py $(AI_DIR)/xkolar71_3.py $(AI_DIR)/xkolar71_4.py $(TMP_AI)
	cp requirements.txt $(TMP_DIR)
	cp $(ML_DIR)/__init__.py  $(ML_DIR)/game.py $(TMP_ML)
	# pack
	cd $(TMP_DIR) && zip -r $(LOGIN) $(PDF_NAME) $(LOGIN) $(SUPL_NAME) requirements.txt -x '*.gitignore'
	mv $(TMP_DIR)/$(LOGIN).zip .

pack_clean:
	rm -rf $(TMP_DIR)
	rm $(LOGIN).zip || true

pack_test: pack_supplement
	./is-it-ok.sh $(LOGIN).zip pack_test
