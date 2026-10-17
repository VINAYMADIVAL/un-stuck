PY ?= python3

.PHONY: check install install-dry health dashboard audit evals test new-agent

check:            ## static validation + offline knowledge-coverage evals
	$(PY) scripts/validate.py
	$(PY) scripts/run_evals.py --offline

install:          ## sync SOUL base + skills into Hermes profiles (never overwrites memory)
	$(PY) scripts/install.py

install-dry:      ## show what install would do
	$(PY) scripts/install.py --dry-run

health:           ## fleet health report
	$(PY) scripts/fleet_health.py

dashboard:        ## static HTML dashboard at status/dashboard.html
	$(PY) scripts/fleet_health.py --html status/dashboard.html

audit:            ## memory isolation + sensitive-data audit
	$(PY) scripts/memory_audit.py

evals:            ## live evals: make evals CMD='hermes -p {profile} chat -q {question}'
	$(PY) scripts/run_evals.py --cmd "$(CMD)"

test:
	$(PY) -m unittest discover -s tests -v

new-agent:        ## make new-agent P=slack
	$(PY) scripts/new_agent.py $(P)
