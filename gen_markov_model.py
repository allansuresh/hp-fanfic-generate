# gen_markov_model.py
from collections import defaultdict
import random

class ContextTracker:
    def __init__(self, window_size=20):
        self.window_size = window_size
        self.themes = {
            'location': defaultdict(lambda: defaultdict(float)),
            'time': defaultdict(lambda: defaultdict(float)),
            'atmosphere': defaultdict(lambda: defaultdict(float)),
            'emotion': defaultdict(lambda: defaultdict(float))
        }
        self.context_words = defaultdict(lambda: defaultdict(float))
        self.scene_transitions = defaultdict(lambda: defaultdict(float))
    
    def learn_contexts(self, cleaned_stories, batch_size=1000):
        """Learn contextual patterns from the text in batches"""
        window = []
        
        self.context_sets = {
            'location': {'room', 'hall', 'chamber', 'corridor', 'forest', 'castle', 
                        'dungeon', 'office', 'classroom', 'library', 'grounds'},
            'time': {'morning', 'afternoon', 'evening', 'night', 'midnight', 'dawn', 'dusk'},
            'atmosphere': {'dark', 'light', 'cold', 'warm', 'quiet', 'loud', 'silent'},
            'emotion': {'happy', 'angry', 'scared', 'worried', 'excited', 'nervous', 'confused'}
        }
        
        for i in range(0, len(cleaned_stories), batch_size):
            batch = cleaned_stories[i:i + batch_size]
            for word in batch:
                window.append(word)
                if len(window) > self.window_size:
                    window.pop(0)
                self._process_window(window)
            
        self._normalize_patterns()
    
    def _process_window(self, window):
        """Optimized window processing"""
        window_lower = [w.lower() for w in window]
        word_positions = {word: i for i, word in enumerate(window_lower)}
        
        for context_type, context_set in self.context_sets.items():
            matching_words = context_set.intersection(set(window_lower))
            for word in matching_words:
                self._update_context(context_type, word, window_lower, word_positions[word])
        
        for i in range(1, len(window_lower)):
            self.scene_transitions[window_lower[i-1]][window_lower[i]] += 1
    
    def _update_context(self, context_type, trigger_word, window, position):
        """Update context patterns with memory optimization"""
        max_associations = 1000
        
        for i, word in enumerate(window):
            if i != position:
                distance = abs(i - position)
                weight = 1.0 / (distance + 1)
                
                if len(self.themes[context_type][trigger_word]) < max_associations:
                    self.themes[context_type][trigger_word][word] += weight
                
                if len(self.context_words[trigger_word]) < max_associations:
                    self.context_words[trigger_word][word] += weight
    
    def _normalize_patterns(self):
        """Normalize with memory cleanup"""
        for context_type in self.themes:
            for trigger in list(self.themes[context_type]):
                if len(self.themes[context_type][trigger]) > 1000:
                    sorted_items = sorted(self.themes[context_type][trigger].items(), 
                                       key=lambda x: x[1], reverse=True)[:1000]
                    self.themes[context_type][trigger] = defaultdict(float, dict(sorted_items))
                
                total = sum(self.themes[context_type][trigger].values())
                if total > 0:
                    for word in self.themes[context_type][trigger]:
                        self.themes[context_type][trigger][word] /= total
        
        for trigger in list(self.context_words):
            if len(self.context_words[trigger]) > 1000:
                sorted_items = sorted(self.context_words[trigger].items(), 
                                   key=lambda x: x[1], reverse=True)[:1000]
                self.context_words[trigger] = defaultdict(float, dict(sorted_items))
            
            total = sum(self.context_words[trigger].values())
            if total > 0:
                for word in self.context_words[trigger]:
                    self.context_words[trigger][word] /= total
        
        for word in self.scene_transitions:
            total = sum(self.scene_transitions[word].values())
            if total > 0:
                for next_word in self.scene_transitions[word]:
                    self.scene_transitions[word][next_word] /= total

def make_markov_model(cleaned_stories, n_gram=2, sensibility=0.7, batch_size=1000):
    """Creates an optimized Markov model with context awareness"""
    markov_model = {}
    
    # Initialize context tracker and learn patterns in batches
    context_tracker = ContextTracker()
    context_tracker.learn_contexts(cleaned_stories, batch_size)
    
    # Process text in batches
    for i in range(0, len(cleaned_stories) - n_gram, batch_size):
        batch = cleaned_stories[i:i + batch_size]
        
        for j in range(len(batch) - n_gram):
            curr_state = ' '.join(batch[j:j + n_gram])
            next_state = ' '.join(batch[j + n_gram:j + n_gram * 2])
            
            if not curr_state or not next_state:
                continue
            
            if curr_state not in markov_model:
                markov_model[curr_state] = defaultdict(float)
            markov_model[curr_state][next_state] += 1
            
            # Apply context-aware weighting
            curr_words = curr_state.split()
            next_words = next_state.split()
            
            weight = 1.0
            for curr_word in curr_words:
                curr_lower = curr_word.lower()
                
                for next_word in next_words:
                    next_lower = next_word.lower()
                    
                    # Check themes
                    for context_type, themes in context_tracker.themes.items():
                        if curr_lower in themes and next_lower in themes[curr_lower]:
                            weight *= (1 + (sensibility * themes[curr_lower][next_lower]))
                    
                    # Check transitions
                    if curr_lower in context_tracker.scene_transitions:
                        if next_lower in context_tracker.scene_transitions[curr_lower]:
                            weight *= (1 + (sensibility * context_tracker.scene_transitions[curr_lower][next_lower]))
            
            markov_model[curr_state][next_state] *= weight
    
    # Normalize probabilities
    for curr_state in markov_model:
        total = sum(markov_model[curr_state].values())
        if total > 0:
            for state in markov_model[curr_state]:
                markov_model[curr_state][state] /= total
    
    return markov_model