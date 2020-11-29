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

.PHONY: pack
pack:
	# clean
	rm -rf $(TMP_DIR)
	rm $(LOGIN).zip || true
	# prepare
	mkdir -p $(TMP_AI) $(TMP_ML) $(TMP_SERVER)
	# doc
	cp doc/$(PDF_NAME)  $(TMP_DIR)
	# ai
	cp -r dicewars/ai/$(LOGIN) $(TMP_DIR)
	# supplementary
	cp -r ml-scripts $(SUPL_DIR)
	cp $(SERVER_DIR)/game.py $(TMP_SERVER)
	cp $(AI_DIR)/xkolar71_orig.py $(AI_DIR)/xkolar71_2.py $(AI_DIR)/xkolar71_3.py $(AI_DIR)/xkolar71_4.py $(TMP_AI)
	cp requirements.txt $(SUPL_DIR)
	cp $(ML_DIR)/__init__.py  $(ML_DIR)/game.py $(TMP_ML)
	# pack
	cd $(TMP_DIR) && zip -r $(LOGIN) $(PDF_NAME) $(LOGIN) $(SUPL_NAME) -x '*.gitignore'
	mv $(TMP_DIR)/$(LOGIN).zip .
