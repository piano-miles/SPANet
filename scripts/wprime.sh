python -m spanet.train -of options_files/wprime/wprime.json --gpus 1 &&
    python -m spanet.test ./spanet_output/version_0 -tf data/wprime/wprime_1000.h5 --gpu &&
    python -m spanet.predict ./spanet_output/version_0 ./wprime_testing_output.h5 -tf data/wprime/wprime_1000.h5 --gpu
