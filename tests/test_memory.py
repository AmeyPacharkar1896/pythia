import pytest
from unittest.mock import MagicMock, patch
from src.services.memory import MemoryEngine

@patch('src.services.memory.chromadb.PersistentClient') 
def test_memory_initialization(mock_client):
    memory = MemoryEngine()
    
    # Did we try to create a collection?
    mock_client.return_value.get_or_create_collection.assert_called_with(
        name="oracle_knowledge",
        metadata={"hnsw:space": "cosine"}
    )

@patch('src.services.memory.chromadb.PersistentClient')
def test_memorize_calls_upsert(mock_client):
    # Setup the Mock Collection
    mock_collection = MagicMock()
    mock_client.return_value.get_or_create_collection.return_value = mock_collection
    
    memory = MemoryEngine()
    
    # Action
    memory.memorize("test.txt", "This is some content")
    
    # Assert
    mock_collection.upsert.assert_called_once()
    
    call_args = mock_collection.upsert.call_args
    # Convert args to string to easily check contents
    args_str = str(call_args)
    assert "test.txt" in args_str
    assert "This is some content" in args_str

@patch('src.services.memory.chromadb.PersistentClient')
def test_forget_calls_delete(mock_client):
    mock_collection = MagicMock()
    mock_client.return_value.get_or_create_collection.return_value = mock_collection
    
    memory = MemoryEngine()
    memory.forget("secret.txt")
    
    mock_collection.delete.assert_called_once()
    assert "secret.txt" in str(mock_collection.delete.call_args)