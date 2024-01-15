import * as dotenv from 'dotenv' // see https://github.com/motdotla/dotenv#how-do-i-use-dotenv-with-import
dotenv.config()
import { Octokit } from 'octokit';
import fs from 'fs';

const octokit = new Octokit({ 
  auth: process.env.TOKEN,
});

let language = "rust";
console.log(`scraping by ${language}\n`);
let fetched = await octokit.request("GET /search/repositories?q=language:{lang}&sort=stars&order=desc", {lang: language});
let repoList = fetched.data.items;
console.log("fetched...");

let from = 0
let to = 30
for(let i = from; i < to; i++) {
	let fetchedFiles = await octokit.request("https://api.github.com/search/code?q=%20+in%3Afile+language%3A{lang}+repo%3A{repo}", {lang: language, repo: repoList[i].full_name});
	let filesList = fetchedFiles.data.items;
	console.log(`${repoList[i].full_name}:`);

	if(filesList.length != 0) {
		for (let j = 0; j < filesList.length; j++) {
			let fetchedContent = await octokit.request(filesList[j].url, {});
			let content = fetchedContent.data.content;
			let name = fetchedContent.data.name.split('.')[0];
			fs.writeFile(`./${language}/files/${name}-${j}.txt`, content, err => {if(err) {console.log(err)}});
			console.log(`${name} fetched. Ratelimit remaining: ${fetchedContent.headers['x-ratelimit-remaining']}`);
		}
		console.log("\n");
	}

}
