# Book-Author Database with SQLAlchemy

This project implements a relational database using SQLAlchemy ORM to manage authors and books in a many-to-many relationship. The database simulates an author-book catalog, with random data generation using the Faker library.

## Features

- **Many-to-Many Relationship**: Authors can have multiple books, and books can have multiple authors.
- **Random Data Generation**: Uses the Faker library to generate random authors and books.
- **Queries**: Includes functions to retrieve data such as:
  - Books with the most pages.
  - Average number of pages per book.
  - The youngest author.
  - Authors with no books.
  - Authors with more than 3 books.

## Project Structure

- `AuthorBook`: Association table linking authors and books.
- `Author`: Represents an author with attributes like `first_name`, `last_name`, `birth_date`, and `birth_place`.
- `Book`: Represents a book with attributes like `title`, `category`, `pages`, and `release_date`.

## Setup

### Requirements

- Python 3.x
- SQLAlchemy
- Faker
- Random
- Datetime

Install dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### Database initialization

Run the main() function to initialize the SQLite database and populate 
it with random authors and books.

```bash
python main.py
```


