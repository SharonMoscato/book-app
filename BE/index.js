const express = require('express');
const cors = require('cors');
const path = require('path');
const { exec } = require('child_process');

const app = express();
app.use(cors());
const port = 3001;

// Path to the Python script 
const pythonScriptPath = path.join(__dirname, 'book_recommender', 'main.py');
const projectRoot = path.resolve(__dirname);

// GET route for /getBooks endpoint
app.get('/getBooks', (req, res) => {
  // Command to run the Python script
  const command = `python3 ${pythonScriptPath}`;
  const options = { env: { ...process.env, PYTHONPATH: projectRoot } };

  // Execute the Python script
  exec(command, options, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error: ${error.message}`);
      res.status(500).send('Error executing the Python script.');
      return;
    }
    if (stderr) {
      console.log(`stderr output from Python script: ${stderr}`);
    }

    try {
      const output = JSON.parse(stdout);
      if (output.error) {
        res.status(500).json({ error: output.error });
      } else {
        res.json(output);
      }
    } catch (err) {
      console.error(`Failed to parse Python script output: ${err.message}`);
      res.status(500).send('Error parsing Python script output.');
    }
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
