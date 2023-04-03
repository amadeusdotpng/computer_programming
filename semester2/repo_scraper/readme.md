# repo_scraper

This uses Github's API to scrape the most popular repos and get files according to language.
It's pretty barebones and requires some manual work.

## Dependencies
repo_scraper is primarily powered by `nodejs` and a little `python` and `bash`.
repo_scraper uses Github's Octokit for their API and `dotenv` for hiding tokens.
```
npm install dotenv
npm install octokit
```
Please make sure that your command line can also run the command `base64`. If not, you must use a third
party tool to decode the downloaded files.

## How To Use
First and foremost, make sure that you have a Github Token so that you're making authenticated requests.
You can find how to make a Personal Access Token 
[here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-personal-access-token-classic).
After you have your Github Token, you can store it in a `.env` file as `TOKEN=<your-token-here>`.  


You can now edit `index.mjs` to scrape repos by language.
Change the `language` variable to whichever language you wish, such as `java` or `cpp`.  

You can change the range of repos scraped by changing the variables `from` and `to`.
```javascript
// This will scrape the 20th to 30th most popular repos in github
// according to language.
let from = 19;
let to = 29;
```

__Please make sure that you have this directory structure created before running `node index.mjs`__
```
<language>
├── decoded
├── files
└── processed
```

Then run the following commands
```
# scrapes repos
node index.mjs

cp preprocess.py <language>/files
cp decode.sh <language>/processed

# preprocess the scraped files by getting rid of newlines and other whitespaces
cd <language>/files
python preprocess.py

# decodes processed files from base64
cd ../processed
./decode.sh

cd ../decoded
```

After running the commands, the current directory will have all of the scraped files.
