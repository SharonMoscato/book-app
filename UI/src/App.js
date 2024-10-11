import React, { useState } from 'react';
import './App.css';
import FancyButton from './components/FancyButton';



function App() {
  // Three state: store the list of books, loading status, error
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(false); 
  const [error, setError] = useState(null);

  // Function to fetch books from the BE API
  const fetchBooks = () => {
    setLoading(true);
    setError(null);

    // Make the API call to the backend
    fetch('http://localhost:3001/getBooks')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch');
        }
        return response.json();
      })
      .then(data => {
        setBooks(data.recommendedBooks);
        setLoading(false); 
      })
      .catch(error => {
        setError('Failed to fetch book recommendations.');
        setLoading(false);
      });
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-blue-50 to-blue-200 py-12">
      <h1 className="text-5xl font-extrabold text-center text-gray-900 mb-8 drop-shadow-lg leading-tight">
        Did you enjoy reading <span className="italic text-blue-600">Lord of the Rings</span>? <br />
        Then you should discover new books with our recommendation engine!
      </h1>

      {/* Button to trigger the fetchBooks function when clicked  */}
      <FancyButton text="Get ten book recommendations" onClick={fetchBooks} />

      {/* Show a loading indicator while fetching books */}
      {loading && <p>Loading...</p>}

      {/* Display error message if fetch fails */}
      {error && <p className="text-red-600">{error}</p>}

      {/* Show the list of recommended books once they are fetched */}
      {books.length > 0 && (
        <div className="mt-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-4">
            Recommended Books:
          </h2>
          <ul className="list-disc list-inside text-lg">
            {books.map((book, index) => (
              <li key={index}>{book}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
