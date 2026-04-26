from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the DB
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')

    # Create cart table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            title TEXT,
            author TEXT,
            price REAL,
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    ''')

    conn.commit()
    conn.close()

#BOOKS_PER_PAGE = 10

@app.route('/')
def index():
    # Get the current page from the query string, default to 1 if not present
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Limit to 10 books per page

    # Connect to the database
    conn = get_db_connection()
    
    # Fetch books for the current page
    books = conn.execute('SELECT * FROM books LIMIT ? OFFSET ?', (per_page, (page - 1) * per_page)).fetchall()
    
    # Get total number of books in the database for pagination
    total_books = conn.execute('SELECT COUNT(*) FROM books').fetchone()[0]
    conn.close()

    # Calculate total number of pages
    total_pages = (total_books // per_page) + (1 if total_books % per_page > 0 else 0)

    # Return the template with the necessary data
    return render_template('index.html', books=books, page=page, total_pages=total_pages)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']
        conn = get_db_connection()
        conn.execute('INSERT INTO books (title, author, price) VALUES (?, ?, ?)',
                     (title, author, price))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add.html')

# Add to cart route
@app.route('/add_to_cart/<int:book_id>')
def add_to_cart(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    if book:
        conn.execute('INSERT INTO cart (book_id, title, author, price) VALUES (?, ?, ?, ?)',
                     (book['id'], book['title'], book['author'], book['price']))
        conn.commit()
    conn.close()
    return redirect('/cart')

# View cart route
@app.route('/cart')
def cart():
    conn = get_db_connection()
    cart_items = conn.execute('SELECT * FROM cart').fetchall()
    conn.close()
    return render_template('cart.html', cart_items=cart_items)

# Remove item from cart route
@app.route('/remove_from_cart/<int:item_id>')
def remove_from_cart(item_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM cart WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect('/cart')

# Buy book route
@app.route('/buy/<int:book_id>')
def buy(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    if book:
        return render_template('payment.html',book=book)
    else:
        return "<h1>Book not found.</h1><a href='/'>← Back</a>"

# Delete book route
@app.route('/delete/<int:book_id>')
def delete(book_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return redirect('/')


@app.route('/payment', methods=['GET', 'POST'])
def payment():
        # In a real application, you would process the payment here
        # For now, we'll just display a confirmation
    return render_template('payemnt_confirmation.html')

@app.route('/checkout')
def checkout():
    return render_template('payment.html')


@app.route('/payment_confirmation')
def payment_confirmation():
    return """
        <h1>Thank you for your payment! Your order is being processed.</h1>
        <a href='/'>Back to Store</a>
    """

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
