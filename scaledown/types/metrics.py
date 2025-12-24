from dataclasses import dataclass

@dataclass
class OptimizerMetrics:
    original_tokens: int
    optimized_tokens: int
    chunks_retrieved: int
    compression_ratio: float
    latency_ms: float
    retrieval_mode: str
    ast_fidelity: float

@dataclass
class CompressorMetrics:
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float
    latency_ms: float
    model_used: str
    cost_saved: float
