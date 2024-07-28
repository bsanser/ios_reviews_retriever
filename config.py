# APPS_LIST_ = {
  # 'ELVIE' : '1349263624',
  # 'WILLOW_GO' : '1579004074',
  # 'WILLOW_3' : '1489872855',
  # 'TOMMEE_TIPPEE' : '1522124003',
  # 'MEDELA' : '909275386',
  # 'LANSINOH_2.0' : '1480550011',
  # 'LANSINOH_3.0' : '1670282806',
  # 'MOMCOZY': '6473000053'
# }


# 1)  Enter your app name and id below. Follow the same format as shown in the example above. 
# To find out the id of the app you're interested in, check in the url of their app store listing page: 
# For example, for the app Slack, this is the url https://apps.apple.com/us/app/slack/id618783545. The id will be 618783545
# The name included here will be included in the name of the spreadsheet that gets generated (but lowercase)

APPS_LIST = {
  'MOMCOZY': '6473000053'
}

# 2) You can add or remove the countries where the script will look for app reviews by editing the list below

COUNTRY_CODES = ["DZ", "AO", "AI",
"AR", "AM", "AU", "AT", "AZ", "BH", "BB", "BY", "BE", "BZ", "BM", "BO","BW", "BR", "VG", "BN", "BG", "CA","KY", "CL", "CN", "CO", "CR", "HR", "CY", "CZ", "DK", "DM", "EC", "EG",
"SV", "EE", "FI","FR", "DE", "GH","GB", "GR", "GD","GT", "GY", "HN","HK", "HU", "IS","IN", "ID", "IE","IL", "IT", "JM", "JP", "JO", "KE", "KW", "LV", "LB","LT", "LU", "MO", "MG", "MY", 
"ML","MT", "MU", "MX","MS", "NP", "NL", "NZ", "NI", "NE","NG", "NO", "OM","PK", "PA", "PY","PE", "PH", "PL","PT", "QA", "MK", "RO", "RU", "SA","SN", "SG", "SK","SI", "ZA", "KR", "ES", 
"LK", "SR","SE", "CH", "TW","TZ", "TH", "TN","TR", "UG", "UA","AE", "US", "UY","UZ", "VE", "VN","YE"]