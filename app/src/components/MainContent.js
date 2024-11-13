import React from 'react';
import GeneratorForm from './GeneratorForm';
import { motion } from 'framer-motion';

function MainContent() {
  return (
    <motion.main
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 1 }}
      className="container mx-auto p-4"
    >
      <div className="glassmorphism bg-white/70 rounded-xl shadow-lg backdrop-blur-md p-8">
        <GeneratorForm />
      </div>
    </motion.main>
  );
}

export default MainContent;
