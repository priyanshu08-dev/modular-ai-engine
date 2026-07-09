from app.engine.memory.implementations import InMemoryStore
from app.engine.memory.manager import MemoryManager

memory_manager = MemoryManager(
    InMemoryStore(),
)