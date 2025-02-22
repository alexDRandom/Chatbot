import unittest
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import requests
from chatbot import buscar_en_google, extraer_texto, generar_respuesta


# Only mark async tests with asyncio
@pytest.fixture
def mock_serper_response():
    return {
        "organic": [
            {"link": "https://example.com/1", "title": "Test 1"},
            {"link": "https://example.com/2", "title": "Test 2"},
        ]
    }

@pytest.fixture
def mock_webpage_content():
    return "<html><body><p>Test paragraph 1</p><p>Test paragraph 2</p></body></html>"

def test_buscar_en_google_success(mock_serper_response):
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = mock_serper_response
        mock_post.return_value.raise_for_status.return_value = None
        
        results = buscar_en_google("test query")
        
        assert len(results) == 2
        assert results[0]["link"] == "https://example.com/1"

def test_buscar_en_google_error():
    with patch('requests.post') as mock_post:
        mock_post.side_effect = requests.exceptions.RequestException("API Error")
        
        results = buscar_en_google("test query")
        
        assert results == []

def test_extraer_texto_success(mock_webpage_content):
    with patch('requests.get') as mock_get:
        mock_get.return_value.text = mock_webpage_content
        mock_get.return_value.raise_for_status.return_value = None
        
        text = extraer_texto("https://example.com")
        
        assert "Test paragraph 1" in text
        assert "Test paragraph 2" in text

def test_extraer_texto_error():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("Connection Error")
        
        text = extraer_texto("https://example.com")
        
        assert "Error al obtener contenido" in text



class TestGenerarRespuesta(unittest.TestCase):

    @patch('groq.Groq')
    async def test_generar_respuesta(self, MockGroq):
        class MockCompletion:
            def __init__(self, content):
                self.choices = [MagicMock(delta=MagicMock(content=content))]
        
        # Simulamos una respuesta de la API.
        mock_response = AsyncMock()
        mock_response.__aiter__.return_value = [
            MockCompletion("Hello! How can I help you with your test query today?"),
            MockCompletion("Is there something specific you would like to know or test?"),
            MockCompletion("")  # Final empty chunk
        ]
        
        mock_instance = MockGroq.return_value
        mock_instance.chat.completions.create.return_value = mock_response

        # Llamamos a la función con un contexto de prueba.
        context = [{"role": "user", "content": "previous message"}]
        response = await generar_respuesta("test query", context)
        
        # Verificamos que la respuesta no esté vacía y tenga sentido.
        self.assertTrue(response)
        self.assertIn("Hello! How can I help you", response)

    @patch('groq.Groq')
    async def test_generar_respuesta_empty_context(self, MockGroq):
        class MockCompletion:
            def __init__(self, content):
                self.choices = [MagicMock(delta=MagicMock(content=content))]

        mock_response = AsyncMock()
        mock_response.__aiter__.return_value = [
            MockCompletion("Sure! Here is a test query for module \"module_name\" with input \"input_value\":"),
            MockCompletion("```python\nimport module_name\n\nresult = module_name.function_name(input_value)\n```"),
            MockCompletion("")  # Final empty chunk
        ]

        mock_instance = MockGroq.return_value
        mock_instance.chat.completions.create.return_value = mock_response

        response = await generar_respuesta("test query", [])
        
        self.assertTrue(response)
        self.assertIn("Sure! Here is a test query", response)
        self.assertIn("```python", response)

    @patch('groq.Groq')
    async def test_generar_respuesta_long_context(self, MockGroq):
        class MockCompletion:
            def __init__(self, content):
                self.choices = [MagicMock(delta=MagicMock(content=content))]

        mock_response = AsyncMock()
        mock_response.__aiter__.return_value = [
            MockCompletion("Hello! How can I help you with your test query today? Is there something specific you would like to know or discuss? I'm here to assist you with any questions you have to the best of my ability."),
            MockCompletion("Is there something specific you would like to know or test?"),
            MockCompletion("")  # Final empty chunk
        ]
        
        mock_instance = MockGroq.return_value
        mock_instance.chat.completions.create.return_value = mock_response

        context = [{"role": "user", "content": "message"} for _ in range(10)]
        response = await generar_respuesta("test query", context)

        self.assertTrue(response)
        self.assertIn("Hello! How can I help you with your test query today?", response)
        self.assertIn("Is there something specific", response)

if __name__ == '__main__':
    unittest.main()

