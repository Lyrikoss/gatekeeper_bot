import os
from llama_cpp import Llama


_llama_instance = None

class LlamaLoader:
    def __init__(
        self,
        model_path: str = None,
        n_ctx: int = 2048,
        n_threads: int = 4,
        temperature: float = 0.7,
        top_p: float = 0.95,
        n_gpu_layers: int = 0,  # set >0 if using GPU
    ):
        """
        Initialize LlamaLoader with model path and generation parameters.
        """
        if model_path is None:
            # Automatically resolve full path relative to this file
            base_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(base_dir, "llama-2-7b-chat.Q4_K_M.gguf")

        self.model_path = model_path
        self.n_ctx = n_ctx
        self.n_threads = n_threads
        self.temperature = temperature
        self.top_p = top_p
        self.n_gpu_layers = n_gpu_layers

        self.model = self.load_model()

    def load_model(self) -> Llama:
        """
        Load the LLaMA model from disk using llama_cpp.
        """
        print(f"Loading LLaMA model from {self.model_path}...")
        model = Llama(
            model_path=self.model_path,
            n_ctx=self.n_ctx,
            n_threads=self.n_threads,
            n_gpu_layers=self.n_gpu_layers,
            chat_format="llama-2",  # Make sure your model supports this
        )
        print("Model loaded successfully.")
        return model

# Singleton instance for global use
_llama_instance: LlamaLoader | None = None

def get_llama_instance(
    model_path: str = None
) -> LlamaLoader:
    global _llama_instance
    if _llama_instance is None:
        _llama_instance = LlamaLoader(model_path=model_path)
    return _llama_instance

def get_llama_safely():
    global _llama_instance
    if _llama_instance is None:
        _llama_instance = get_llama_instance()
    return _llama_instance
