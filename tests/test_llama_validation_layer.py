import pytest
from unittest.mock import patch, MagicMock
from app.services.generator import note_generator_service

@patch("app.services.generator.InferenceClient")
def test_llama_validation_success(mock_inference_client):
    """Verify that the Llama validation layer successfully validates clinical notes using the correct model and prompt."""
    mock_client = MagicMock()
    mock_inference_client.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Corrected Note: Zyrtec and Paracetamol."
    mock_client.chat_completion.return_value = mock_response
    
    raw_note = "Original Note: sir tech and paracetol."
    transcript = "Start the patient on Zyrtec and paracetamol."
    
    res = note_generator_service._llama_validate_and_correct(
        raw_note=raw_note,
        transcript=transcript,
        hf_token="valid_token_123"
    )
    
    assert res == "Corrected Note: Zyrtec and Paracetamol."
    mock_client.chat_completion.assert_called_once()
    called_args = mock_client.chat_completion.call_args[1]
    assert called_args["model"] == "meta-llama/Llama-3.3-70B-Instruct"
    assert called_args["temperature"] == 0.1

@patch("app.services.generator.InferenceClient")
def test_llama_validation_fallback_on_failure(mock_inference_client):
    """Verify that if the Llama validation layer throws an exception, it falls back to the original note."""
    mock_client = MagicMock()
    mock_inference_client.return_value = mock_client
    mock_client.chat_completion.side_effect = Exception("HF Hub Connection Timeout")
    
    raw_note = "Original Note Content"
    transcript = "Doctor patient conversation transcript"
    
    res = note_generator_service._llama_validate_and_correct(
        raw_note=raw_note,
        transcript=transcript,
        hf_token="valid_token_123"
    )
    
    # Must fallback gracefully to original raw_note
    assert res == raw_note

def test_llama_validation_demo_mode():
    """Verify that in demo mode, the validation layer skips remote client execution and returns the raw note."""
    raw_note = "Original Note Content"
    transcript = "Doctor patient conversation transcript"
    
    res = note_generator_service._llama_validate_and_correct(
        raw_note=raw_note,
        transcript=transcript,
        hf_token="demo"
    )
    
    assert res == raw_note

def test_llama_validation_preserves_free_text():
    """Verify that free-text layout formatting (no headers) is handled correctly."""
    # Free text notes do not contain markdown headers or colons
    free_text_note = "The patient presents with mild cough. Lungs are clear. Return to clinic in 1 week if worsening."
    transcript = "The patient has a mild cough. Lungs are clear. See you in a week."
    
    with patch("app.services.generator.InferenceClient") as mock_inference_client:
        mock_client = MagicMock()
        mock_inference_client.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Corrected Free-Text: The patient has a mild cough. Lungs are clear. Return in 1 week."
        mock_client.chat_completion.return_value = mock_response
        
        res = note_generator_service._llama_validate_and_correct(
            raw_note=free_text_note,
            transcript=transcript,
            hf_token="token_123"
        )
        assert res == "Corrected Free-Text: The patient has a mild cough. Lungs are clear. Return in 1 week."
