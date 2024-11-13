import React from 'react';
import { Typography, Paper } from '@mui/material';
import { motion } from 'framer-motion';

function StoryOutput({ story }) {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
      <Paper elevation={4} className="p-6 bg-white/90 mt-6 rounded-lg">
        <Typography variant="body1" className="text-gray-800">
          {story}
        </Typography>
      </Paper>
    </motion.div>
  );
}

export default StoryOutput;
