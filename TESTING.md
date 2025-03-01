# Testing

This project uses [pytest](https://pytest.org/) to run tests for both API functionality and Flask endpoints.

## Setup

1. **Activate Your Virtual Environment:**

   ```bash
   source venv/bin/activate

2. **Set the PYTHONPATH:**

   ```bash
   export PYTHONPATH=.

## Running Tests
Simply running "pytest" will automatically discover tests in the tests directory:

``
pytest
``


## Testing Strategy

- **Endpoint Tests:**
  - Tests for Flask routes (e.g., the index route).
  - Uses monkeypatching (in `weather.views`) to replace the real API call with dummy data.
  - Checks HTML content for expected weather details.

- **API Function Tests:**
  - Tests for the `fetch_weather` function.
  - Simulates successful and failed API responses by monkeypatching `requests.get` with dummy functions.

## Adding New Tests

- Create new test files in the `tests/` directory with filenames starting with `test_`.
- Use pytest fixtures to create an isolated testing environment.
- Use `monkeypatch` to override external calls for consistent, predictable test results.

