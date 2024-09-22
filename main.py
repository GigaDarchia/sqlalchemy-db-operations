from sqlalchemy import create_engine, String, Column, Integer, Date, ForeignKey, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship
from faker import Faker
import random
from datetime import datetime

author_num = 500
book_num = 1000

fake = Faker()

Base = declarative_base()

class AuthorBook(Base):
    __tablename__ = "author_book"

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    author_id = Column("author_id", Integer, ForeignKey("authors.id"))
    book_id = Column("book_id", Integer, ForeignKey("books.id"))

    def __repr__(self):
        return f"<AuthorBook(id={self.id} | author_id={self.author_id} | book_id={self.book_id})>"

class Author(Base):
    __tablename__ = "authors"

    author_id = Column("id", Integer, autoincrement=True, primary_key=True)
    first_name = Column("first_name", String, nullable=False)
    last_name = Column("last_name", String, nullable=False)
    birth_date = Column("birth_date", Date, nullable=False)
    birth_place = Column("place_of_birth", String, nullable=False)

    books = relationship("Book", secondary='author_book', back_populates="authors")

    def __repr__(self):
        return (f"<Person(id={self.author_id}, first_name={self.first_name}, last_name={self.last_name}, "
                f"birth_date={self.birth_date}, birth_place={self.birth_place}>")

class Book(Base):
    __tablename__ = "books"

    book_id = Column("id", Integer, autoincrement=True, primary_key=True)
    title = Column("title", String, nullable=False)
    category = Column("category", String, nullable=False)
    pages = Column("pages", Integer, nullable=False)
    release_date = Column("release_date", Date, nullable=False)


    authors = relationship("Author", secondary="author_book", back_populates="books")

    def __repr__(self):
        return (f"<Book(id={self.book_id}, title={self.title}, category={self.category}, pages={self.pages}, "
                f"release_date={self.release_date}, author_id={self.author_id})>")

def insert_into_authors(session: Session, count: int = 500):
    book_list = session.query(Book).all()
    for i in range(count):
        fake_first_name = fake.first_name()
        fake_last_name = fake.last_name()
        fake_birth_date = fake.date_of_birth(minimum_age=15, maximum_age=100)
        fake_birth_place = fake.country()

        books = random.sample(book_list, random.randint(1, 3))

        author = Author(first_name=fake_first_name, last_name=fake_last_name, birth_date=fake_birth_date,
                        birth_place=fake_birth_place, books=books)
        session.add(author)

def insert_into_books(session: Session, count: int = 1000):
    categories = ["Comedy", "Drama", "Horror", "Thriller", "Romance", "Fantasy",
                  "Mystery", "Adventure", "Science Fiction"]
    for i in range(count):
        fake_title = fake.sentence(nb_words=4).replace('.', ' ').title()
        fake_category = random.choice(categories)
        fake_pages = random.randint(150, 1000)
        fake_release_date = fake.date_between(start_date="-30y", end_date="today")
        book = Book(title=fake_title, category=fake_category, pages=fake_pages,
                    release_date=fake_release_date)
        session.add(book)

# Fetch 10 books with most pages
def fetch_books_with_most_pages(session: Session):
    max_pages = session.query(func.max(Book.pages)).scalar()
    results = session.query(Book).filter(Book.pages == max_pages).all()
    print("Books with most pages: ")
    for r in results:
        print(f"{r.title} - {r.pages} pages")

# Fetch average number of pages of every book in the database
def fetch_average_page_number(session: Session):
    avg_pages = session.query(func.avg(Book.pages)).scalar()
    print(f"\nAverage pages - {avg_pages:.0f}\n")

# Fetch the youngest author in the database
def fetch_youngest_author(session: Session):
    latest_birth_date = session.query(func.max(Author.birth_date)).scalar()
    youngest_author = session.query(Author).filter(Author.birth_date == latest_birth_date).one()
    first_name = youngest_author.first_name
    last_name = youngest_author.last_name
    current_date = datetime.now()
    age = current_date.year - latest_birth_date.year - (
    (current_date.month, current_date.day) < (latest_birth_date.month, latest_birth_date.day))
    print(f"Youngest actor - {first_name} {last_name}, aged {age}.\n")

def fetch_authors_with_no_books(session: Session, limit: int = 10):
    pass

def fetch_authors_with_more_than_3_books(session: Session):
    pass


# Main Function
def main():
    engine = create_engine("sqlite:///mydb.db", echo=True)

    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()


    insert_into_books(session, book_num)
    insert_into_authors(session, author_num)

    # fetch_books_with_most_pages(session)
    # fetch_average_page_number(session)
    # fetch_youngest_author(session)
    # results = session.query(Book, Author).filter(Book.author_id == Author.author_id).filter(Author.first_name == "Samantha")
    # for r in results:
    #     print(r)

    session.commit()

if __name__ == '__main__':
    main()


