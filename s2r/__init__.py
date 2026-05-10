"""s2r - Convert SLURM scripts to Run.ai configurations using AI."""

from s2r.converter import convert_slurm_to_runai, ConversionError

__version__ = "0.3.2"
__all__ = ["convert_slurm_to_runai", "ConversionError"]
