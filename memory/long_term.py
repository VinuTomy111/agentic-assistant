import json
import os
from typing import List, Dict, Any

class LongTermMemory:
    """
    Manages long-term persistence of facts, preferences, and data using a simple JSON file.
    Implements a basic keyword search to retrieve relevant memories.
    """
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.memories: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    self.memories = json.load(f)
            except json.JSONDecodeError:
                self.memories = []
        else:
            self.memories = []
            self._save()

    def _save(self):
        """Save memories to the JSON file."""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.memories, f, indent=4)

    def save_memory(self, memory_text: str, keywords: List[str]):
        """
        Save a specific piece of information to long-term memory.
        """
        new_memory = {
            "content": memory_text,
            "keywords": [kw.lower() for kw in keywords]
        }
        self.memories.append(new_memory)
        self._save()

    def retrieve_relevant(self, query: str, top_k: int = 3) -> List[str]:
        """
        Retrieve memories based on simple keyword matching with the query.
        Returns the top_k most relevant memory contents.
        """
        if not self.memories:
            return []

        query_words = set(query.lower().split())
        
        # Calculate scores for each memory based on keyword overlap
        scored_memories = []
        for mem in self.memories:
            mem_keywords = set(mem.get("keywords", []))
            # Fall back to word overlap with content if no keywords match
            content_words = set(mem.get("content", "").lower().split())
            
            score = len(query_words.intersection(mem_keywords)) * 2 # Weight defined keywords higher
            score += len(query_words.intersection(content_words))
            
            if score > 0:
                scored_memories.append((score, mem.get("content", "")))
                
        # Sort by score descending
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        
        # Return top K contents
        return [mem[1] for mem in scored_memories[:top_k]]

    def get_all(self) -> List[Dict[str, Any]]:
        return self.memories
