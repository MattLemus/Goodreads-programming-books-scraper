# 📚 Goodreads Programming Books Scraper

A Python script that extracts highly rated programming books from Goodreads lists, saves the results in an Excel file, and displays the top books in the console.

---

## 🚀 Features

- Scrapes multiple Goodreads lists of programming and computer science books.
- Extracts book title, author, rating, description, and URL.
- Filters only books with a rating of 4.0 or higher.
- Saves results in a professional Excel file.
- Displays the Top N programming books in the console.

---

## 🛠 Requirements

Install the dependencies with:

```bash
pip install -r requirements.txt
```
---

## Usage
```bash
python scraper.py
```
---

**Output:**  
- Excel file: `programming_books_goodreads.xlsx`  
- Console summary with top books

---

## 📊 Example Output
```
🏆 TOP 5 PROGRAMMING BOOKS:
================================================================================
 1. Clean Code: A Handbook of Agile Software Craftsmanship
     👤 Author: Robert C. Martin
     ⭐ Rating: 4.40/5.0
     📝 Even bad code can function. But if code isn’t clean, it can bring a development organization...
     🔗 https://www.goodreads.com/book/show/3735293-clean-code
--------------------------------------------------------------------------------
```
