import pytest
from unittest.mock import MagicMock, patch
from src.brain import Brain

# 1. Test Persona Logic
def test_get_persona():
    brain = Brain()
    
    # UPDATED: Matches your actual code strings
    assert "Senior Python Engineer" in brain._get_persona(".py")
    assert "Frontend Developer" in brain._get_persona(".html")
    assert "Data Engineer" in brain._get_persona(".json")
    
    # Test fallback
    assert "helpful AI assistant" in brain._get_persona(".unknown_extension")

# 2. Test Text Cleaning
def test_clean_text():
    brain = Brain()
    
    raw_text = "```python\nprint('Hello')\n```"
    cleaned = brain._clean_text(raw_text)
    
    assert cleaned.strip() == "print('Hello')"

# 3. Test Generation (Fixed Mocking)
@patch('src.brain.model') # <--- Patch the GLOBAL model variable in src.brain
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