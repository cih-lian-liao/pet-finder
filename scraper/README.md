Dear Professor and Dear TA,

This is Group 1. We have some instructions but have no ideas where to put them. So we write this additional note for you to run our website on your own computers as a local server. Please kindly read the below steps before operating it. Thank you!


Steps to run the website on a local machine:

1. Create a project folder, let's call it "final_project_part_1_web_scrape" or so.
2. Download the code folder(Scraper) and put it in the "final_project_part_1_web_scrape" folder.

(From Step 3 To Step 14 : Run the command lines in Terminal)

3. Download virtual env: pip3 install virtualenv
4. cd to final_project_part_1_web_scrape folder: cd final_project_part_1_web_scrape
5. Create a virtual environment called env: virtualenv env
6. cd to env folder: cd env
7. Activate the virtual environment: source bin/activate
8. cd back to final_project_part_1_web_scrape folder: cd ..
9. Install Django framework: pip install django
10. Install requests library: pip install requests
11. cd to scraper folder: cd scraper
12. Start the server: python manage.py runserver
13. Make the database migration: python manage.py makemigrations
14. Run the database migration: python manage.py migrate
15. Go to the scraper website at: http://127.0.0.1:8000
16. Now it can run on your computer


If you have any other questions, please let me know. 

Thank you very much, 
Group 1
