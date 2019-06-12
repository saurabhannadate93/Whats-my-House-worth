WHERE=Local #"Local" or "AWS"
STORAGE_S3_BUCKET=nw-saurabhannadate-s3
BUCKET=Scripts

.PHONY: load_data clean_data generate_features train_model run_app venv

msia423projectEnv/${BUCKET}/activate: requirements.txt
	test -d msia423projectEnv || virtualenv msia423projectEnv
	. msia423projectEnv/${BUCKET}/activate; pip install -r requirements.txt
	touch msia423projectEnv/${BUCKET}/activate

venv: msia423projectEnv/${BUCKET}/activate
	
load_data: venv
	. msia423projectEnv/${BUCKET}/activate; python run.py load_data --where=${WHERE} --bucket=${STORAGE_S3_BUCKET}

clean_data: load_data venv
	. msia423projectEnv/${BUCKET}/activate; python run.py clean_data --where=${WHERE} --bucket=${STORAGE_S3_BUCKET}

generate_features: clean_data venv
	. msia423projectEnv/${BUCKET}/activate; python run.py generate_features --where=${WHERE} --bucket=${STORAGE_S3_BUCKET}

train_model: generate_features venv
	. msia423projectEnv/${BUCKET}/activate; python run.py train_model --where=${WHERE} --bucket=${STORAGE_S3_BUCKET}

app: train_model venv
	. msia423projectEnv/${BUCKET}/activate; python run.py run_app
