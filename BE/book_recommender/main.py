import logging
import json
from book_recommender.config import Config
from book_rec import configure_s3fs, load_data
from book_rec import (tolkien_readers, get_books_to_compare, prepare_ratings_data, compute_correlations)

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    try:
        s3_fs = configure_s3fs(Config.minio_endpoint.value, Config.access_key.value, Config.secret_key.value)
        dataset = load_data(Config.bucket_name.value, s3_fs)

        reader_ids = tolkien_readers(dataset, "the fellowship of the ring (the lord of the rings, part 1)", "tolkien")
        books_to_compare = get_books_to_compare(dataset, reader_ids, Config.rating_threshold.value)
        ratings_data_raw, dataset_for_corr = prepare_ratings_data(dataset, books_to_compare)
        correlation_results = compute_correlations(dataset_for_corr, "the fellowship of the ring (the lord of the rings, part 1)", books_to_compare, ratings_data_raw)

        top_books = correlation_results.sort_values('corr', ascending=False).head(10)
        recommended_books = top_books['book'].tolist()

        print(json.dumps({"recommendedBooks": recommended_books}))

    except Exception as e:
        logging.error(f"Error in book recommendation process: {e}")
        print(json.dumps({"error": str(e)}))
