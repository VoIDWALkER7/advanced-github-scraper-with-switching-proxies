# advanced-github-scraper-with-switching-proxies
Advanced github scraper with switching proxies that will help ya find a keyword by searching the target's repos, folders, files.

### it works! 

# explanation

this is a github-scraper made with the help of python, and selenium library present in it. 
this scrapes a repository that you enter, and looks through each folder and file, to search for the file that has the keyword that you are searching for. the output looks something just like this: 


![image](https://github.com/VoIDWALkER7/github-scraper/assets/84080270/406a90e7-3cf4-4c9a-aa97-cf898e4ff89b)


for proxies, you can visit the website: ```https://free-proxy-list.net``` and add the proxies in the list as follows: 

```Python
[
"http://proxy1:port1", 
"http://proxy2:port1",
#and so on
]
```

The proxies will be switched when accessing a new repo or a new file using the function switch_proxy()
