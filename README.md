# **SI 506 Final Project README**

## **What does the project do?**

*This program searches the New York Times API for a given query, then provides a list of 10 articles related to that search, sorted by age. The user can then select one of the articles presented, and the program will search flickr for 10 photos for each of the three top keywords the NYT has assigned that article. A HTML file is created using the article details at the top, and sections for each of the three keywords with the photos and photo details listed.*

**What files (by name) are included in your submission?**

 - SI506_finalproject.py
 - API_Keys.py
 - class_Article.py
 - class_createHTML.py     
 - class_Photo.py     
 - project_caching.py
 - SI506finalproject_cache.json
 - README.txt
 - Sample Output.html
 - Sample Output Screenshot.png

**What Python modules must be pip installed in order to run your submission?**
*json, requests, time, datetime*

**Explain SPECIFICALLY how to run your code**
*First, API keys for NYT and Flickr need to be included in the "API_Keys.py" file.
Running SI506_finalproject, the user will be presented with a prompt for a search term. Entering a term will search the NYT's API for up to 10 articles that have at least one keyword and present them to the user, ordered by the age of the article and with a number 0-9 next to each. The user is prompted to select an article by it's number, which gives the program the keywords to make a Flickr search for. The Article details as well as the photo details and images are added to a file titled "{search term}_results.html"*

## REQUIREMENTS LIST:

* Get and cache data from 2 REST APIs (list the lines where the functions to get & cache data begin and where they are invoked):
*Caching is handled in project_caching.py. The request is specifically made in the "Cache.Check" function on lines 53 & 55 of that file. The call to this function is made in SI506_finalproject.py: on line 24 for the NYT API and line 58 for the Flickr API.*

* Define at least 2 classes, each of which fulfill the listed requirements:
    *Classes are in files class_Photo.py (Photo), class_Article.py (Article), and class_createHTML.py (createHTML)*

* Create at least 1 instance of each class:
    *The Article class is instanced in SI506_finalproject.py on line 26
    The Photo class is instanced in SI506_finalproject.py on line 61
    The createHTMl class is instanced in SI506_finalproject on line 76*

* Invoke the methods of the classes on class instances:
    *Article class: "DaysOld" method in the sort in SI506_finalproject.py, line 38
    Photo class: "SourceUrl" method in SI506_finalproject.py, line 87
    CreateHTML class: multiple times in SI506_finalproject.py, lines 77-88*

* At least one sort with a key parameter:
    *Articles are sorted by age once they're retrieved from the API in SI506_finalproject.py, line 38*

* Define at least 2 functions outside a class (list the lines where function definitions begin):
    *"GetArticles" in SI506_finalproject.py, line 11
    "GetPhotos" in SI506_finalproject.py, line 41
    "Check:" in project_caching.py, line 31*

* Invocations of functions you define:
    *"GetArticles" in SI506_finalproject.py, line 65
    "GetPhotos" in SI506_finalproject.py, line 83
    "Check:" in SI506_finalproject.py, lines 24 & 58*

* Create a readable file:
    *"CreateFile" method in class_createHTML.py, lines 22-43. Invoked in SI506_finalproject.py, line 88*
