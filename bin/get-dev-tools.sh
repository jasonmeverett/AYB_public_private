#!/bin/bash

# Get Atuin for magical shell history.
# https://atuin.sh/
curl --proto '=https' --tlsv1.2 -LsSf https://setup.atuin.sh | sh
source ~/.bashrc

# Get oh-my-bash to unleash your terminal.
# https://ohmybash.nntoan.com/
bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)"
source ~/.bashrc