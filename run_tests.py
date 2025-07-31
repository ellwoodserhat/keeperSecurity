import pytest

if __name__ == "__main__":
    pytest.main(["-v", "api_testing/", "--html=reports/index.html", "--self-contained-html"])
