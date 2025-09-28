#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import mysql.connector
from datetime import date
import schedule
import time

# In[58]:


## WITHOUT DUPLICATES

def scrape_laptops():
    url = 'https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    
    laptop = []
    seen_products = set()  # store unique product signature without link
    
    for i in range(1, 100):
        print(f"Scraping Page {i}...")
        response = requests.get(url + f"&page={i}")
        soup = BeautifulSoup(response.text, 'html.parser')
        product = soup.find_all("div", attrs={'class': 'cPHDOP col-12-12'})
    
        for i in product:
            if i.find("a", {"class": "CGtC98"}):
                link = 'https://www.flipkart.com' + i.find("a", {"class": "CGtC98"}).get("href")
    
                name = i.find("div", attrs={'class': 'KzDlHZ'}).text.strip() if i.find("div", attrs={'class': 'KzDlHZ'}) else None
    
                stars = i.find("div", attrs={'class': 'XQDdHH'}).text.strip() if i.find("div", attrs={'class': 'XQDdHH'}) else None
    
                rating = int(i.find("span", attrs={'class': 'Wphh3N'}).text.strip().replace("\xa0", " ").split(" ")[0].replace(",", "")) if i.find("span", attrs={'class': 'Wphh3N'}) else None
    
                review = int(i.find("span", attrs={'class': 'Wphh3N'}).text.strip().replace("\xa0", " ").split(" ")[3].replace(",", "")) if i.find("span", attrs={'class': 'Wphh3N'}) else None
    
                disc_price = int(i.find("div", attrs={'class': 'Nx9bqj _4b5DiR'}).text.strip().replace(",", "").replace("₹", "")) if i.find("div", attrs={'class': 'Nx9bqj _4b5DiR'}) else None
    
                orig_price = int(i.find("div", attrs={'class': 'yRaY8j ZYYwLA'}).text.strip().replace(",", "").replace("₹", "")) if i.find("div", attrs={'class': 'yRaY8j ZYYwLA'}) else None
    
                discount = i.find("div", attrs={'class': 'UkUFwK'}).text.strip().replace(" off", "") if i.find("div", attrs={'class': 'UkUFwK'}) else None
    
                features = ", ".join([li.text.strip() for li in i.find("ul", attrs={"class": "G4BRas"}).find_all("li")]) if i.find("ul", attrs={"class": "G4BRas"}) else None
    
                # ✅ Required fields check
                if name and disc_price:
                    # ✅ Create a unique signature (ignoring link)
                    signature = (name, stars, rating, review, disc_price, orig_price, discount, features, date.today())
    
                    if signature not in seen_products:  # prevent duplicates
                        seen_products.add(signature)
                        laptop.append({
                            "Link": link,
                            "Name": name,
                            "Stars": stars,
                            "Rating": rating,
                            "Review": review,
                            "Discounted_Price": disc_price,
                            "Original_Price": orig_price,
                            "Discount": discount,
                            "Features": features,
                            "date": date.today()
                        })
    if laptop:

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MYSQLwb@1234",
            database="ecommerce_tracker"
        )
        
        cursor = conn.cursor()
        
        for p in laptop:
            cursor.execute("""
                INSERT INTO products  (link, name, stars, number_of_rating, number_of_reviews, disc_price, orig_price, discount, features, scrape_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (p["Link"],p["Name"],p["Stars"],p["Rating"],p["Review"],p["Discounted_Price"],p["Original_Price"],p["Discount"],p["Features"],p["date"]))
        
        conn.commit()
        cursor.close()
        conn.close()
        
    print("Scraping and insertion completed!")

# Schedule the scraper daily at 3:10 PM
schedule.every().day.at("15:10").do(scrape_laptops)

print("Scheduler started. Press Ctrl+C to stop.")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)
