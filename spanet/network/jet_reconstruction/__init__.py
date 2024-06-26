from spanet.network.jet_reconstruction.jet_reconstruction_training import (
    JetReconstructionTraining,
)
from spanet.network.jet_reconstruction.jet_reconstruction_validation import (
    JetReconstructionValidation,
)
from spanet.network.jet_reconstruction.jet_reconstruction_optimization import (
    JetReconstructionOptimization,
)


# class JetReconstructionModel(JetReconstructionOptimization, JetReconstructionValidation, JetReconstructionTraining):
class JetReconstructionModel(JetReconstructionValidation, JetReconstructionTraining):
    pass
