## 1. About the project:
- This project is a big exercise for a Python course at my school.
- It is a web application that is built on the Flask framework. The app is a platform for students to create section classes and in each section class, students can create vocabularies for themselves and can practice through using flashcards or playing games.

Demo:

https://github.com/taiphanvan2k3/QuizMaker/assets/108993284/b1ce6610-f825-4d73-a2af-417f797d91b5



## 2. Prerequisite:
- Python 3.10 or higher
- Flask
- With Firebase: This project uses Firestore to store data. You need to create a project on Firebase and get the credentials to connect to the database. I have an image that shows how to get the credentials. You can see it in the folder `static/images/setup_project/how_to_get_private_key.png` 

## 3. Folder structure:
```
- app
    | - blueprints: contains all blueprints of the app
    |    | - auth: login, register,...
    |    | - home: home page
    |    | - section_class: CRUD of section_class
    |    | ....
    |    | - utils: contains all utilities of the app relevant to Firebase, helpers
    | - layouts: contains all layouts which are used by templates
    |    | _layout.html
    |    | ...
    | - static
    |    | - CSS: contains all CSS files of every page
    |    | - js: contains all javascript files of every page
    |    | - images
    |    | - favicon
    |    | - libraries: jQuery, bootstrap, etc.
```

## 4. How to run the app
1. Clone the project
2. Install all dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`
