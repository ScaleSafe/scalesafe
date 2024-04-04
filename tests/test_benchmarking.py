import pytest
import requests_mock
from scalesafe.benchmarking import Benchmarker
from scalesafe.exceptions import ScaleSafeTokenError, ScaleSafeException
import os

# Fixture for creating a Benchmarker instance
@pytest.fixture
def benchmarker():
    return Benchmarker(benchmark="test_benchmark", batch_size=5, api_key="test_api_key")

@pytest.fixture
def get_api_key():
    return os.environ.get('SCALESAFE_API_KEY_TEST')

# Mock API responses for successful and failed fetches
@pytest.fixture
def mock_responses(requests_mock):
    # Successful fetch response
    requests_mock.get(
        "https://get-benchmark-datum-zc6tu6qxxa-uc.a.run.app",
        json={
            "data": [{"id": str(i), "content": f"content_{i}"} for i in range(5)],
            "nextLastDocId": "5"
        },
        status_code=200
    )
    # Successful post response
    requests_mock.post(
        "https://post-benchmark-response-zc6tu6qxxa-uc.a.run.app",
        json={"message": "success"},
        status_code=200
    )
    # Failed fetch response
    requests_mock.get(
        "https://get-benchmark-datum-zc6tu6qxxa-uc.a.run.app",
        json={"error": "Unauthorized"},
        status_code=401
    )

# Test initialization of the Benchmarker instance
def test_benchmarker_initialization(benchmarker):
    assert benchmarker.benchmark == "test_benchmark"
    assert benchmarker.batch_size == 5
    assert benchmarker.api_key == "test_api_key"
    assert not benchmarker.is_finished

# # Test fetching the next batch successfully
# def test_fetch_next_batch_success(benchmarker, mock_responses):
#     benchmarker.fetch_next_batch()
#     assert len(benchmarker.data_buffer) == 5
#     assert benchmarker.last_doc_id == "5"


# Test exception when fetching data fails
def test_fetch_next_batch_fail(benchmarker, mock_responses):
    benchmarker.api_key = "invalid_key"
    with pytest.raises(Exception) as e:
        benchmarker.fetch_next_batch()
    assert "Error fetching data" in str(e.value)

# # Test iteration over Benchmarker
# def test_benchmarker_iteration(benchmarker, mock_responses):
#     fetched_items = [item for item in benchmarker]
#     assert len(fetched_items) == 5
#     assert fetched_items[0]['id'] == '0'
#     assert benchmarker.is_finished