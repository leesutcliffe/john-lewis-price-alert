.DEFAULT_GOAL := show-help
.PHONY: show-help
# See <https://gist.github.com/klmr/575726c7e05d8780505a> for explanation.
## This help screen
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)";echo;sed -ne"/^## /{h;s/.*//;:d" -e"H;n;s/^## //;td" -e"s/:.*//;G;s/\\n## /---/;s/\\n/ /g;p;}" ${MAKEFILE_LIST}|LC_ALL='C' sort -f|awk -F --- -v n=$$(tput cols) -v i=29 -v a="$$(tput setaf 6)" -v z="$$(tput sgr0)" '{printf"%s%*s%s ",a,-i,$$1,z;m=split($$2,w," ");l=n-i;for(j=1;j<=m;j++){l-=length(w[j])+1;if(l<= 0){l=n-i-length(w[j])-1;printf"\n%*s ",-i," ";}printf"%s ",w[j];}printf"\n";}'
UNAME := $(shell uname -m)


.PHONY: app
app:
	@cd price_alert_app && $(MAKE) all

.PHONY: tf-fmt
tf-fmt:
	@terraform -chdir=terraform fmt -recursive

.PHONY: tf-storage
tf-storage: tf-fmt
	@terraform -chdir=terraform/deployments/storage apply -auto-approve

.PHONY: tf-func
tf-func: tf-fmt
	@terraform -chdir=terraform/deployments/function_app apply -auto-approve

.PHONY: tf-storage-nuke
tf-storage-nuke:
	@terraform -chdir=terraform/deployments/storage destroy -auto-approve

.PHONY: tf-func-nuke
tf-func-nuke:
	@terraform -chdir=terraform/deployments/function_app destroy -auto-approve

.PHONY: deploy
deploy:
	@cd price_alert_app; func azure functionapp publish func-price-alert-app --python;

.PHONY: all
## Run all required pre-push commands
all: app tf-storage tf-func deploy
	@echo -e "\n\n >> All Good!!! << :)"

.PHONY: nuke
## destroy all the things
nuke: tf-func-nuke tf-storage
	@echo -e "\n\n >> BOOM!!! <<"


