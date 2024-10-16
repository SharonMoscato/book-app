import pandas as pd
import s3fs
import logging

logging.basicConfig(level=logging.INFO)

def configure_s3fs(minio_endpoint, access_key, secret_key):
    try:
        s3_fs = s3fs.S3FileSystem(
            key=access_key, 
            secret=secret_key, 
            client_kwargs={'endpoint_url': minio_endpoint})
        logging.info("Successfully connected to S3 (MinIO)")
        return s3_fs
    except Exception as e:
        logging.error(f"Error configuring S3 connection: {e}")
        raise

def load_data(bucket_name, s3_fs):
    parquet_files = s3_fs.glob(f's3://{bucket_name}/*.parquet')
    return pd.concat([pd.read_parquet(parquet_file, filesystem=s3_fs) for parquet_file in parquet_files])


def tolkien_readers(dataset, book_title, author):
        """
        Find the list of users who have read the book title .
        
        :param dataset, book_title, author.
        :return: List of unique user IDs who read the book".
        """
        try:
            tolkien_readers = dataset.loc[
                (dataset['Book-Title'] == book_title) & 
                dataset['Book-Author'].str.contains(author, case=False), 'User-ID'
            ].unique()
            return tolkien_readers
        except Exception as e:
            logging.error(f"Error finding Tolkien readers: {e}")
            raise

def get_books_to_compare(dataset, readers, ratings_threshold):
    """
    Get the list of books read by the reader of the chosen book title that have ratings above a certain threshold.
    
    :param dataset: pd dataframe containing ratings and book details.
    :param readers: List of the selected book readers' User IDs.
    :param ratings_threshold: Minimum number of ratings for a book to be included, defined in config.
    :return: List of book titles that meet the criteria.
    """
    books_of_tolkien_readers = dataset[dataset['User-ID'].isin(readers)]
    number_of_ratings_per_book = books_of_tolkien_readers.groupby('Book-Title').count().reset_index()
    books_to_compare = number_of_ratings_per_book['Book-Title'][number_of_ratings_per_book['User-ID'] >= ratings_threshold]
    return books_to_compare.tolist()

def prepare_ratings_data(dataset, books_to_compare):
    """
    Prepare the ratings data for correlation analysis by filtering the dataset based on the books to compare 
    and transforming it into a pivot table format.

    This function performs the following steps:
    1. Filters the dataset to include only the books specified in `books_to_compare`.
    2. Groups the data by 'User-ID' and 'Book-Title' and computes the mean rating for each book per user.
    3. Pivots the grouped data into a matrix where each row represents a user, each column represents a book, 
       and the values are the mean ratings for the corresponding user-book pair.

    :param dataset: pd dataframe containing ratings and book details.
    :param books_to_compare: list of book titles to filter the dataset.
    
    :return: A tuple containing:
        - ratings_data_raw: DataFrame with user ratings filtered by the specified books.
        - dataset_for_corr: Pivot table where rows are users, columns are books, and values are mean ratings.
    """

    ratings_data_raw = dataset[['User-ID', 'Book-Rating', 'Book-Title']][dataset['Book-Title'].isin(books_to_compare)]
    ratings_data_raw_nodup = ratings_data_raw.groupby(['User-ID', 'Book-Title'])['Book-Rating'].mean().reset_index()
    dataset_for_corr = ratings_data_raw_nodup.pivot(index='User-ID', columns='Book-Title', values='Book-Rating')
    return ratings_data_raw, dataset_for_corr


def compute_correlations(dataset_for_corr, target_book, books_to_compare, ratings_data_raw):
    """
    Compute the correlation of books with the target book (e.g., 'The Fellowship of the Ring') 
    and their average ratings, in a single loop.

    :param dataset_for_corr: Pivot table with users as rows and books as columns.
    :param target_book: The book for which correlations are computed.
    :param books_to_compare: List of books to compare with the target book.
    :param ratings_data_raw: Raw ratings data used to compute the average ratings of the books.
    
    :return: DataFrame containing correlations, book titles, and average ratings.
    """
    dataset_of_other_books = dataset_for_corr.drop([target_book], axis=1, inplace=False)

    avg_ratings = ratings_data_raw[ratings_data_raw['Book-Title'].isin(books_to_compare)].groupby('Book-Title')['Book-Rating'].mean()

    book_titles = []
    correlations = []
    avg_rating_values = []

    for book in dataset_of_other_books.columns:
        corr_value = dataset_for_corr[target_book].corr(dataset_of_other_books[book])
        book_titles.append(book)
        correlations.append(corr_value)
        avg_rating_values.append(avg_ratings[book])

    return pd.DataFrame({
        'book': book_titles,
        'corr': correlations,
        'avg_rating': avg_rating_values})

