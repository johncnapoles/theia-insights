# Christian Napoles SW Engineer Take-home project

This repository is my solution to the external take-home project for Theia Insights.

The project is comprised of two parts: `Data Pipeline` and `Web API`.

**Data Pipeline:**

- The input is a folder of HTML files, one file per company (see [snippet A](#snippet-a---example-input-file) for one file).
- The first processing stage parses the HTML to:
  1. extract the `ticker symbol`,
  2. extract the `company name`, and
  3. extract the `text description` of the company.
- Then, use the `flax-sentence-embeddings` model to find the cosine similarity between the company text description and the 10 themes given in the specification (see [snippet B](#snippet-b---example-theme-line) for one line).
- The output is a JSON-lines file, where each line contains:
  1. the `ticker symbol`,
  2. the `company name`,
  3. the `3 most similar themes`, and
  4. the `text description` of the company.

**Web API:**

- The processed data is served through an API implemented in Python.
- The project uses the _FastAPI_ framework and returns an OpenAPI specification.
- The API has 2 endpoints:
  1. given a theme name, get a list of ticker symbols.
  2. given a ticker symbol, get the company name, description, and list of themes

---

### Project Structure

A quick overview of the project structure:
- `constants/` - directory housing the constants for re-use, separated by concerns.
- `db/` - directory housing the database configs, helper functions and the database file itself.
- `inputs/companies/` - directory housing all the input company HTML files to parse.
- `inputs/themes.txt` - the input text file of all the themes used for the sentence embedding model.
- `logs/` - directory for the log files, separated by concerns. Useful for future instrumentation, analytics and visualization.
- `outputs/` - directory for processed data files. To be used by the web API.
- `tests/` - directory housing the Pytest tests.
- `tests/test_data/` - directory for supplementary data for cleaner testing.
- `__init__.py` - file necessary for treating directory like a package.
- `.gitignore` - file to ignore pushing certain files to github.
- `uitls/` - directory housing shared utility functions, such as logger.
- `A_process_data_pipeline.py` - python file to execute data pipeline process. to classify business activities into themes.
- `B_serve_web_api.py` - python file to serve the web API.
- `LICENSE` - standard github license.
- `README.md` - this file.
- `requirements.txt` - list of all the external libraries and versions.

---

### How to Build

> _Note: whilst this project was built in Python v3.8, it should generally work with the latest version of Python_

#### 1. Setting up the Python virtual environment

It is highly reccommended to set up a virtual environment to download external packages for this project.

to create your virtual environment

```bash
python -m venv .venv
```

activate your virtual environment

```bash
#for Unix or MacOS
source .venv/bin/activate

#for Windows
.\.venv\Scripts\activate
```

deactivate your virtual environment when you are done

```
deactivate
```

#### 2. Installation

> _Note: It is reccomended to do this stage with your virtual environment activated._

Some installations are required to use external libraries.

- `jsonlines` - library related to jsonline file format
- `sentence-transformers` - library to leverage the flax-sentence-embeddings model for sentence similarity comparisons
- `beautifulsoup4` - HTML parsing
- `SQLAlchemy` - toolkit for object-relational mapping and databases.
- `fastapi` - python web api framework
- `uvicorn` - web server implementation for the fastapi framework
- `pytest` - python testing framework
- `pytest-mock` - to assist with mocking functions for testing
- `httpx` - to assist with testing the web api

> Note: installing libraries like `sentence-transformers` could take a while. Please be patient.

**Automatically (recommended method):**
run the following code

```bash
pip install -r requirements.txt
```

**Manually (an alternative method):**
run the following code

```bash
pip install jsonlines==4.0.0
pip install sentence-transformers==2.3.1
pip install beautifulsoup4==4.12.3
pip install SQLAlchemy==2.0.27
pip install fastapi==0.109.2
pip install uvicorn[standard]==0.27.1
pip install pytest ==8.0.1
pip install pytest-mock==3.12.0
pip install httpx==0.26.0 
```

#### 2. How to run the code

Firstly, run the script to process the data

```bash
python ./A_process_data_pipeline.py
```

You should see console logs like the following

```
[2024-02-20T06:56:57.921][INFO]STARTED process_data_pipeline.py
[2024-02-20T06:57:00.305][INFO]Done parsing themes. There are 10 themes: ['electric-vehicles', 'manufacturing', 'solar-energy', 'mobile-phones', 'telecommunications', 'audio-products', 'cloud-computing', 'retail', 'e-commerce', 'consumer-products'][2024-02-22T06:57:00.404][INFO]Done parsing companies. There are 3 companies. Last three: ['AAPL', 'TSLA', 'WMT']
[2024-02-20T06:57:00.405][INFO]Done saving keys of themes into: outputs/theme_names.txt
[2024-02-20T06:57:00.409][INFO]Done determining top 3 themes for every company.        
[2024-02-20T06:57:00.409][INFO]Done saving processed company data.
[2024-02-20T06:57:00.410][INFO]FINISHED process_data_pipeline.py
```

Once the script is complete, run the following to serve the web api:

```
uvicorn B_serve_web_api:app
```

You should see console logs like the following

```
INFO:     Will watch for changes in these directories: ['C:\\Users\\User\\Desktop\\theia-insights']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [7616] using WatchFiles
INFO:     Started server process [18208]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
Awesome, you're all ready to use the web API!

#### 3. How to call the web API endpoints

By default and for the scope of the project, the server is running locally in port 8000 (`http://127.0.0.1:8000`)

After successfully serving the web API you can now call the following 2 endpoints:

**GET** `/v1/companies/{ticker}`

- This endpoint will return the company associated with the supplied ticker symbol.
- If found, the response will contain the company's ticker, name, description, and top themes. 
- If the ticker is not in an expected format or does not return a company, the appropriate error will be given.
- successful response example:

```
{
  "company_description": "Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops, and sells consumer electronics, computer software, and online services. It is considered one of the Big Five companies in the U.S. information technology industry, along with Amazon, Google, Microsoft, and Facebook. Its hardware products include the iPhone smartphone, the iPad tablet computer, the Mac personal computer, the iPod portable media player, the Apple Watch smartwatch, the Apple TV digital media player, the AirPods wireless earbuds, the AirPods Max headphones, and the HomePod smart speaker line. Apple's software includes iOS, iPadOS, macOS, watchOS, and tvOS operating systems, the iTunes media player, the Safari web browser, the Shazam music identifier, and the iLife and iWork creativity and productivity suites, as well as professional applications like Final Cut Pro X, Logic Pro, and Xcode. Its online services include the iTunes Store, the iOS App Store, Mac App Store, Apple Arcade, Apple Music, Apple TV+, Apple Fitness+, iMessage, and iCloud. Other services include Apple Store, Genius Bar, AppleCare, Apple Pay, Apple Pay Cash, and Apple Card.",
  "company_ticker": "AAPL",
  "company_name": "Apple Inc.",
  "company_top_themes": "[\"audio-products\", \"cloud-computing\", \"manufacturing\"]"
}
```

**GET** `/v1/companies/list-by-theme/{theme}`

- This endpoint will return a list of companies that contain the same theme names.
- If at least one company matches, the response will contain the theme name, the number of matches, and the list of company tickers.
- If the theme does not exist in the processed data or if no companies is found with the theme, the appropriate error will be given.
- successful response example:

```
{
  "theme_name": "manufacturing",
  "number_of_matches": 2,
  "data": [
    "AAPL",
    "TSLA"
  ]
}
```

For more information about the endpoints or a visualization, please refer to the OpenAPI (v3.1.0) swagger documentation, which is available whenever the application is served: http://127.0.0.1:8000/docs#/

You can also:

- see it directly as a json http://127.0.0.1:8000/openapi.json
- see an alternative documentation via http://127.0.0.1:8000/redoc

#### 4. How to run the pytest unit tests

To test the project, run the following code:
```
pytest
```

You should see console logs like the following
```
================================== test session starts ==================================
platform win32 -- Python 3.8.3, pytest-8.0.1, pluggy-1.4.0
rootdir: ###\theia-insights
plugins: anyio-4.3.0, mock-3.12.0
collected 38 items

tests\test_process_data_pipeline.py ..........................                     [ 68%]
tests\test_serve_web_api.py ............                                           [100%]

================================== 38 passed in 4.89s ===================================
```

---

### Decisions and Assumptions
The purpose of this section is to explain and think out loud my considerations when designing the code, to highlight my careful attention to detail:

**1. Error Handling**
- Malformed HTML is common and is expected to be handled elegantly in a way that does not stop the data processing.
- I try to use the _fail-fast_ pattern and error out as soon as possible for defensive programming, especially when handling with HTMLs.
- Skipped data is logged at an error level to grab the attention of the data processor.
- With few information to go by, plenty of assumptions were made to guarantee that the data is valid. Whilst there are rigid, this guarantees the code runs smoothly for serving data to the web API:
  - the theme name must match the regex `r"^[a-zA-Z0-9][a-zA-Z0-9-.#&]*[a-zA-Z0-9]$"`
  - the tags structure of the HTML file must match the expected structure:
  `["html", "head", "title", "body", "h1", "h2", "p"]`
  - company name is pulled from the HEAD -> TITLE, and must match the title from Body -> H1
  - company name must follow the format `Company Description:<company name>`
  - if any of the company's name, description, ticker is missing , skip the file
  - a supplied ticker must be match the regex `r"^[A-Z]{1,6}$"`
  - etc...
- Should the requirement ask for more flexibility, the code is modularized to easily allow for extension
- Web API errors are accounted for with data validation based from the processed data. For example, only themes that have been processed are valid inputs.

**2. Scale**
- I made the reasonable assumption that The list of companies will grow significantly larger than the list of themes, so more robust ways to handle parsing companies is needed.
- I made sure to use data structures that are space efficient, like dictionaries.
- I also made sure to use a database to query the persistent data source rather than loop through a jsonline file repeatedly.
- I made sure that the data processing code tries not to repeat any unecessary code, such as compiling the regex pattern only one and passing it when necessary.
- pre-processing the data into small functions with specific tasks allows my code to be extended for multi-threading, something that is out of scope for the size of the task.
- There is still plenty to do to accommodate the larger scale of companies, which is mentioned in the Further Work section below. Whilst it is possible to code, I focused on a complete and solid solution.

**3. Instrumentation**
- We can monitor requests to the API endpoint with logging, such that it can verify that the API is operational, and give us meaningful insight into how the API is used.
- Logs for the data processing are separated from the logs for web API.
- Logs are timestamped, contain request_ids, and contain the request and response details. This enables us to understand the entire enduser journey.
- In addition categorical and standardized logging with meaningful log messages is a strong foundation for analytics. We can collect groups of the same requests into buckets for data visualization of API use.

**4. Python API framework**
- I chose FastAPI as my framework because it is lightweight, powerful and fit for purpose for the scope of the task of creating two endpoints.
- For example, the framework allows for automatic OpenAPI documentation generation, and testing works seemlessly with Pytest. 
- The ability to write fast yet powerful API endpoints with type hints and schemas help me implement RESTful APIs
- I also used SQLite with the SQLAlchemy toolkit to easily analyze the contents of the jsonline output, because it is far better than 
- Should the project grow larger, perhaps frameworks like Django and databases like PostgreSQL will be more robust. However the boiler plate outweighed the marginal benefit.

**5. Other Considerations**
- _naming_: function and variable names are simple without specialist language. The order of function execution is intuitive.  Readability and extensibility is the focus. The code uses the _ruff_ linter.
- _structure_: files are also organized in a way that is common to most developers.
- _comments and docstrings_: functions are given succint docstrings to summarize what they do, adhering to [PEP-257](https://peps.python.org/pep-0257/)
- _information and visual fatigue_: I make sure to log or output the most meaningful information, in a way that is easy to read. I also balance it with not being to verbose.

---

### Further Work

To further demonstrate my skill to _"forsee design requirements"_, the following is a non-exhaustive list of future requirements are out of scope that I think are the logical next steps for :

Data Pipeline:
- _AI to correct malformed data_: A creative extension to the design is to use the malformed file to correct itself. If the name of the company is missing, it is probably mentioned in the company description. Having a model infer a company name could prevent unwanted skipping of malformed files.
- _Multi-threading_: In the event that the list of companies grows to the order of millions or more, perhaps having more than one threads or processes processing on a split workload of files to process can improve speed.
- _Accounting for processed unchanged inputs_: whilst it is uncommon to repeatedly parse the same data, in the event of having to process skipped files, mechanisms can be implemented to prevent unecessary re-processing of files. Examples include moving processed files to another directory, OR having as hashing a directory and saving the value to check if the directory has changed since.
- _Graphing of data_: another area of data processing is visualizing with graphs and the interconnections between companies and themes or other companies.
- _Testing_: having full code coverage is ideal to guarantee functions and paths of code work as expected, eliminating one source of unexpected errors.

Web API:
- _Extending the API_: The data source lends itself to many more meaningful endpoints for queries. For example, "given a company, which company has themes?"
- _API Security_: Currently, the web api is accessed locally without any authorization checks. When a project scales and has many users, it is important to limit usage to intended users. For example: API-Keys or OAuth
- _Logging Visualization_: With categorized logs, we can easily use charts to visualize activity of the API and filter them by time periods and dig deeper into individual requests.
- _Data Obfuscation_: Currently, logging is verbose to allow for ease of intrumentation. If the data is seen as sensitive, it is possible to obfuscate logged details.
- _Pagination_: This is not necessary for the two endpoints seeing as one returns a single company's details, and the other endpoint returns a list of small ticker symbols. This may be more relevant with other endpoints that lists, or if the list of ticker symbols is significantly larger.
- SQL Injection: This is standard to protect yourself whenever SQL-like databases are involved. This is not a problem because validations for each endpoints is set in place, but more robust methods can be used.

---

### Snippets

###### Snippet A - Example input file

```HTML
<HTML>
<HEAD>
<TITLE>Company Description: Walmart Inc.</TITLE>
</HEAD>
<BODY>
<H1>Walmart Inc.</H1>
<H2>Ticker: WMT</H2>
<P>
    Walmart Inc. is an American multinational retail corporation that operates a chain of hypermarkets, discount department stores,
    and grocery stores from the United States, headquartered in Bentonville, Arkansas. The company was founded by Sam Walton in
    1962 and incorporated on October 31, 1969. It also owns and operates Sam's Club retail warehouses. As of October 31, 2021,
    Walmart has 11,443 stores and clubs in 26 countries, operating under 56 different names. The company operates under the name
    Walmart in the United States and Canada, as Walmart de México y Centroamérica in Mexico and Central America, and as Flipkart
    Wholesale in India. It has wholly owned operations in Argentina, Chile, Canada, and South Africa. Since August 2018, Walmart
    holds only a minority stake in Walmart Brasil, which was renamed Grupo Big in August 2019, with 20 percent of the company's
    shares, and private equity firm Advent International holding 80 percent ownership of the company.
</P>
</BODY>
</HTML>
```

###### Snippet B - Example theme line

```text
...
Solar Engergy: The solar energy theme includes companies that facilitate and produce renewable energy through the use of solar-powered products, services, and systems. These companies focus on creating efficient, sustainable, and cost-effective solutions to reduce the world's dependence on fossil fuels and provide a clean energy source. Solar energy companies have developed a variety of technologies from solar photovoltaics and solar thermal systems to solar tracking systems and solar parks. Companies within the theme are leveraging these innovations to power homes, businesses, and cars.
...
```
