import pytest
from unittest.mock import MagicMock, patch
from src.services.brain import Brain
from src.services.prompts import PERSONAS, DEFAULT_PERSONA

# 1. Test Persona Logic
def test_persona_mapping():
    # Test that personas are correctly mapped for different file extensions
    assert "Senior Python Engineer" in PERSONAS.get(".py", "")
    assert "Frontend Developer" in PERSONAS.get(".html", "")
    assert "Data Engineer" in PERSONAS.get(".json", "")
    
    # Test fallback
    assert DEFAULT_PERSONA == "You are a helpful AI assistant."

# 2. Test Text Cleaning
def test_clean_text():
    brain = Brain()
    
    raw_text = "```python\nprint('Hello')\n```"
    cleaned = brain._clean_text(raw_text)
    
    assert cleaned.strip() == "print('Hello')"

# 3. Test Generation (Fixed Mocking)
@patch('src.services.brain.model') # <--- Patch the GLOBAL model variable in src.services.brain
def test_generate_calls_api_correctly(mock_model):
    # SETUP: Create the fake response
    mock_response = MagicMock()
    mock_response.text = "print('AI Generated Code')"
    mock_model.generate_content.return_value = mock_response

    # ACTION: Run your code
    brain = Brain()
    result = brain.generate("test_script.py", ".py", "Context: None")

    # ASSERTION: Did it return our fake text?
    assert result == "print('AI Generated Code')"
    
    # Did it call the API?
    mock_model.generate_content.assert_called_once()
    
    # Check what we sent to the AI
    args, _ = mock_model.generate_content.call_args
    sent_prompt = args[0]
    
    assert "TASK: Write the code" in sent_prompt
    assert "Senior Python Engineer" in sent_prompt