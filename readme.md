
# 📅 Google Calendar -> Toggl synchronizer ⏰
This cli app synchronizing events from google calendar to the toggl. OAuth2 Local Authentication is used to provide access to the account's primary calendar  


**NOTICE**: You will have a google authorization warning with default binary because app is not verified. You can ignore that or rebuild it with your credentials. 


**[Download the executable binary for mac]()**
## How to use

```
#If it is not in $PATH
./gcal-toggl -t "toggl_api_token" -d "2019-11-01" -w "123456"

#If it is in $PATH
gcal-toggl -t "toggl_api_token" -d "2019-11-01" -w "123456"
```

### Parameters:
* `-t` = toggl token value. Must be provided at least once. Once provided - it will be cached on your system for further use in your local directory
* `-d` = date to sync. Optional parameter. If not provided, set to today's date.
* `-w` = toggle workspace id. Must be provided, unless you have the same workspace id as me 🙂




## Building from source (Manually)
* Install dependencies from requirements.txt
* Add google credentials file to data folder as `credentials.json`. [More on creating google apps](https://developers.google.com/identity/protocols/OAuth2)
* Run command below to package binary. You binary will be available in `dist` folder

```
pyinstaller --onefile --add-data='data/*:data' -n gcal-toggl src/main.py
```


## Todo
- [ ] Add project inference by name
- [ ] Add manual project specification (e.g. #MyProject meeting)
- [ ] Add skip-event tag (e.g. #skip)
- [ ] Add giphy to readme


