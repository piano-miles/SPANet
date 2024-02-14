#!/bin/bash

# This script is an example of how to use the SPANet package to train, evaluate, and predict on the example ttbar dataset.

# Deactivate any existing environment
echo "Deactivating environment..."
conda deactivate

# Delete ./environment if it exists
if [ -d ./environment ]; then
    echo "Deleting environment..."
    rm -rf ./environment
fi

# Create a new environment
echo "Creating environment..."
conda env create -p ./environment --file environment.yaml
conda activate ./environment && (
    echo "Environment created and activated."
    echo ""

    # Print Python version
    echo "Python version:"
    python --version

    # Print installed packages and versions
    conda list
    echo ""
    echo "Beginning training..."
    echo ""

    python -m spanet.train -of options_files/full_hadronic_ttbar/example.json --time_limit 00:00:01:00 --gpus 1 && ( # Train
        echo ""
        echo "Training complete. Beginning evaluation and prediction..."
        echo ""

        python -m spanet.test ./spanet_output/version_0 -tf data/full_hadronic_ttbar/example.h5 --gpu && # Evaluate
            (
                python -m spanet.predict ./spanet_output/version_0 ./spanet_ttbar_example_output.h5 -tf data/full_hadronic_ttbar/example.h5 --gpu && ( # Predict
                    echo ""
                    echo "Evaluation and prediction complete."
                )
            )
    )
)
