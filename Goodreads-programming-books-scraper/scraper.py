import requests
import bs4
import pandas as pd
import time
import re

def scrape_programming_books():
    """
    Extract programming books with high ratings from Goodreads
    Search across multiple popular programming lists
    """
    
    # URLs of programming book lists on Goodreads
    urls = [
        "https://www.goodreads.com/list/show/94619.Best_Popular_Computer_Science_Books_on_Goodreads",
        "https://www.goodreads.com/list/show/79035.Information_Security_Penetration_Testing_Social_Engineering_Counter_Intelligence_Hacker_Hacking_Culture_and_History_",
        "https://www.goodreads.com/list/show/32685.Best_Python_programming_books"
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    all_books = []
    processed_titles = set()  # Avoid duplicates
    
    for url_idx, url in enumerate(urls):
        print(f"Processing list {url_idx + 1}/3: {url.split('/')[-1].replace('_', ' ').title()}")
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"  HTTP Error {response.status_code}")
                continue
                
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            
            # Find books with different selectors depending on the page
            book_items = soup.find_all('tr', itemtype="http://schema.org/Book")
            if not book_items:
                book_items = soup.find_all('div', class_='bookBox')
            
            books_found = 0
            
            for book in book_items:
                try:
                    # Extract title
                    title_elem = book.find('a', class_='bookTitle')
                    if not title_elem:
                        continue
                        
                    title = title_elem.get_text(strip=True)
                    title = re.sub(r'\s+', ' ', title)  # Clean extra spaces
                    
                    # Avoid duplicates
                    if title in processed_titles or len(title) < 5:
                        continue
                    
                    # Extract author
                    author_elem = book.find('a', class_='authorName')
                    
                    author = author_elem.get_text(strip=True) if author_elem else "Unknown author"
                    
                    # Extract rating
                    rating_elem = book.find('span', class_='minirating')
      
                    rating = 0.0
                    if rating_elem: 
                        rating_text = rating_elem.get_text()
                        rating_match = re.search(r'(\d+\.\d+)', rating_text)
                        if rating_match:
                            rating = float(rating_match.group(1))
                    
                    # Filter only books with good rating
                    if rating >= 4.0:
                        # Extract description if available
                        desc_elem = book.find('span', class_='readable')
                        description = desc_elem.get_text(strip=True)[:200] + "..." if desc_elem else "No description"
                        
                        # Book URL
                        book_url = title_elem.get('href', '')
                        if book_url and not book_url.startswith('http'):
                            book_url = f"https://www.goodreads.com{book_url}"
                        
                        all_books.append({
                            'title': title,
                            'author': author,
                            'rating': rating,
                            'description': description,
                            'url': book_url,
                            'category': 'Programming'
                        })
                        
                        processed_titles.add(title)
                        books_found += 1
                        
                        # Limit per list to avoid spam
                        if books_found >= 15:
                            break
                            
                except Exception as e:
                    continue
            
            print(f"  Books found: {books_found}")
            time.sleep(2)  # Pause between lists
            
        except Exception as e:
            print(f"  Error processing list: {e}")
            continue
    
    return all_books

def save_to_excel(books_data):
    """Save data to Excel with professional formatting"""
    if not books_data:
        print("No data to save")
        return
    
    df = pd.DataFrame(books_data)
    
    # Sort by rating descending
    df = df.sort_values('rating', ascending=False)
    df = df.reset_index(drop=True)
    
    # Save to Excel
    filename = 'programming_books_goodreads.xlsx'
    df.to_excel(filename, index=False, sheet_name='Programming Books')
    
    print(f"\n📊 SUMMARY:")
    print(f"Total books saved: {len(df)}")
    print(f"Average rating: {df['rating'].mean():.2f}")
    print(f"File saved: {filename}")
    
    return df

def show_top_books(df, top_n=10):
    """Show the best books in console"""
    print(f"\n🏆 TOP {top_n} PROGRAMMING BOOKS:")
    print("=" * 80)
    
    for i, row in df.head(top_n).iterrows():
        print(f"{i+1:2d}. {row['title']}")
        print(f"    👤 Author: {row['author']}")
        print(f"    ⭐ Rating: {row['rating']}/5.0")
        print(f"    📝 {row['description'][:100]}...")
        print(f"    🔗 {row['url']}")
        print("-" * 80)

if __name__ == "__main__":
    print("🚀 PROGRAMMING BOOKS SCRAPER - GOODREADS")
    print("=" * 60)
    
    # Main scraping
    print("📚 Extracting books from essential lists...")
    books_data = scrape_programming_books()
    
    if books_data:
        # Save to Excel
        df = save_to_excel(books_data)
        
        # Show top books
        show_top_books(df)
                
    else:
        print(" Could not extract books. Possible causes:")
        print("1. Changes in Goodreads HTML structure")
        print("2. Access limitations")
        print("3. Connection issues")
    
    print(f"\n✅ Process completed.")
