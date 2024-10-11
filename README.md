# Book Recommendation App

A simple full-stack application that recommends books for fans of *The Lord of the Rings*. The backend runs a Python script to compute book recommendations, and the frontend provides a user interface to view them.

## Prerequisites

Before running the app, ensure the following are installed:

- **Node.js** and **npm**: for both backend and frontend
- **Docker** and **Docker Compose**: for MinIO service
- **Python**: for running the recommendation script

## Installation

### 1. Backend Setup (BE)

Navigate to the `BE` folder to install the backend dependencies:

    $cd BE
    $npm install

### 2. Frontend Setup (UI)

Go to the `UI` folder to install the frontend dependencies:

    $cd UI
    $npm install

### 3. MinIO Setup

This project uses MinIO for storage. To set it up:

1. Navigate to the MinIO mock services folder:

    $cd ./book-app/BE/mock-services

2. Start the MinIO service:

    $docker compose up -d

3. Create a bucket and upload the required parquet file:

    $mc mb myminio/data

    $mc cp --recursive ./BE/data/ myminio/data/      

4. Access the MinIO console at [http://localhost:9090](http://localhost:9090).

## Running the App

### 1. Start the Backend

To start the backend server, run:

    $cd BE
    $node index.js

The backend will be available at [http://localhost:3001](http://localhost:3001).

### 2. Start the Frontend

To run the frontend, execute:

    $cd UI
    $npm start

The frontend will be available at [http://localhost:3000](http://localhost:3000).

## Backend API

The backend provides an API endpoint that runs a Python script to generate book recommendations.

- **Endpoint**: `/getBooks`
- **Method**: GET
- **Response**: JSON object containing a list of recommended books, e.g. `{ "recommendedBooks": ["Book 1", "Book 2", "Book 3", ...] }`

## File Structure

- **Backend (BE)**: Handles API requests and executes the Python script for recommendations.
- **Frontend (UI)**: Provides a user interface for viewing book recommendations.
- **MinIO**: Local object storage service to store required data for the recommendation engine.
