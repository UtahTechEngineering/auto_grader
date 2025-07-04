# Python Auto Grader

Used to grade python files. Grades are automatically submitted to canvas when pushed.

## Installation and Configuration

Setting up the auto grader occurs in several phases. 

### Prerequisits

This code requires you to have installed
- Git
- Python
- The following pip packages
    - Numpy
    - Pandas
    - Requests
- Visual Studio Code (Recomended)
- Assignments created in Canvas
- [Github Educators Account](https://github.com/education/teachers) with [Classrooms](https://classroom.github.com/classrooms) access
- Education (I think it free Teams access we get?) or Enterprise Originization on Github

Note these instructions are intended for Mac or Linux. If you are on windows a Bash emulator may be a good idea. I recomend [Git Bash and Visual Studio Code](https://code.visualstudio.com/docs/python/python-tutorial).

If you are new to git you'll need to [configure your git settings and Github authentication](https://docs.github.com/en/get-started/git-basics/set-up-git)

### Write Your Solution Code

First write your solution code. This should behave exactly how you want your students' code to behave. The auto_grader uses funcitons and class methods to evaluate code. Essentially these are input/output tests on these functions. So you should structure your code so that you can check the accuracy of the code based on the output of the function. Note that both functions and class methods are supported.

Your code should be tracked by git. Create a private respository on Github to store this solution code. You can do this by running the following commands in terminal.

    git init
    git add -A # Stages all files (even untracked ones) for commit
    git commit -m "first commit of solution code"
    git branch -M main
    git remote add origin <Solution Code Repository SSH or HTTPS>
    git push -u origin main

### Download the Auto Grader

The auto_grader should be a [submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) within your solution code repository. You can do this using a syntax similar to `git clone`

    git submodule add <This Repository SSH or HTTPS>
    git add -A # Stages all files (even untracked ones) for commit
    git commit -m "Adds auto grader submodule"
    git push origin master



### Initilize Auto Grader Files

The auto grader nees several files in your solution repository's base folder to function properly. I have created a python function to automatically create these files in their proper location. To run that code

    python3
    >>> from auto_grader.DNE_AutoGrader import AutoGrader
    >>> AutoGrader.create_auto_grader_files()

This will initilize the following files

- `.github/workflows/classroom.yml` - Github action workflow to tell Github how to grade the files and send them to Canvas.
- `requirements.txt` - Python dependancies. You can add to these.
- `_create_assignment_files.py` - A file we'll use later in the setup process to generate the files students will run to check their code and CSVs that store the expected output of the student's code.
- `DNE_assignment_info.py` - A file that contains settings and details for each assignment (you can have multiple assignments in each repository)
- `DNE_github_grade_on_push.py` - A file that Github will run to send grades to Canvas.
- `_<folder name of your repository's root>_private_data/_roster.csv` - A file used to corrilate the students Github user names with their Canvas API ID. Students will not have access to this file.

This will not overwrite these files if they already exist. If you would like to overwrite then you need to set the `overwrite` optional input to the `create_auto_grader_files` method to `True`. Just be aware this will delete your roster and assignment settings.

### Optional Set up a Virtual Enviorment

If you have not already, I recomend using a virtual enviorment. To set one up

    pip install virtualenv
    python -m virtualenv <name of virtual enviorment>
    source <name of virtual enviorment>/bin/activate
    pip install -r requirements.txt

**Note** You may need to use `pip3` and `python3` or some other call to pip and python depending on your python installation.

If you already have a virtual enviorment you will need to install `pandas`, `numpy`, and `requests`. I recommed adding them to your `requirements.txt`

### Input The Assignment Information

**Note:** `DNE` (Do Not Edit) before an assignment is to tell students not to edit a file. These files also have a large banner at the top and bottom telling students not to edit them. You, the instructor, are allowed to edit them. In addition to the warning, Github Classrooms has a feature that will let us mark these files as protected. If you use that feature then you will be notified when those files are edited. This discourages students from editing the autograder to always give themselves 100%.

Fill in the following information in the file `DNE_assignment_info.py`.
- `Param.course_id` - Canvas course ID. This can be found by opening the home page of your canvas course and looking at the URL. The course ID is the number at the end.
- For each assignment:
    - `title` - Arbitrary human readable name that will be used to identify the assignmnet in file names and the grade report. I recomend not using spaces.
    - `id` -  Canvas assignment ID. This is where the grade should be posted. This can be found by opening the assignment on Canvas and looking at the URL. The assignment ID is the number at the end.
    - `input_shapes` - A list of tuples. Each list entry is associated with a different input to the function. The tuples contain numbers indicating the shape of the numpy array that this input expects. The order of the tuples should match the order of the inputs to the function. Currently this auto grader can only work with numeric inputs and outputs.
    - `output_shapes` - Same as the input shapes but now for the outputs.
    - `input_ranges` - This is a list of the same length of the input shapes. However, instead of tuples representing the shape. It is a numpy array of the previously specified shape. Each entry in the numpy array is a tuple with two entries. The first entry represents the lowest possible value that component of the input can be and the second represents the highest. input_ranges is used to randomly generate inputs to the function. Notably, the tuple will be interpreted as another dimension in the numpy array. So for exmple if the first entry in the `input_shapes` is `(3,4)` then the first entry in `input_ranges` will have the shape `(3,4,2)`. This also means that there is some duplicate information. We could technically get the shape from the dimension of `input_ranges`. However seperating them like this simplifies the code and helps to stop errors.
    - `input_labels` - a list of strings of the same length as `input_shapes`. Each string should be the variable name of the corrisponding input. This name will be used to report where mistakes are to the student.
    - `function_to_evalutate` - There are two ways to define this variable depending on if you need to test a function or a class method
        - **Function** - If you need to test a function then simply put the name of the function in the variable `function_to_evalutate`. It should not be a string. Something as simple as `function_to_evalutate=len`
        - **Class Method** - If you need to evaluate a class method then you also need to set two additional variables
            - `class_to_evaluate` - Simply put the name of the function in the variable `class_to_evaluate`. It should not be a string. Something as simple as `class_to_evaluate=np`
            - `class_inputs` - A dictionary containing the inputs used to instantiate the class. Notably this is only done once during a given auto grader run. The key should be the variable name of the input to the contstructor and the value should be the input you want. The order should be consistant with how you would typically instantiate the class. For example, if I had a class defined as `class example: def __init__(self, a: int, b: int, c: int = 3): pass` Then I would set `class_inputs = {"a":1, "b":2, "c":3}`.
            - `function_to_evalutate` - Now `function_to_evalutate` should be a string with the name of the method you want to test. For example `function_to_evalutate="len"`.

All of these variables are used to create an `Assignment` object which is then appended to the list `assignment`. This list of assignments is then input into the the `AutoGrader` constructor along with the `AutoGraderParam` variable `Param`. You can append as many assignments to the assignment list as you would like. Create each assignmnet in the same way as described above. `Param` stores the settings which should apply to all assignments. Each time the autograder is used, this script is run and the `auto_grader` variable of type `AutoGrader` is imported. 

You also need to set up the `_<folder name of your repository's root>_private_data/_roster.csv` file. To do this you need the Github username for each student and the Canvas Student ID for each student. Notably, this is not your institution student ID. Canvas assigns an ID to each student. Like the course ID the student ID can be found by navigating to `Grades` tab, clicking on a student name, clicking on their name again in the tab that appears, and looking at the URL. The student ID is the number at the end. However, in a large class I suggest creating an quiz (I suggest making it a survey so credit can be given for completion) with a single essay question asking students to type in their Github Username. Tell the students to make sure it is typed correctly (spelling, case, and no extra white space). Then download their answers by clicking `Student Analysis` in the `Statistics` tab of the survey. The Canvas student ID is the ID column of the generated CSV. The Github usernames are also list in this CSV. So you can copy both over to the appropriate column of the roster `_<folder name of your repository's root>_private_data/_roster.csv`.

Finally, open the file `.github/workflows/classroom.yml` and find the comment `# private grader repository goes here`. Put the following there: `<your orginization name>/_<folder name of your repository's root>_private_data`

#### Tips for Setting Up Assignmnets

There is a lot of flexibility in this setup. For example, if you would like to create an assignment that grades two functions (or class methods) simply create a dummy function (or class) which takes all of the inputs to both functions (or class methods), evaluates each function (or class method) seperately, and returns all of the outputs of both functions (or class methods). The dummy class constructor can be used to construct multiple objects for testing. The only disadvantage of this is that when reporting errors to the student, the name of the function where error occured will be the name from the dummy function. However, the standard error traceback is provided and most of the debuging should occur when testing the code, not when grading it. By that I mean, I like to include seperate scripts in my solution code that simply use the functions so I can confirm proper behavior before using the autograder. Students can do the same. This is good coding practice. 

You can also do other things in this file. For example, I've used the assignment info file to allow students to choose which problems they want to complete from a subset. The assignment `title` is used to find the solution data but the assignment `id` is used to specify where to submit the grade on canvas. So to do this I have students specify (using true/false booleans) which problems they want to complete in a different file. Then, in this file I import those responses and use that logic to set the assignment IDs. Then I only append the choosen assignments to the `assignments` list. In general, do not forget to import any functions and classes you want to evaluate.

#### Optional Settings

The `AutoGraderParam` class also has several other global settings you can adjust. They are

- `iterations` - The number of times to evaluate the test function (each time with different inputs). Default is `1e4`.
- `tolerance` - The auto grader simply checks if the students solution is close to your provided solution. This variable defines how close they need to be. If the difference is less than this value then the students solution is considered correct. This helps account for issues like machine floating point precision errors. Default value is `1e-10`.
- `total_average_report_blocks` - When the code is posted to Canvas a comment is added to a pull request on Github called `Feedback`. This comment gives details about the autograder's results. This includes a table listing each output and if it was correct or not. In my work, it is common for some outputs to begin correct, but then slowly diverge from the solution (i.e. persistant variables). So it is useful to debugging to see how the error changes over time. To that end I added a plot of sorts. It is a colored line for each output. Green represents an correct output and red represents an incorrect output. The darker the shade of red the larger the error is. The line is broken into `total_average_report_blocks` segments. So each segment represents the total error over `iterations/total_average_report_blocks` test cases. The default is `10`. Note that adding too many segments (i.e. blocks) may make this portion of the pull request comment difficult to read.
- `late_penalty_per_day` and `late_penalty_floor` - The late penalty functionality works identical to Canvas's built in late penatley. If the submission is late then `NEW_GRADE = max(late_penalty_floor, GRADE - late_penalty_per_day * days_late)`. However, I am not a fan of how Canvas allows the grade to decrease on future submissions. So if the new grade (after the late penalty if there is one) is lower than the original grade then the original grade is kept.

The autograder prints a detailed log of its process. It also prints that log to the file `auto_grader/_log.txt`. It stores 1,000 lines of the log before deleting the oldest lines. You are welcome to `from auto_grader.DNE_log import log` to use this logging capablity elsewhere. The syntax is `log(message, type=type_string)`. The variable `type_string` is allowed to be
- `"info"`
- `"debug"`
- `"grade"`
- `"warning"`
- `"error"`
- `"break"`
Each of these is formated slightly differently (i.e. an identifying prefix applied). `message` should be a string unless you are using the `"grade"` type. Then it should be a number. The `message` for the `"break"` type is ignored. Instead a line of arrows is printed to seperate the log into chunks. This is done everytime the logger is imported (i.e. the start of a logging session).

You can also set some settings for the logger. These are intended to be edited less frequently (if at all). So you have to edit the file `auto_grader/DNE_log.py`. The settings are

- `print_to_log_file` - Weather or not to print to the `auto_grader/_log.txt` file.
- `print_to_console` - Weather or not to print to the console. Note that disabling this will make it hard to see what happened in Github's logs because, as things stand now, the `auto_grader/_log.txt` file is not saved after a github run.
- `print_info` - Weather or not to print the `"info"` type.
- `print_debug` - Weather or not to print the `"debug"` type.
- `print_warning` - Weather or not to print the `"warning"` type.
- `print_error` - Weather or not to print the `"error"` type.
- `print_grade` - Weather or not to print the `"grade"` type.
- `print_break` - Weather or not to print the `"break"` type.

All of these are booleans with default values `True`.

### Initilize Assignment Files

Now that the assignment information is input we can intilize the assignment files. A script has been provided to do this for you.

    python3 _create_assignment_files.py

This will create the following files

- `_<folder name of your repository's root>_private_data/_<assignment title>_grader_data.csv` - These files contain all of the secret test data that *Github* will use to check the students work. It is essential a list of correct input/output pairs. Students *will not* have access to these files.
- `auto_grader/DNE_<assignment title>_checker_data.csv` - These files contain all of the test data that *students* will use to check their work. It is essential a list of correct input/output pairs. Students *will* have access to these files. By keeping two sets of input/output test data, one secret one not, students are able to check their work, but won't be able to see the data their grade is based on. This discurages students from simply writing code to pull the correct output from the data file.
- `DNE_<assignment title>_check.py` - These file are the files students will run to test their code locally (before pushing to Github and Canvas).

The check and grade CSVs are always overwritten. If you would like to overwrite the check python files then you need to set the `overwrite` optional input to the `create_assignment_files` method to `True`. This can be done in the `_create_assignment_files.py` file.

Everything is now setup and you should be able to run the autograder. To test it you can run the `DNE_<assignment title>_check.py` files and the `DNE_github_grade_on_push.py` file. To run the `DNE_github_grade_on_push.py` you will need to supply the required arguments `--github_actor` which should be the github username of the student (I suggest setting up a test account on Github) and `--canvas_api_token` which is the Canvas API token (I'll tell you to set this up later, but you can see how to do it [here](https://community.canvaslms.com/t5/Canvas-Basics-Guide/How-do-I-manage-API-access-tokens-in-my-user-account/ta-p/615312))

**Note:** The print statements in the student's code are suppresed to stop the console from being clogged with print statments that students left in the code after debuging.

### Commit Changes

Now that everything works we should save it all in Git.

First, the autograder must be on a branch to avoid merge issues (see [here](https://git-scm.com/book/en/v2/Git-Tools-Submodules#Working_on_a_Submodule) for more details). 

    cd auto_grader
    git branch local
    git checkout local
    git add -A # Stages all files (even untracked ones) for commit
    git commit -m "Local version of auto grader"

Now you can update the auto_grader using

    # From the root repository
    git submodule update --remote --merge 
    # OR from the auto_grader folder 
    git checkout main
    git pull
    git checkout local
    git merge main

If you merge a development branch into main and push you can also contribute to the auto grader this way.

Then from your project root directory you can do as you tpycially would

    git add -A # Stages all files (even untracked ones) for commit
    git commit -m "adds auto grader"
    git pull
    git push

**Note:** Becasue we have moved/created some files out of the autograder, they are no longer tracked in the git submodule. If you pull changes to the auto grader that change these files (or how they are created in the autograder), then you need to copy them over again. This can be done by using the `overwrite` flag in the `create_auto_grader_files` and the `create_assignment_files` methods. Just be aware this will delete your roster and assignment settings.

## Set Up Github Secrets

Create two [Github orginization wide action secretes](https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-guides/using-secrets-in-github-actions).
- `CANVAS_API_TOKEN` - Generate an API token following [these instructions](https://community.canvaslms.com/t5/Canvas-Basics-Guide/How-do-I-manage-API-access-tokens-in-my-user-account/ta-p/615312) and save it in this Github secret.
- `GITHUB_PAT` - Generate a fine-grained Personal Access Token (PAT) following [these instructions](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) and save it in this Github secret. Your token needs the following access:

    - Access to all repositories in your orginization.
    - No orginization permissions
    - For Repositories:
        - Read access to code and metadata
        - Read and Write access to issues and pull requests

## Set Up Support Repositories

You will need two forks of your main solution repository. They need to be named as follows

- `_<folder name of your repository's root>_private_data` - In this fork delete everything except the contents of the `_<folder name of your repository's root>_private_data` folder. Move those contents so that they are in the root directory. There should be no folders in this repository.
- `<folder name of your repository's root>_skeleton` - Make this repository a [template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository) repository in the Github settings. In this fork delete the following
    - All solutions that you want the students to complete (it might be good to mark these areas with comments)
    - All files with an underscore before them.
        - `_create_assignment_files.py`
        - `auto_grader/_log.txt`
        - `auto_grader/_pull_request_comment.md`
        - `auto_grader/_assignment_info_template.py`
        - `auto_grader/_classroom.yml`
        - `auto_grader/_requirements.txt`
        - All `auto_grader/_<assignment title>_test_data.csv` files
        - The entire `_<folder name of your repository's root>_private_data` folder.

You can fork on Github using [these instructions](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo). You can then make the required changes by using

    git clone <Forked Repository URL>
    # Make the changes as you normally would (e.g. in visual studio code)
    git add -A # Stages all files (even untracked ones) for commit
    git commit -m "Removes unnesisary files"
    git push

## Set Up Github Classrooms

In github classrooms create a new class. Link it to Canvas following [these instructions](https://docs.github.com/en/education/manage-coursework-with-github-classroom/teach-with-github-classroom/connect-a-learning-management-system-course-to-a-classroom#linking-a-canvas-course-with-a-classroom). You will need to ask your Canvas Adminstrator for the Github Client ID. This will allow you to import the student list. I like to import thier names for easy identification, but that is optional.

## Create an Assignment

Create a new assignment.

Set the deadline and title as desired.

Select the skeleton code template repository you created earlier as starter code. 

Make repositories private.

Don't grant admin access to the students.

Do copy only the default branch.

Select custom YAML

Select all files labeled as DNE in the protected file paths section. 

**Enable the Feedback Pull Request**

Finally give the students the provided link. I like to put it in the assignment description on Canvas.

## Making Changes

If you need to update an assignment you would follow this work flow:

1. Make the changes in your solution repository
2. Merge them into both forked repsotiories using [these instructions](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests).
3. Make the same changes in the assignment fork of the template. Github Classrooms does this annoying thing where it creates a fork of the template that has a diconnected history. So you need to find the template fork (avlaible from the assignment page on Github classrooms) and make the changes manually a second time. You might be able to do this by cloning the template fork and rebasing any changes. I haven't experimented with it.
4. On the Github classroom page click `Sync Assignments` to create a pull request on each students version of the homework repository. 
5. Tell the students to merge the pull request.


## Security

This auto grader is not perfectly secure. There are still ways for students to get around the autograder pretections. Such efforts would be complicated and propably more difficult than simply completing the given asssignment (depending on your assignment). The user is reminded that it is impossible to make a system unhackable (or an assignment uncheatable). Instead the goal is to make it more work than it is worth to hack (or cheat) an assignment. Cheaters are looking for an easy way out, so I have designed this system so that the "easy way out" is usually doing the actual assignment. However, to be clear this code is provided on an as is basis with no garuntees of security. The instructor using this code assumes all the risk of potential cheeting.
