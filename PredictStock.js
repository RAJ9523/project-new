import React, { useState } from 'react';
import { Box, TextField, Button, Typography, CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const PredictStock = () => {
  const navigate = useNavigate();
  const [openPrice, setOpenPrice] = useState('');
  const [predictedPrice, setPredictedPrice] = useState(null); // Store the predicted stock price
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Handle input change
  const handleChange = (e) => {
    setOpenPrice(e.target.value);
  };

  // Handle stock prediction
  const handlePredict = async () => {
    if (!openPrice || isNaN(openPrice)) {
      setError('Please enter a valid open price');
      return;
    }

    setLoading(true);
    setError('');
    setPredictedPrice(null);  // Reset previous prediction

    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        alert('Please log in first');
        navigate('/login');
        return;
      }

      const response = await fetch('http://localhost:5000/predict-stock', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ open_price: parseFloat(openPrice) }),  // Send open price to backend
      });

      const data = await response.json();

      if (response.ok) {
        // Assuming the response contains the predicted stock price
        setPredictedPrice(data.predicted_price); // Store the predicted price
      } else {
        setError(data.error || 'Failed to predict stock');
      }
    } catch (err) {
      setError('Error fetching stock predictions');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
      <Typography variant="h4" sx={{ mb: 2 }}>
        Stock Price Prediction
      </Typography>

      <TextField
        label="Enter Open Price"
        variant="outlined"
        value={openPrice}
        onChange={handleChange}
        sx={{ mb: 2 }}
        type="number"  // Ensure the input is a number
      />

      <Button variant="contained" onClick={handlePredict} sx={{ mb: 2 }}>
        Predict
      </Button>

      {loading && <CircularProgress />}
      {error && <Typography color="error">{error}</Typography>}

      {predictedPrice !== null && (
        <Box sx={{ mt: 3 }}>
          <Typography variant="h6">Predicted Stock Price:</Typography>
          <Typography variant="h5" sx={{ color: '#1976d2' }}>
            ${predictedPrice.toFixed(2)}
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default PredictStock;
