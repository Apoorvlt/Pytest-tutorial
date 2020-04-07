import pytest
import sys

@pytest.mark.usefixtures('driver')
class TestLink:

    def test_title(self, driver):
        """
        Verify click and title of page
        :return: None
        """
        driver.get('https://lambdatest.github.io/sample-todo-app/')
        driver.find_element_by_name("li1").click()
        driver.find_element_by_name("li2").click()

        title = "Sample page - lambdatest.com"
        assert title == driver.title


