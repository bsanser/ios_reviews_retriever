# 📱 iOS Reviews Retriever
A simple python script to get the app store reviews of one or more apps and export them to a spreadsheet

<h2>Steps to run the script</h2>

1. 🧩 Install the dependencies of the project contained in the file `requirements.txt` by running the following code:
```
pip install -r requirements.txt
```


2. 👩🏻‍💻 Add the apps you would like to retrieve app store reviews from to the `APPS_LIST` dictionary in the `constants.py`file
 <ul>
     <li>Follow this pattern for including new apps NAME_OF_THE_APP: 'id_of_the_app' and make sure each app is separated by commas - there is an example at the beginning of the file </li> 
     <li>You can choose to name the app as you want. The name you choose for the app will be included in the name of the spreadsheet that gets generated</li> 
     <li>To find out the id of the app you're interested in, check in the url of the app store listing page: for example, for Slack the URL is https://apps.apple.com/us/app/slack/id618783545, which means that it should be added as follows:</li>
  </ul>

```
'SLACK': '618783545'
```
  
3. 🌎 Customise the countries where you want to look for reviews by adding or removing country codes to the list called `COUNTRY_CODES` in the file `constants.py`
   <ul>
     <li>The API we're using to retrieve the reviews needs to make a request for each individual country (there is not a way to request all countries)</li> 
     <li>The existing list should cover most of the countries if not all where an app will have reviews</li> 
   </ul>

4. 🧚🏻‍♀️ Run the script with the following command:
   ```
    python3 ios_reviews_retriever.py
  ```
