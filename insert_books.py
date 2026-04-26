import sqlite3

# Data in CSV format
csv_data = """Title, Author, Price
The Handmaid's Tale, Margaret Atwood, 13.50
The Hitchhiker's Guide to the Galaxy, Douglas Adams, 10.00
The Joy of Cooking, Irma S. Rombauer, 35.00
To the Lighthouse, Virginia Woolf, 11.00
Mrs. Dalloway, Virginia Woolf, 10.50
The Bell Jar, Sylvia Plath, 12.00
Catch-22, Joseph Heller, 14.50
Slaughterhouse-Five, Kurt Vonnegut, 11.50
The Crying of Lot 49, Thomas Pynchon, 13.00
Invisible Man, Ralph Ellison, 15.00
The Color Purple, Alice Walker, 12.50
Midnight's Children, Salman Rushdie, 16.00
The God of Small Things, Arundhati Roy, 11.00
The Remains of the Day, Kazuo Ishiguro, 10.50
Bel Canto, Ann Patchett, 12.00
The Corrections, Jonathan Franzen, 15.00
The Amazing Adventures of Kavalier & Clay, Michael Chabon, 14.00
The Road, Cormac McCarthy, 11.50
The Help, Kathryn Stockett, 13.00
Gone Girl, Gillian Flynn, 12.50
The Girl with the Dragon Tattoo, Stieg Larsson, 14.00
The Hunger Games, Suzanne Collins, 10.00
The Fault in Our Stars, John Green, 11.00
The Book Thief, Markus Zusak, 12.00
The Secret History, Donna Tartt, 14.50
A Little Life, Hanya Yanagihara, 16.00
Educated, Tara Westover, 13.50
Sapiens: A Brief History of Humankind, Yuval Noah Harari, 18.00
Becoming, Michelle Obama, 15.00
Where the Crawdads Sing, Delia Owens, 12.50
The Lord of the Flies, William Golding, 11.00
The Old Man and the Sea, Ernest Hemingway, 10.00
Of Mice and Men, John Steinbeck, 9.50
The Sun Also Rises, Ernest Hemingway, 12.00
A Farewell to Arms, Ernest Hemingway, 13.00
For Whom the Bell Tolls, Ernest Hemingway, 14.00
The Metamorphosis, Franz Kafka, 10.00
Steppenwolf, Hermann Hesse, 11.50
Siddhartha, Hermann Hesse, 10.00
Demian, Hermann Hesse, 9.50
The Trial, Franz Kafka, 11.50
The Castle, Franz Kafka, 12.00
The Stranger, Albert Camus, 10.50
The Plague, Albert Camus, 11.00
The Fall, Albert Camus, 9.00
No Exit, Jean-Paul Sartre, 8.50
The Myth of Sisyphus, Albert Camus, 10.00
Waiting for Godot, Samuel Beckett, 9.50
Rosencrantz and Guildenstern Are Dead, Tom Stoppard, 10.50
Long Day's Journey into Night, Eugene O'Neill, 11.00
Death of a Salesman, Arthur Miller, 9.50
A Streetcar Named Desire, Tennessee Williams, 10.00
Who's Afraid of Virginia Woolf?, Edward Albee, 10.50
The Glass Menagerie, Tennessee Williams, 9.00
Fences, August Wilson, 11.00
Angels in America, Tony Kushner, 15.00
Medea, Euripides, 8.00
Antigone, Sophocles, 8.50
Oedipus Rex, Sophocles, 9.00
The Oresteia, Aeschylus, 12.00
The Odyssey, Homer, 15.00
The Iliad, Homer, 14.50
The Aeneid, Virgil, 13.00
Beowulf, Unknown Author, 10.00
The Epic of Gilgamesh, Unknown Author, 9.50
The Tale of Genji, Murasaki Shikibu, 25.00
Journey to the West, Wu Cheng'en, 20.00
Dream of the Red Chamber, Cao Xueqin, 22.00
The Pillow Book, Sei Shōnagon, 11.00
Essays, Michel de Montaigne, 18.00
Leviathan, Thomas Hobbes, 15.00
The Prince, Niccolò Machiavelli, 10.00
Discourse on Method, René Descartes, 12.00
The Social Contract, Jean-Jacques Rousseau, 14.00
On Liberty, John Stuart Mill, 11.00
Thus Spoke Zarathustra, Friedrich Nietzsche, 16.00
Beyond Good and Evil, Friedrich Nietzsche, 14.00
The Interpretation of Dreams, Sigmund Freud, 20.00
Civilization and Its Discontents, Sigmund Freud, 12.00
The Republic, Plato, 15.50
The Symposium, Plato, 10.00
The Apology, Plato, 8.50
Politics, Aristotle, 17.00
Nicomachean Ethics, Aristotle, 15.00
Meditations, Marcus Aurelius, 11.00
The Art of War, Sun Tzu, 9.00
The Bhagavad Gita, Unknown Author, 10.50
The Tao Te Ching, Lao Tzu, 9.50
The Quran, Various Authors, 15.00
The Bible, Various Authors, 20.00
The Upanishads, Various Authors, 14.00
The Dhammapada, Various Authors, 11.00
The Analects, Confucius, 10.00
Leaves of Grass, Walt Whitman, 13.00
Moby-Dick, Herman Melville, 19.00
Walden, Henry David Thoreau, 11.50
The Scarlet Letter, Nathaniel Hawthorne, 13.50
Uncle Tom's Cabin, Harriet Beecher Stowe, 14.00
Little Women, Louisa May Alcott, 12.00
The Adventures of Tom Sawyer, Mark Twain, 10.50
The Call of the Wild, Jack London, 10.50
The Great Gatsby, F. Scott Fitzgerald, 14.00
Tender is the Night, F. Scott Fitzgerald, 13.00
The Catcher in the Rye, J.D. Salinger, 11.50
To Kill a Mockingbird, Harper Lee, 12.50
Invisible Man, Ralph Ellison, 15.00
Beloved, Toni Morrison, 14.00
One Hundred Years of Solitude, Gabriel García Márquez, 18.00
Love in the Time of Cholera, Gabriel García Márquez, 15.00
Things Fall Apart, Chinua Achebe, 12.50
A Thousand Splendid Suns, Khaled Hosseini, 13.00
The Kite Runner, Khaled Hosseini, 12.50
The God of Small Things, Arundhati Roy, 11.00
Midnight's Children, Salman Rushdie, 16.00"""

# Connect to SQLite database (or create if it doesn't exist)
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

# Create a table named 'books' if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        title TEXT,
        author TEXT,
        price REAL
    )
''')

# Split the CSV data into lines and then into individual fields
lines = csv_data.strip().split('\n')
header = lines[0].split(', ')
book_data = [line.split(', ') for line in lines[1:]]

# Insert the book data into the 'books' table
cursor.executemany('INSERT INTO books (title, author, price) VALUES (?, ?, ?)', book_data)

# Commit the changes
conn.commit()

# Close the connection
conn.close()

print("Data inserted successfully into the 'books' table in 'books.db'")