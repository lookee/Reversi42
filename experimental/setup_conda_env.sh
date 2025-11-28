#!/bin/bash

# Script per creare/configurare ambiente conda per RL Player
# Usage: ./setup_conda_env.sh [python_version]

set -e

ENV_NAME="reversi42_rl"
PYTHON_VERSION=${1:-"3.11"}  # Default Python 3.11

echo "=========================================="
echo "Conda Environment Setup for RL Player"
echo "=========================================="
echo ""
echo "Environment name: $ENV_NAME"
echo "Python version: $PYTHON_VERSION"
echo ""

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Conda non trovato!"
    echo ""
    echo "Installa conda da: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Check if environment already exists
if conda env list | grep -q "^${ENV_NAME} "; then
    echo "⚠️  Ambiente '$ENV_NAME' già esistente"
    read -p "Vuoi ricrearlo? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Rimozione ambiente esistente..."
        conda env remove -n $ENV_NAME -y
    else
        echo "Attivazione ambiente esistente..."
        echo ""
        echo "Per attivare l'ambiente, esegui:"
        echo "  conda activate $ENV_NAME"
        exit 0
    fi
fi

# Create new environment
echo "Creazione nuovo ambiente conda..."
conda create -n $ENV_NAME python=$PYTHON_VERSION -y

echo ""
echo "Attivazione ambiente..."
echo ""

# Activate environment (note: this might not work in script, so we'll print instructions)
echo "=========================================="
echo "Ambiente creato con successo!"
echo "=========================================="
echo ""
echo "Per attivare l'ambiente, esegui:"
echo "  conda activate $ENV_NAME"
echo ""
echo "Poi installa le dipendenze:"
echo "  pip install -r experimental/requirements-rl.txt"
echo ""
echo "Per disattivare l'ambiente:"
echo "  conda deactivate"
echo ""
echo "Per vedere tutti gli ambienti:"
echo "  conda env list"
echo ""

