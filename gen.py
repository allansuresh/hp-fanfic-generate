from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import random
import re
from collections import defaultdict

class TextAnalyzer:
    def __init__(self, training_text):
        """Initialize with training text to learn patterns"""
        self.training_text = training_text
        self.proper_nouns = set()
        self.sentence_enders = defaultdict(float)
        self.dialogue_verbs = defaultdict(float)
        
        # HP-specific terms that should be capitalized
        self.hp_terms = {
            'harry', 'potter', 'ron', 'hermione', 'hogwarts', 'dumbledore',
            'voldemort', 'snape', 'hagrid', 'gryffindor', 'slytherin',
            'ravenclaw', 'hufflepuff', 'weasley', 'malfoy', 'hogsmeade',
            'diagon', 'fred', 'george', 'ginny', 'mcgonagall', 'riddle',
            'sirius', 'black', 'lupin', 'neville', 'luna', 'draco'
        }
        
        # Common sentence-ending words
        self.ending_words = {
            'said', 'asked', 'replied', 'muttered', 'whispered', 'shouted',
            'exclaimed', 'thought', 'wondered', 'knew', 'felt', 'saw',
            'continued', 'added', 'explained', 'interrupted', 'agreed'
        }
        
        self.initialize_patterns()

    def initialize_patterns(self):
        """Learn patterns from text without requiring NLTK downloads"""
        # Split text into rough sentences using basic punctuation
        sentences = re.split('[.!?]', self.training_text)
        
        for i, sentence in enumerate(sentences):
            if not sentence.strip():
                continue
                
            words = sentence.strip().split()
            
            # Learn capitalized words as potential proper nouns
            for word in words:
                if word and word[0].isupper():
                    self.proper_nouns.add(word.lower())
            
            # Learn sentence ending patterns
            if len(words) >= 3:
                last_words = ' '.join(words[-3:]).lower()
                self.sentence_enders[last_words] += 1
                
                # Learn dialogue patterns
                if any(verb in words[-1].lower() for verb in self.ending_words):
                    self.dialogue_verbs[words[-1].lower()] += 1
        
        # Add HP terms to proper nouns
        self.proper_nouns.update(self.hp_terms)

    def is_proper_noun(self, word: str) -> bool:
        word_lower = word.lower()
        word_upper = word.upper()
        return (word_lower in self.proper_nouns or 
                word_upper in self.hp_terms)

    def should_end_sentence(self, recent_words: list, words_since_period: int) -> tuple:
        """
        Determine if and how a sentence should end based on multiple factors.
        Returns (should_end: bool, punctuation: str)
        """
        # Too short to end
        if words_since_period < 5:
            return False, ''
        
        # Get the last few words as a pattern
        last_words = [w.lower() for w in recent_words[-3:]]
        pattern = ' '.join(last_words)
        
        # Strong ending indicators
        strong_endings = {
            # Dialogue markers
            'said', 'asked', 'replied', 'muttered', 'whispered', 'shouted',
            # Action completion
            'stopped', 'finished', 'ended', 'concluded', 'completed',
            # State changes
            'disappeared', 'arrived', 'left', 'died', 'fell', 'stood',
            # Time transitions
            'later', 'afterwards', 'finally', 'eventually'
        }
        
        # Question indicators
        question_starters = {'what', 'why', 'how', 'where', 'when', 'who'}
        question_verbs = {'wonder', 'ask', 'questioned', 'inquired'}
        
        # Exclamation indicators
        exclamation_words = {
            'suddenly', 'shouted', 'yelled', 'exclaimed', 'screamed',
            'bang', 'crash', 'boom', 'amazing', 'incredible', 'terrible',
            'horrified', 'shocked', 'alarmed', 'excited'
        }
        
        # Check for specific ending patterns
        if last_words:
            last_word = last_words[-1]
            
            # Direct dialogue endings
            if last_word in strong_endings:
                return True, '.'
                
            # Questions
            if (any(q in pattern for q in question_starters) or 
                any(v in pattern for v in question_verbs)):
                return True, '?'
                
            # Exclamations
            if any(e in pattern for e in exclamation_words):
                return True, '!'
        
        # Length-based endings
        if words_since_period > 25:  # Force end very long sentences
            return True, '.'
        elif words_since_period > 15:  # Probabilistic ending for medium sentences
            # Increasing probability of ending as sentence gets longer
            prob = (words_since_period - 15) / 20
            if random.random() < prob:
                return True, '.'
        
        # Context-based endings
        if len(recent_words) >= 3:
            # End on complete thoughts
            if recent_words[-1].lower() in {'too', 'also', 'well'}:
                return True, '.'
            
            # End after location changes
            location_markers = {'inside', 'outside', 'upstairs', 'downstairs', 'away'}
            if recent_words[-1].lower() in location_markers:
                return True, '.'
            
            # End after time expressions
            time_markers = {'today', 'tomorrow', 'yesterday', 'tonight', 'soon'}
            if recent_words[-1].lower() in time_markers:
                return True, '.'
        
        # Sentence enders from learned patterns
        if pattern in self.sentence_enders:
            if random.random() < 0.3:  # 30% chance to use learned pattern
                # Default to period unless special case detected
                return True, '.'
        
        return False, ''

    def get_punctuation(self, pattern: str) -> str:
        """Helper method to determine appropriate punctuation"""
        # Question patterns
        if any(q in pattern for q in ['what', 'why', 'how', 'where', 'when', 'who']):
            return '?'
            
        # Exclamation patterns
        if any(e in pattern for e in ['suddenly', 'shouted', 'yelled', 'exclaimed']):
            return '!'
            
        # Action patterns
        if any(a in pattern for a in ['ran', 'jumped', 'dashed', 'rushed']):
            if random.random() < 0.3:  # 30% chance for excitement
                return '!'
                
        # Emotional patterns
        if any(e in pattern for e in ['happy', 'angry', 'scared', 'excited']):
            if random.random() < 0.4:  # 40% chance for emotion
                return '!'
        
        # Default to period
        return '.'

    def format_dialogue(self, text: str) -> str:
        """Format dialogue using simple patterns"""
        sentences = re.split('([.!?])', text)
        formatted_sentences = []
        
        for i in range(0, len(sentences), 2):
            sentence = sentences[i]
            punct = sentences[i + 1] if i + 1 < len(sentences) else "."
            
            words = sentence.strip().split()
            if not words:
                continue
                
            # Check for dialogue verbs at the end
            last_word = words[-1].lower() if words else ""
            if last_word in self.dialogue_verbs:
                # Format as dialogue
                speech = ' '.join(words[:-1])
                formatted_sentences.append(f'"{speech}," {last_word}{punct}')
            else:
                formatted_sentences.append(sentence + punct)
        
        return ' '.join(formatted_sentences)

def generate_story(markov_model, start, limit=100):
    """Generate fanfic stories with improved formatting"""
    # Create text analyzer from model keys
    training_text = ' '.join(list(markov_model.keys()))
    analyzer = TextAnalyzer(training_text)
    
    # Initialize variables
    n = 0
    curr_state = start
    next_state = None
    story_words = []
    recent_words = []
    words_since_period = 0
    needs_capitalization = True
    
    # Add initial state
    story_words.extend(start.split())
    recent_words.extend(start.split())
    words_since_period = len(story_words)
    
    # Generate story
    while n < limit:
        # Get next state using original Markov logic
        next_state = random.choices(
            list(markov_model[curr_state].keys()),
            list(markov_model[curr_state].values())
        )
        
        curr_state = next_state[0]
        
        # Format word
        word = curr_state
        if needs_capitalization or analyzer.is_proper_noun(word):
            word = word.capitalize()
            needs_capitalization = False
            
        # Update tracking lists
        story_words.append(word)
        recent_words.append(word)
        if len(recent_words) > 3:
            recent_words.pop(0)
        
        # Check for sentence ending
        should_end, punct = analyzer.should_end_sentence(recent_words, words_since_period)
        if should_end:
            story_words[-1] = story_words[-1] + punct
            words_since_period = 0
            needs_capitalization = True
        else:
            words_since_period += 1
            
        n += 1
    
    # Ensure story ends with punctuation
    if not story_words[-1][-1] in '.!?':
        story_words[-1] += '.'
    
    # Join words and format
    story = ' '.join(story_words)
    
    # Fix spacing and format dialogue
    story = re.sub(r'\s+([.,!?])', r'\1', story)
    story = re.sub(r'([.,!?])(?=[A-Za-z])', r'\1 ', story)
    story = analyzer.format_dialogue(story)
    
    return story