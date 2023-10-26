# Doubtable

**TEMP README PLEASE REPLACE WITH A BETTER DESCRIPTION LATER**

## Run

How to Clone the Repo:
```bash
git clone https://github.com/Fakesum/doubtable.git
```
This will create a folder called doubtable with the code inside.

<br>

First to Install the requirements run(This only has to be done once.):
```bash
pip install -r requirements.txt
```

Then to run this to start the website at localhost:5000

```bash
python doubtable
```

then go to your browser of choice(example: chrome) and go to the site: (http://localhost:5000)[http://localhost:5000]
this is the link to any localy hosted website.

## TODO

* Styling
    - [x] Make a Basic Header
    - [ ] Make a Logo
    - [ ] Write a explination on the main body as to what the website is about and what it does
    - [ ] Make it look better by adding more styling
        - [ ] Add Borders on everything 
        - [ ] some css tricks to make it look like certain divs are floting.
    - [ ] Add a Blured Background Image for the Page
* Functionality
    - [ ] Add Sources to scrape answers from:
        - [ ] Toppr.answers
        - [ ] Brainly.in
    - [ ] Optimize Selenium Base For this task
        - [ ] Use a pool of ephimereal proxies in case ip ban.
        - [ ] Create a genereal scraper which can scrape from a variety of sites using the same code(This can be done by simply putting the entire page as text then making it so that the text is read through the find the portion which is considered the answer automatically.)