#!/usr/bin/env python
# coding: utf-8

# # Helping Marketers Understand Their Users
# 
# This project will analyze free Android and iOS mobile apps to help  developers within our company better understand their target audience. The company we are at develops Android and iOS apps free Android and iOS apps that gain revenue from adds. We are gathering data driven data to determine what type of apps are likely to attact the most users in order to determie what products to develop. 
# 
# # Opening and Exploring the App Data
# 
# As of late 2018, there were over 4 million apps combined in the App Store and Google Play. To reduce the amount of resources used in gathering this data, we used a sample from the App Store and Google Play. They can be found here:
# 
# https://www.kaggle.com/lava18/google-play-store-apps/home
# https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps/home
# 
# We'll start by opening and exploring both data sets.

# In[1]:


from csv import reader

# The Google Play data set #
opened_file = open('/Users/Keeri/Documents/googleplaystore.csv')
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]

# The App Store data set #
opened_file = open('//Users/Keeri/Documents/AppleStore.csv')
read_file = reader(opened_file)
ios = list(read_file)
ios_header = ios[0]
ios = ios[1:]


# First we'll explore a small part of the data sets.

# In[2]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') 
        
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

print(android_header)
print('\n')
explore_data(android, 0, 3, True)


# The Google Play data set has 10841 apps and 13 columns. 'App', 'Category', 'Reviews', 'Installs', 'Type', 'Price', and 'Genres' are all columns that may be purposeful for us to analyze at a later time.
# 
# Now let's take a look at the App Store data set.

# In[3]:


print(ios_header)
print('\n')
explore_data(ios, 0, 3, True)


# There are 7197 iOS apps in this data set, and the columns that could be useful are: 'track_name', 'currency', 'price', 'rating_count_tot', 'rating_count_ver', and 'prime_genre'. Not all column names are self-explanatory in this case, but details about each column can be found in the data set documentation provided in the link at the beginning of this documentation.
# 
# # Deleting Wrong Data
# 
# A dedicated Google Play discussion section outlined an error for row 10472. Let's print this row and compare it against the header and another row that is correct.

# In[4]:


print(android[10472])  # incorrect row
print('\n')
print(android_header)  # header
print('\n')
print(android[0])      # correct row


# The row 10472 corresponds to the app Life Made WI-Fi Touchscreen Photo Frame. It shows a rating of '19', when the highest rating value is '5'.  We will delete this since it is an error. 

# In[5]:


print(len(android))
del android[10472]  
print(len(android))


# # Removing Duplicate Entries
# 
# Some apps have more than one entry in the Google Play data set. For instance, the application Instagram has four entries:

# In[6]:


for app in android:
    name = app[0]
    if name == 'Instagram':
        print(app)


# In total, there are 1,181 cases where an app occurs more than once:

# In[7]:


duplicate_apps = []
unique_apps = []

for app in android:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)
    
print('Number of duplicate apps:', len(duplicate_apps))
print('\n')
print('Examples of duplicate apps:', duplicate_apps[:15])


# We don't want to have multiple entries for one app, so we need to delete the duplicates. We could delete a duplicate randomly, or we could choose which duplicate to delete. Since we are using this data for analytics, it is best to choose the duplicate to delete in order to have the most precise data.
# 
# To do this, we are going to keep the duplicate with the highest number of reviews. This will likely give us the most reliable data on the app. 
# 
# In order to do this, we will create a dictionary where each key is a unique app name, and the value is the highest number of reviews of that app. Then use the dictionary to create a new data set, which will have only one entry per app (and we only select the apps with the highest number of reviews)

# In[8]:


reviews_max = {}

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
        
    elif name not in reviews_max:
        reviews_max[name] = n_reviews


# Previously we found there are 1,181 cases where an app occurs more than once, so the length of our dictionary (of unique apps) should be equal to the difference between the length of our data set and 1,181.

# In[9]:


print('Expected length:', len(android) - 1181)
print('Actual length:', len(reviews_max))


# Next we'll use the 'reviews_max' dictionary to remove the duplicates. We will keep the highest number of reviews.
# 
# We start by initializing two empty lists, 'android_clean' and 'already_added'. Looping through 'android', if the app's number of reviews is equal to it's 'reviews_max' number and it's name is not in the 'already_added' list, it will be appended to the 'android_clean' list. This is the list where our non-duplicates with the highest review rates are. It will also be added to the 'already_added' list to ensure it does not become a duplicate to our clean list. 

# In[10]:


android_clean = []
already_added = []

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name) 


# We'll explore the new data set and confirm that the number of rows is 9,659.

# In[11]:


explore_data(android_clean, 0, 3, True)


# We have 9659 rows, just as expected.

# # Removing Non-English Apps
# 
# People everywhere use apps and of all different languages. However, the company we're at wants to produce English apps. So we need to narrow our data down to English only apps in order to get the best information.

# In[12]:


print(ios[813][1])
print(ios[6731][1])

print(android_clean[4412][0])
print(android_clean[7940][0])


# The way we will go about removing non-English apps is by using the ASCII standard. Each character has a numeric value assigned to it. English characters have numberic characters between 0 and 127 assigned to them. These include letters, numbers, punctuation marks, and common arithmatic symbols. 
# 
# Below we will create a function that can help determine whether an app in English or non-English based on it's name.

# In[13]:


def is_english(string):
    
    for character in string:
        if ord(character) > 127:
            return False
    
    return True

print(is_english('Instagram'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))


# This system will work, but many apps use special characters or emojis. So having a limit that strict would block a large amount of English apps from our data. 

# In[14]:


print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))

print(ord('™'))
print(ord('😜'))


# To minimize the impact of data loss, we'll only remove an app if its name has more than three non-ASCII characters to account for emojis or other special characters.

# In[15]:


def is_english(string):
    non_ascii = 0
    
    for character in string:
        if ord(character) > 127:
            non_ascii += 1
    
    if non_ascii > 3:
        return False
    else:
        return True

print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))


# This function is not perfect, but it will do well for the purposes of our data gathering.
# 
# Below, we use the is_english() function to filter out the non-English apps for both data sets:

# In[16]:


android_english = []
ios_english = []

for app in android_clean:
    name = app[0]
    if is_english(name):
        android_english.append(app)
        
for app in ios:
    name = app[1]
    if is_english(name):
        ios_english.append(app)
        
explore_data(android_english, 0, 3, True)
print('\n')
explore_data(ios_english, 0, 3, True)


# We can see that we're left with 9614 Android apps and 6183 iOS apps.
# 
# # Isolating the Free Apps
# 
# As we mentioned in the introduction, we only build apps that are free to download and install, and our main source of revenue consists of in-app ads. Our data sets contain both free and non-free apps, and we'll need to isolate only the free apps for our analysis. Below, we isolate the free apps for both our data sets.

# In[17]:


android_final = []
ios_final = []

for app in android_english:
    price = app[7]
    if price == '0':
        android_final.append(app)
        
for app in ios_english:
    price = app[4]
    if price == '0':
        ios_final.append(app)
        
print(len(android_final))
print(len(ios_final))


# We're left with 8864 Android apps and 3222 iOS apps that are free to play. 
# 
# # Most Common Apps by Genre
# 
# As mentioned previously, our aim is to determine the kinds of apps that are likely to attract more users because our revenue is highly influenced by the number of people using our apps.
# 
# To minimize risks and overhead, our validation strategy for an app idea is comprised of three steps:
# 
# Build a minimal Android version of the app, and add it to Google Play.
# If the app has a good response from users, we then develop it further.
# If the app is profitable after six months, we also build an iOS version of the app and add it to the App Store.
# Because our end goal is to add the app on both the App Store and Google Play, we need to find app profiles that are successful on both markets. For instance, a profile that might work well for both markets might be a productivity app that makes use of gamification.
# 
# We'll begin by initilizing frequency tables to analyze the most common apps by genre. One function will show percentages will display the percentages in a descending order

# In[18]:


def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
    
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage 
    
    return table_percentages


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# We start by examining the frequency table for the prime_genre column of the App Store data set.

# In[19]:


display_table(ios_final, -5)


# Among the free English apps, more than a half (58.16%) are games. The remainder of the apps come nowhere near the rest of the makeup in frequency. Entertainment apps are slighly below 8%, and photo and video apps are around 5%. Education apps madu up approximately 3.6% of the frequencies, with social networking coming in at 3.2%. 
# 
# From what we can see, the App Store is saturated with "fun." Games, entertainment, photo and vidoe- at least in the free English speaking part of it. Apps with a practical purpose, such as shopping, education, lifeslyle, and productivity apps are more rare. Although there are more fun apps available, doesn't necessarily mean they have the greatest number of users or there isn't a demand for the app categories with fewer frequencies.
# 
# We'll continue by examining the Genres and Category columns of the Google Play data set.

# In[20]:


display_table(android_final, 1) 


# Google Play seems to be significantly different than the App Store based on the tables we created. It tends to have more practical apps rather than such an emphasis on games. The family category does have a lot of children's games, but there is still a large emphasis on practicality. 
# 
# The genres table also confirms this. 

# In[21]:


display_table(android_final, -4)


# The difference between the Genres and the Category columns is not explicit, but it does have a lot mroe categories. Since we are only looking at the big picture for now, we will work with only the Category column at the moment. 
# 
# Up to this point, we found that the App Store is dominated by apps designed for fun, while Google Play shows a more balanced landscape of both practical and for-fun apps. Now we'd like to get an idea about the kind of apps that have most users.
# 
# # Most Popular Apps by Genre on the App Store
# 
# The most common way to find out the most populat genres is to calculate the average number of installs for each apps. For Google Play, this information is available and we can calculate it. 
# 
# Unfortunately, this information is not available for the App Store. One way to get around this lack of data is by using the total number of ratings as a workaround. We'll do so below:
# 

# In[22]:


genres_ios = freq_table(ios_final, -5)

for genre in genres_ios:
    total = 0
    len_genre = 0
    for app in ios_final:
        genre_app = app[-5]
        if genre_app == genre:            
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre
    print(genre, ':', avg_n_ratings)


# Navigation apps have the highest number of user reviews. This figure is heavily influenced by Waze and Google Maps, which have close to half a million user reviews together.

# In[23]:


for app in ios_final:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5]) # print name and number of ratings


# However, this niche seems to show some potential. One thing we could do is take another popular book and turn it into an app where we could add different features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes about the book, etc. On top of that, we could also embed a dictionary within the app, so users don't need to exit our app to look up words in an external app.
# 
# This idea seems to fit well with the fact that the App Store is dominated by for-fun apps. This suggests the market might be a bit saturated with for-fun apps, which means a practical app might have more of a chance to stand out among the huge number of apps on the App Store.
# 
# Other genres that seem popular include weather, book, food and drink, or finance. The book genre seem to overlap a bit with the app idea we described above, but the other genres don't seem too interesting to us:
# 
# Weather apps — people generally don't spend too much time in-app, and the chances of making profit from in-app adds are low. Also, getting reliable live weather data may require us to connect our apps to non-free APIs.
# 
# Food and drink — examples here include Starbucks, Dunkin' Donuts, McDonald's, etc. So making a popular food and drink app requires actual cooking and a delivery service, which is outside the scope of our company.
# 
# Finance apps — these apps involve banking, paying bills, money transfer, etc. Building a finance app requires domain knowledge, and we don't want to hire a finance expert just to build an app.
# 
# Now we'll analyze the Google Play market.
# 
# # Most Popular Apps by Genre on Google Play
# 
# For the Google Play market we do have data for the number of installs, so we should be able to get a clearer picture about genre popularity. The install numbers are not very precise however.

# In[24]:


display_table(android_final, 5) # the Installs columns


# With the current data, we don't know whether 100,000+ means an app has 100,000 installs, 200,000 installs, or 300,000 installs. Thankfully, for our purposes we do not need exact data. 
# 
# For our purposes we're going to leave the numbers as they are, which means that we'll consider that an app with 100,000+ installs to have 100,000 installs and an app with 1,000,000+ installs  to have 1,00,000 installs and so on.
# 
# To perform computations we'll need to convert each install number to a float by removing the comas and plus characters. We'll do this in the loop below as well as calculate the average number of installs for each genre.

# In[25]:


categories_android = freq_table(android_final, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in android_final:
        category_app = app[1]
        if category_app == category:            
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


# On average, communication apps have the most installs: 38,456,119. A few communication apps have heavily skewed this with one billion installs: WhatsApp, Facebook Messenger, Skype, Google Chrome, Gmail, and Hangouts.  A few others had over 100 and 500 million installs, as seen below.

# In[26]:


for app in android_final:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                      or app[5] == '500,000,000+'
                                      or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# If we removed the 27 apps that make up these large amount of downloads, the average number of installs would be reduced by approximately ten times.

# In[27]:


under_100_m = []

for app in android_final:
    n_installs = app[5]
    n_installs = n_installs.replace(',', '')
    n_installs = n_installs.replace('+', '')
    if (app[1] == 'COMMUNICATION') and (float(n_installs) < 100000000):
        under_100_m.append(float(n_installs))
        
sum(under_100_m) / len(under_100_m)


# The same pattern is present in the video players category. There are 34, 727,872 installs, yet the market is largely dominated by a select number of apps such as Google Play Movies, Youtube, and MX Player. A similar pattern is seen in the social apps category dominated by Facebook, Instagram, and Google+. Photography app high downloads are Google Photos and a few other other popular photo editors. Another category is productivity apps, where Microsoft Word, Dropbox, Google Calendar, and Evernote are high downloads.
# 
# The main concerns are these app categories may seem more popular than they actually are, and these highly downloaded apps may be very difficult to compete with.
# 
# The game genre seems popular, but based on the data we gathered earlier, the market seems a bit saturated. It would likely be best to put our resources into another category.
# 
# The books and reference genre appears popular. It has an average install of 8,767,811. It's interesting to explore this in more depth, since we found this genre has some potential to work well on the App Store, and our aim is to recommend an app genre that shows potential for being profitable on both the App Store and Google Play.
# 
# We'll look at some of the apps and their installs.

# In[28]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5])


# The book and reference genre includes many different apps: software for processing and reading ebooks, various collections of books/libraries, dictionaries, tutorials, etc. As we saw in previous categories, there are some apps that have a high number of download frequencies that skew our results:

# In[29]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000,000+'
                                            or app[5] == '500,000,000+'
                                            or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# Compared to the other app markets we researched, this is a relatively low number of apps that have 100,000,000+ downloads. This means there is still potential for our team to create a great app for this market.  
# 

# In[30]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000+'
                                            or app[5] == '5,000,000+'
                                            or app[5] == '10,000,000+'
                                            or app[5] == '50,000,000+'):
        print(app[0], ':', app[5])


# The Books and References Market is dominated by software for processing and reading ebooks. There are also large collections of libraries and dictionaries in both stores, meaning none of these would be a good app to build as there is already significant competition.
# 
# One notable feature in the market are a number of apps about the Quran. This suggests it can be profitable to build an app around a book for both Google Play and the App Store. There are already a significan amount of apps for the Quran, but we could look into creating an app for a newer popular book.
# 
# Since there are so many places to already get books, we could need to add features to our app no one else has besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.
# 
# # Conclusion
# 
# In this project, we analyzed data about the App Store and Google Play mobile apps with the goal of recommending an app profile that can be profitable for both markets.
# 
# We concluded that taking a popular book and turning it into an app could be profitable for both the Google Play and the App Store markets. The markets are already full of libraries, so we need to add some special features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.
