import React, { useState } from 'react';
import { Slider, Select, MenuItem, Button, CircularProgress, TextField } from '@mui/material';
import { FaMagic } from 'react-icons/fa';
import StoryOutput from './StoryOutput';
import { motion } from 'framer-motion';

function GeneratorForm() {
  const [startPhrase, setStartPhrase] = useState('harry potter');
  const [customStartPhrase, setCustomStartPhrase] = useState('');
  const [wordLimit, setWordLimit] = useState(100);
  const [story, setStory] = useState('Your magical story will appear here...');
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    setStory('');
    try {
      const response = await fetch('https://hp-fanfic-generate.onrender.com/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start: startPhrase === 'custom' ? customStartPhrase : startPhrase, limit: wordLimit }),
      });
      const data = await response.json();
      if (response.ok && data.success) {
        setStory(data.story);
      } else {
        setStory('Error generating story. Please try again.');
      }
    } catch (error) {
      console.error('Error:', error);
      setStory('An error occurred while generating the story.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      <div>
        <label className="block text-sm font-medium text-gray-600 mb-2">Choose a Starting Phrase</label>
        <Select
          value={startPhrase}
          onChange={(e) => setStartPhrase(e.target.value)}
          fullWidth
          className="bg-white/90"
        >
          <MenuItem value="harry potter">Harry Potter</MenuItem>
          <MenuItem value="hermione granger">Hermione Granger</MenuItem>
          <MenuItem value="ron weasley">Ron Weasley</MenuItem>
          <MenuItem value="dumbledore looked">Dumbledore looked</MenuItem>
          <MenuItem value="hogwarts was">Hogwarts was</MenuItem>
          <MenuItem value="in the common">In the common</MenuItem>
          {/* <MenuItem value="custom">Custom</MenuItem> */}
        </Select>

        {startPhrase === 'custom' && (
          <TextField
            value={customStartPhrase}
            onChange={(e) => setCustomStartPhrase(e.target.value)}
            fullWidth
            placeholder="Enter your custom phrase"
            variant="outlined"
            className="mt-2"
          />
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-600 mb-2">Story Length: {wordLimit} words</label>
        <Slider
          value={wordLimit}
          onChange={(e, newValue) => setWordLimit(newValue)}
          aria-labelledby="word-limit-slider"
          step={10}
          min={50}
          max={500}
          valueLabelDisplay="auto"
          className="text-blue-600"
        />
      </div>

      <Button
        variant="contained"
        color="primary"
        fullWidth
        startIcon={<FaMagic />}
        onClick={handleGenerate}
        disabled={loading}
        className="bg-gradient-to-r from-blue-500 to-blue-700 hover:from-blue-600 hover:to-blue-800"
        style={{ padding: '12px 16px', fontSize: '1.2rem' }}
      >
        {loading ? <CircularProgress size={24} className="text-white" /> : 'Generate Story'}
      </Button>

      <StoryOutput story={story} />
    </motion.div>
  );
}

export default GeneratorForm;
