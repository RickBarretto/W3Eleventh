# Update pip
python -m pip install --upgrade pip

# Install pipx to manage python apps
pip install pipx

# Install Python Apps
pipx install poetry                 # For dependency management 
pipx install vyper                  # Avoids VsCode issues with the extension

# Project Bootstrap
poetry install --no-root            # Install dependencies
poetry self add poetry-plugin-shell # Install shell plugin to avoid calling `poetry run`
poetry env activate                 # Activate the environment