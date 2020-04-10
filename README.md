![LambdaTest Logo](https://www.lambdatest.com/images/logo.svg)

## Pytest tutorial

![alt text](https://github.com/Apoorvlt/test/blob/master/pytesti.png)


## Prerequisites for Pytest tutorial 

### 1. Python Installation

 * [Download Python](https://www.python.org/downloads/) and click on Add to path and install.
 
 * To check if python installed correctly you need to go to terminal type python in command prompt. It will show you the current version you have downloaded.
 
### 2. LambdaTest Credentials
  * To use Pytest with LambdaTest, make sure you have the 2 environment variables LT_USERNAME and LT_ACCESS_KEY set. To obtain a username and access_key, sign up for free [here](https://lambdatest.com). After signing up you can find your username and access key [here](https://accounts.lambdatest.com/detail/profile).
  * In the terminal export your LambdaTest Credentials as environmental variables:
       
       * For Mac/Linux
            ```
            $ export LT_USERNAME=<your LambdaTest username>
            $ export LT_ACCESS_KEY=<your LambdaTest access key>
            ```
       
       * For Windows
            ```
            set LT_USERNAME=<your LambdaTest username>
            set LT_ACCESS_KEY=<your LambdaTest access key>
    	    ```	
### 3. Setup

  * You can download the file. To do this click on Clone or download button. You can download zip file.
  * Then open the terminal in the folder you want to clone the file. Run the command:
	
	``` 
	git clone https://github.com/Apoorvlt/Pytest-tutorial.git
  	```
  * After Clone or downloading file you need to setup pytest, selenium and virtual environment. It will isolate the build from other setups you may have running and ensure that the tests run with the specified versions of the modules specified in the requirements.txt file. To run the file you need to open terminal in the project folder:
  
	```bash
    pip install -r requirements.txt
    ```
* Create a virtual environment in your project folder the environment name is arbitrary.

	```bash
    virtualenv venv
    ```
  

## Test Scenario

### Single Test

In our demonstration, we will be creating a script that uses the Selenium WebDriver to click check boxes and add button. If assert returns true, it indicates that the test case passed successfully and will show up in the automation logs dashboard else if assert returns false, the test case fails, and the errors will be displayed in the automation logs.

In desired capabilities we are using windows 10 platform and chrome browser with version 73.

You have successfully configured your project and are ready to execute your first pytest selenium testing script. Here is the configuration file for pytest selenium Testing. Lets call it <code>conftest.py</code>.

	```
	import pytest
	from os import environ

	from selenium import webdriver
	from selenium.common.exceptions import WebDriverException
	from selenium.webdriver.remote.remote_connection import RemoteConnection


	@pytest.fixture(scope='function')
	def driver(request):

	    desired_caps = {}

	    browser = {
		"platform": "Windows 10",
		"browserName": "chrome",
		"version": "73"
	    }

	    desired_caps.update(browser)
	    test_name = request.node.name
	    build = environ.get('BUILD', "Sample PY Build")
	    tunnel_id = environ.get('TUNNEL', False)
	    username = environ.get('LT_USERNAME', None)
	    access_key = environ.get('LT_ACCESS_KEY', None)


	    selenium_endpoint = "http://{}:{}@hub.lambdatest.com/wd/hub".format(username, access_key)
	    desired_caps['build'] = build
	    desired_caps['name'] = test_name
	    desired_caps['video']= True
	    desired_caps['visual']= True
	    desired_caps['network']= True
	    desired_caps['console']= True

	    executor = RemoteConnection(selenium_endpoint, resolve_ip=False)
	    browser = webdriver.Remote(
		command_executor=executor,
		desired_capabilities=desired_caps
	    )
	    yield browser



	    def fin():
		#browser.execute_script("lambda-status=".format(str(not request.node.rep_call.failed if "passed" else "failed").lower()))
		if request.node.rep_call.failed:
		    browser.execute_script("lambda-status=failed")
		else:
		    browser.execute_script("lambda-status=passed")
		    browser.quit()
	    request.addfinalizer(fin)

	@pytest.hookimpl(tryfirst=True, hookwrapper=True)
	def pytest_runtest_makereport(item, call):
	    # this sets the result as a test attribute for LambdaTest reporting.
	    # execute all other hooks to obtain the report object
	    outcome = yield
	    rep = outcome.get_result()

	    # set an report attribute for each phase of a call, which can
	    # be "setup", "call", "teardown"
	    setattr(item, "rep_" + rep.when, rep)
	```

### Test code

	```
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
	```

#### To run single.py file :

     ```
     pytest tests\single.py 
     ```

### Parallel Testing

Lambdatest provides you with parallel testing which helps you to execute multiple files at same time. By default, pytest runs tests in sequential order. In a real scenario, a test suite will have a number of test files and each file will have a bunch of tests. This will lead to a large execution time. To overcome this, pytest provides us with an option to run tests in parallel.

For this, we need to first install the pytest-xdist plugin. Install pytest-xdist by running the following command −
    
    ```bash
    pip install pytest-xdist
    ``` 

### Code
	
	```
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


        def test_item(self, driver):
		"""
		Verify item submission
		:return: None
		"""
		driver.get('https://lambdatest.github.io/sample-todo-app/')
		sample_text = "Happy Testing at LambdaTest"
		email_text_field = driver.find_element_by_id("sampletodotext")
		email_text_field.send_keys(sample_text)

        driver.find_element_by_id("addbutton").click()

	``` 


#### Run Test in Parallel:
   
   ```bash
    pytest tests\parallel.py
   ```

![alt text](https://github.com/Apoorvlt/test/blob/master/cmdc.PNG)


##  Routing traffic through your local machine using Lambdatest
- Set tunnel value to `True` in test capabilities
> OS specific instructions to download and setup tunnel binary can be found at the following links.
>    - [Windows](https://www.lambdatest.com/support/docs/display/TD/Local+Testing+For+Windows)
>    - [Mac](https://www.lambdatest.com/support/docs/display/TD/Local+Testing+For+MacOS)
>    - [Linux](https://www.lambdatest.com/support/docs/display/TD/Local+Testing+For+Linux)



Below we see a screenshot that depicts our Pytest code is running over different browsers i.e Chrome, Firefox and Safari on the LambdaTest Selenium Grid Platform. The results of the test script execution along with the logs can be accessed from the LambdaTest Automation dashboard.


![alttext](https://github.com/Apoorvlt/test/blob/master/Capture.PNG)



### Important Note:
---
- Some Safari & IE browsers, doesn't support automatic resolution of the URL string "localhost". Therefore if you test on URLs like "http://localhost/" or "http://localhost:8080" etc, you would get an error in these browsers. A possible solution is to use "localhost.lambdatest.com" or replace the string "localhost" with machine IP address. For example if you wanted to test "http://localhost/dashboard" or, and your machine IP is 192.168.2.6 you can instead test on "http://192.168.2.6/dashboard" or "http://localhost.lambdatest.com/dashboard".

## About LambdaTest
[LambdaTest](https://www.lambdatest.com/) is a cloud based selenium grid infrastructure that can help you run automated cross browser compatibility tests on 2000+ different browser and operating system environments. LambdaTest supports all programming languages and frameworks that are supported with Selenium, and have easy integrations with all popular CI/CD platforms. It's a perfect solution to bring your [selenium automation testing](https://www.lambdatest.com/selenium-automation) to cloud based infrastructure that not only helps you increase your test coverage over multiple desktop and mobile browsers, but also allows you to cut down your test execution time by running tests on parallel.

### Resources

##### [Selenium Documentation](http://www.seleniumhq.org/docs/)

##### [Python Documentation](https://docs.python.org/2.7/)

##### [Pytest Documentation](http://pytest.org/latest/contents.html)
