# Define the virtual environment folder and Python executable
VENV_NAME = .venv
PYTHON = $(VENV_NAME)/bin/python
UVICORN = $(VENV_NAME)/bin/uvicorn
CELERY = $(VENV_NAME)/bin/celery
ALEMBIC = $(VENV_NAME)/bin/alembic

# Define the tasks
TASK_APP = app.tasks.tasks

# Default target
.PHONY: all
all: install run

# Create the virtual environment
.PHONY: venv
venv:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV_NAME)

# Install dependencies into the virtual environment
.PHONY: install
install: venv
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

# Run both Uvicorn and Celery workers in the background
.PHONY: run
run: run-migrations start-uvicorn start-celery-worker start-celery-beat

# Run Alembic migrations
.PHONY: run-migrations
run-migrations:
	@echo "Running Alembic migrations..."
	$(ALEMBIC) upgrade head

# Start Uvicorn with --reload
.PHONY: start-uvicorn
start-uvicorn:
	@echo "Starting Uvicorn..."
	$(UVICORN) app.main:app --reload &

# Start Celery Worker with solo pool
.PHONY: start-celery-worker
start-celery-worker:
	@echo "Starting Celery Worker..."
	$(CELERY) -A $(TASK_APP) worker -l info --pool=solo &

# Start Celery Beat with solo pool
.PHONY: start-celery-beat
start-celery-beat:
	@echo "Starting Celery Beat..."
	$(CELERY) -A $(TASK_APP) beat -l info

# Clean up the virtual environment and remove old installations
.PHONY: clean
clean:
	@echo "Cleaning virtual environment..."
	rm -rf $(VENV_NAME)
