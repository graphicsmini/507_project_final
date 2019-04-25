# SI 507 Final Project

Youngmin Kim

[Link to this repository](https://github.com/graphicsmini/507_project_final)

---

## Project Description

My project will aggregate the National Park data in United States. It allows users to see the list of parks in each state page. There will be a route for looking at the number of park in States. In another route, the clickable names of states will be listed. When users click one state, they would see the list of parks with the information such as type, location and description.

## How to run

1. First, you should install all requirements with `pip3 install -r requirements.txt`
2. Second, you should run `python3 SI507project_tools.py runserver`


## How to use

1. When you run the program, you will see the number of parks in the states. Click **Browse all states**. *(See sample_screenshots/sample_screenshot_1.png)*
2. You will see the list of states, click **Connecticut**. *(See sample_screenshots/sample_screenshot_2.png)*
3. You will see 5 parks informations which are **Appalachian, New England, The Last Green Valley, Washington-Rochambeau, Weir Farm**. *(See sample_screenshots/sample_screenshot_3.png)*
4. You can always go back to the list of states by clicking 'Return to State list' on the bottom.


## Routes in this application
- `/index` -> this is the home page
- `/all_states` -> this route has a list of states
- `/state/<state>` -> this route is showing parks' information in this 'state'


## How to run tests
1. First, make sure that you installed all modules in 'requirements.txt'.
2. Second, run SISI507project_tools.py to generate 'nps.csv' file and 'nps.db' file which are going to use in the test. 
3. Lastly, run SISI507project_tests.py 


## In this repository:
- SI507project_tools.py
- SI507project_tests.py
- Templates/
  - index.html
  - all_states.html
  - each_state.html
- nps_sample.db
- sample_screenshots/
  - sample_screenshot_1.png
  - sample_screenshot_2.png
  - sample_screenshot_3.png
- advanced_expiry_caching.py
- requirements.txt
- README.md
- data_structure.png


---
## Code Requirements for Grading
Please check the requirements you have accomplished in your code as demonstrated.
- [x] This is a completed requirement.
- [ ] This is an incomplete requirement.

Below is a list of the requirements listed in the rubric for you to copy and paste.  See rubric on Canvas for more details.

### General
- [x] Project is submitted as a Github repository
- [x] Project includes a working Flask application that runs locally on a computer
- [x] Project includes at least 1 test suite file with reasonable tests in it.
- [x] Includes a `requirements.txt` file containing all required modules to run program
- [x] Includes a clear and readable README.md that follows this template
- [x] Includes a sample .sqlite/.db file
- [x] Includes a diagram of your database schema
- [x] Includes EVERY file needed in order to run the project
- [x] Includes screenshots and/or clear descriptions of what your project should look like when it is working

### Flask Application
- [x] Includes at least 3 different routes
- [x] View/s a user can see when the application runs that are understandable/legible for someone who has NOT taken this course
- [x] Interactions with a database that has at least 2 tables
- [x] At least 1 relationship between 2 tables in database
- [x] Information stored in the database is viewed or interacted with in some way

### Additional Components (at least 6 required)
- [x] Use of a new module
- [ ] Use of a second new module
- [ ] Object definitions using inheritance (indicate if this counts for 2 or 3 of the six requirements in a parenthetical)
- [ ] A many-to-many relationship in your database structure
- [ ] At least one form in your Flask application
- [x] Templating in your Flask application
- [ ] Inclusion of JavaScript files in the application
- [x] Links in the views of Flask application page/s
- [ ] Relevant use of `itertools` and/or `collections`
- [x] Sourcing of data using web scraping
- [ ] Sourcing of data using web REST API requests
- [x] Sourcing of data using user input and/or a downloaded .csv or .json dataset
- [x] Caching of data you continually retrieve from the internet in some way

### Submission
- [x] I included a link to my GitHub repository with the correct permissions on Canvas! (Did you though? Did you actually? Are you sure you didn't forget?)
- [x] I included a summary of my project and how I thought it went **in my Canvas submission**!
