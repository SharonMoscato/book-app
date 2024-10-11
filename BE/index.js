const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');

const app = express();
app.use(cors());
const port = 3001;
const pythonScriptPath = './scripts/book_rec.py';

// GET route for /gerBooks endpoint
app.get('/getBooks', (req, res) => {
  exec(`python3 ${pythonScriptPath}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error: ${error.message}`);
      res.status(500).send('Error executing the Python script.');
      return;
    }
    if (stderr && !stderr.includes('FutureWarning') && !stderr.includes('Skipping line')) {
      console.error(`stderr: ${stderr}`);
      res.status(500).send('Error in Python script.');
      return;
    }
    const bookList = stdout.split('\n').filter(line => line.trim() !== '');
    // send the books list in json format
    res.json({ recommendedBooks: bookList });
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
