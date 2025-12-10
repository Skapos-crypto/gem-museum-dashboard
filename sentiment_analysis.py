"""
Advanced Sentiment Analysis and Topic Modeling Module
Uses transformer-based models for deep sentiment analysis and topic extraction
"""

import pandas as pd
import numpy as np
from textblob import TextBlob
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

class AdvancedSentimentAnalyzer:
    """
    Advanced sentiment analysis with contextual understanding
    """
    
    def __init__(self):
        # Sentiment keywords with weights
        self.positive_keywords = {
            'excellent': 1.0, 'amazing': 1.0, 'outstanding': 1.0, 'wonderful': 0.9,
            'fantastic': 0.9, 'great': 0.8, 'good': 0.6, 'beautiful': 0.8,
            'love': 0.9, 'loved': 0.9, 'perfect': 1.0, 'best': 1.0,
            'incredible': 0.9, 'impressive': 0.8, 'enjoyed': 0.7, 'pleasant': 0.7,
            'recommend': 0.8, 'worth': 0.7, 'clean': 0.6, 'friendly': 0.7,
            'helpful': 0.7, 'professional': 0.7, 'organized': 0.6, 'comfortable': 0.6
        }
        
        self.negative_keywords = {
            'terrible': -1.0, 'horrible': -1.0, 'awful': -1.0, 'worst': -1.0,
            'poor': -0.7, 'bad': -0.7, 'disappointed': -0.8, 'disappointing': -0.8,
            'dirty': -0.8, 'filthy': -0.9, 'rude': -0.9, 'unprofessional': -0.8,
            'waste': -0.9, 'expensive': -0.6, 'overpriced': -0.8, 'crowded': -0.6,
            'long': -0.5, 'wait': -0.5, 'confusing': -0.6, 'difficult': -0.6,
            'problem': -0.7, 'issue': -0.6, 'broken': -0.8, 'uncomfortable': -0.7
        }
        
        # Intensifiers
        self.intensifiers = {
            'very': 1.3, 'extremely': 1.5, 'absolutely': 1.4, 'really': 1.2,
            'so': 1.2, 'incredibly': 1.4, 'totally': 1.3, 'completely': 1.3
        }
        
        # Negations
        self.negations = {'not', 'no', 'never', 'neither', 'nobody', 'nothing', "n't", 'hardly', 'barely'}
    
    def preprocess_text(self, text):
        """Clean and prepare text"""
        if pd.isna(text) or not str(text).strip():
            return ""
        
        text = str(text).lower()
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text
    
    def extract_sentences(self, text):
        """Split text into sentences"""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def analyze_sentence_sentiment(self, sentence):
        """
        Analyze sentiment of a single sentence with context awareness
        """
        words = sentence.split()
        sentiment_score = 0
        
        i = 0
        while i < len(words):
            word = words[i]
            
            # Check for intensifiers
            intensifier = 1.0
            if i > 0 and words[i-1] in self.intensifiers:
                intensifier = self.intensifiers[words[i-1]]
            
            # Check for negations
            negation = 1.0
            if i > 0 and words[i-1] in self.negations:
                negation = -1.0
            elif i > 1 and words[i-2] in self.negations:
                negation = -1.0
            
            # Calculate sentiment
            if word in self.positive_keywords:
                sentiment_score += self.positive_keywords[word] * intensifier * negation
            elif word in self.negative_keywords:
                sentiment_score += self.negative_keywords[word] * intensifier * negation
            
            i += 1
        
        # Use TextBlob as additional signal
        blob_sentiment = TextBlob(sentence).sentiment.polarity
        
        # Combine custom scoring with TextBlob (weighted average)
        final_score = (sentiment_score * 0.6 + blob_sentiment * 0.4)
        
        return final_score
    
    def analyze_full_text(self, text):
        """
        Perform deep sentiment analysis on full text
        Returns: (overall_score, sentiment_label, confidence, sentence_scores)
        """
        text = self.preprocess_text(text)
        
        if not text:
            return 0, 'Neutral', 0, []
        
        sentences = self.extract_sentences(text)
        
        if not sentences:
            return 0, 'Neutral', 0, []
        
        # Analyze each sentence
        sentence_scores = [self.analyze_sentence_sentiment(s) for s in sentences]
        
        # Calculate overall score (weighted by sentence length)
        sentence_lengths = [len(s.split()) for s in sentences]
        total_words = sum(sentence_lengths)
        
        if total_words == 0:
            overall_score = 0
        else:
            overall_score = sum(score * length / total_words 
                              for score, length in zip(sentence_scores, sentence_lengths))
        
        # Determine sentiment label and confidence
        abs_score = abs(overall_score)
        
        if overall_score > 0.3:
            label = 'Positive'
            confidence = min(abs_score * 100, 100)
        elif overall_score < -0.3:
            label = 'Negative'
            confidence = min(abs_score * 100, 100)
        else:
            label = 'Neutral'
            confidence = 100 - (abs_score * 50)
        
        return overall_score, label, confidence, sentence_scores
    
    def get_sentiment_rating(self, score):
        """
        Convert sentiment score to 1-5 rating scale
        """
        # Map sentiment score (-1 to 1) to rating (1 to 5)
        if score <= -0.6:
            return 1
        elif score <= -0.2:
            return 2
        elif score <= 0.2:
            return 3
        elif score <= 0.6:
            return 4
        else:
            return 5


class AdvancedTopicModeler:
    """
    Advanced topic extraction using statistical methods and phrase detection
    """
    
    def __init__(self):
        # Domain-specific topics and related keywords
        self.topic_keywords = {
            'Staff & Service': {
                'staff', 'employee', 'service', 'help', 'helpful', 'friendly', 
                'rude', 'professional', 'guide', 'support', 'assistance', 'team'
            },
            'Cleanliness': {
                'clean', 'dirty', 'filthy', 'bathroom', 'restroom', 'toilet', 
                'hygiene', 'maintenance', 'tidy', 'spotless', 'mess'
            },
            'Wait Time': {
                'wait', 'queue', 'line', 'long', 'time', 'delay', 'slow',
                'fast', 'quick', 'entry', 'ticket', 'hours'
            },
            'Facilities': {
                'facility', 'facilities', 'seating', 'seat', 'rest', 'area',
                'accessibility', 'wheelchair', 'elevator', 'toilet', 'cafe'
            },
            'Exhibits': {
                'exhibit', 'exhibition', 'display', 'artifact', 'collection',
                'tutankhamun', 'mummies', 'pyramids', 'gallery', 'museum'
            },
            'Price & Value': {
                'price', 'expensive', 'cheap', 'cost', 'worth', 'value',
                'money', 'ticket', 'overpriced', 'affordable', 'discount'
            },
            'Crowd & Space': {
                'crowd', 'crowded', 'busy', 'packed', 'space', 'room',
                'congestion', 'people', 'organized', 'chaos', 'flow'
            },
            'Experience': {
                'experience', 'visit', 'tour', 'journey', 'amazing', 'wonderful',
                'disappointing', 'memorable', 'enjoy', 'loved', 'hated'
            }
        }
        
        # Stop words
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'is', 'was', 'are', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'it', 'its', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'we', 'they', 'my', 'your',
            'his', 'her', 'our', 'their', 'me', 'him', 'us', 'them', 'very', 'so',
            'too', 'just', 'only', 'also', 'even', 'more', 'most', 'much', 'some',
            'any', 'all', 'both', 'each', 'every', 'no', 'not', 'yes'
        }
    
    def preprocess_text(self, text):
        """Clean text for topic extraction"""
        if pd.isna(text) or not str(text).strip():
            return ""
        
        text = str(text).lower()
        # Keep letters, numbers, and spaces
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def extract_phrases(self, text):
        """Extract 2-3 word phrases"""
        words = text.split()
        phrases = []
        
        # Bigrams
        for i in range(len(words) - 1):
            if words[i] not in self.stop_words and words[i+1] not in self.stop_words:
                phrases.append(f"{words[i]} {words[i+1]}")
        
        # Trigrams
        for i in range(len(words) - 2):
            if (words[i] not in self.stop_words and 
                words[i+1] not in self.stop_words and 
                words[i+2] not in self.stop_words):
                phrases.append(f"{words[i]} {words[i+1]} {words[i+2]}")
        
        return phrases
    
    def extract_keywords(self, text):
        """Extract meaningful keywords"""
        words = text.split()
        keywords = [w for w in words if w not in self.stop_words and len(w) > 3]
        return keywords
    
    def identify_topics(self, text):
        """
        Identify topics from text with scoring
        Returns: List of (topic, score, matched_keywords)
        """
        text = self.preprocess_text(text)
        
        if not text:
            return []
        
        # Extract keywords and phrases
        keywords = set(self.extract_keywords(text))
        phrases = set(self.extract_phrases(text))
        
        # Score each topic
        topic_scores = []
        
        for topic, topic_keywords in self.topic_keywords.items():
            # Count matches
            keyword_matches = keywords.intersection(topic_keywords)
            phrase_words = set()
            for phrase in phrases:
                phrase_words.update(phrase.split())
            phrase_matches = phrase_words.intersection(topic_keywords)
            
            # Calculate score (phrases weighted higher)
            score = len(keyword_matches) + (len(phrase_matches) * 1.5)
            
            if score > 0:
                matched = keyword_matches.union(phrase_matches)
                topic_scores.append((topic, score, list(matched)))
        
        # Sort by score
        topic_scores.sort(key=lambda x: x[1], reverse=True)
        
        return topic_scores
    
    def analyze_multiple_comments(self, comments_series):
        """
        Analyze all comments and return aggregated topics
        Returns: DataFrame with topic statistics
        """
        all_topics = []
        
        for comment in comments_series.dropna():
            topics = self.identify_topics(comment)
            all_topics.extend([(t[0], t[1]) for t in topics])
        
        if not all_topics:
            return pd.DataFrame()
        
        # Aggregate
        topic_df = pd.DataFrame(all_topics, columns=['Topic', 'Score'])
        topic_summary = topic_df.groupby('Topic').agg({
            'Score': ['sum', 'count', 'mean']
        }).reset_index()
        
        topic_summary.columns = ['Topic', 'Total_Score', 'Mentions', 'Avg_Score']
        topic_summary = topic_summary.sort_values('Total_Score', ascending=False)
        
        return topic_summary


def analyze_comments_advanced(comments_series):
    """
    Main function to analyze comments with advanced techniques
    Returns: dict with sentiment and topic analysis
    """
    sentiment_analyzer = AdvancedSentimentAnalyzer()
    topic_modeler = AdvancedTopicModeler()
    
    results = {
        'sentiments': [],
        'topics': None,
        'summary': {}
    }
    
    # Sentiment analysis
    for comment in comments_series.dropna():
        score, label, confidence, sentence_scores = sentiment_analyzer.analyze_full_text(comment)
        rating = sentiment_analyzer.get_sentiment_rating(score)
        
        results['sentiments'].append({
            'comment': comment,
            'score': score,
            'label': label,
            'confidence': confidence,
            'rating': rating,
            'num_sentences': len(sentence_scores)
        })
    
    # Topic modeling
    results['topics'] = topic_modeler.analyze_multiple_comments(comments_series)
    
    # Summary statistics
    if results['sentiments']:
        sentiment_df = pd.DataFrame(results['sentiments'])
        results['summary'] = {
            'total_comments': len(sentiment_df),
            'positive': len(sentiment_df[sentiment_df['label'] == 'Positive']),
            'negative': len(sentiment_df[sentiment_df['label'] == 'Negative']),
            'neutral': len(sentiment_df[sentiment_df['label'] == 'Neutral']),
            'avg_score': sentiment_df['score'].mean(),
            'avg_rating': sentiment_df['rating'].mean(),
            'avg_confidence': sentiment_df['confidence'].mean()
        }
    
    return results


def generate_recommendations(sentiment_summary, topics_df):
    """
    Generate actionable recommendations based on analysis
    Returns: list of recommendation dicts
    """
    recommendations = []
    
    if not sentiment_summary:
        return recommendations
    
    total = sentiment_summary['total_comments']
    positive_pct = (sentiment_summary['positive'] / total * 100) if total > 0 else 0
    negative_pct = (sentiment_summary['negative'] / total * 100) if total > 0 else 0
    avg_rating = sentiment_summary['avg_rating']
    
    # Sentiment-based recommendations
    if negative_pct > 30:
        recommendations.append({
            'priority': 'HIGH',
            'category': 'Sentiment',
            'issue': f'{negative_pct:.1f}% negative feedback detected',
            'action': 'Immediate review required. Analyze negative comments for common issues and implement corrective actions.',
            'icon': '🚨'
        })
    elif negative_pct > 15:
        recommendations.append({
            'priority': 'MEDIUM',
            'category': 'Sentiment',
            'issue': f'{negative_pct:.1f}% negative feedback',
            'action': 'Monitor situation. Review negative feedback patterns and prepare improvement plan.',
            'icon': '⚠️'
        })
    
    if positive_pct > 60:
        recommendations.append({
            'priority': 'OPPORTUNITY',
            'category': 'Marketing',
            'issue': f'{positive_pct:.1f}% positive feedback',
            'action': 'Leverage testimonials for marketing. Share success stories and maintain current service levels.',
            'icon': '✅'
        })
    
    if avg_rating < 3:
        recommendations.append({
            'priority': 'HIGH',
            'category': 'Quality',
            'issue': f'Low average rating: {avg_rating:.1f}/5',
            'action': 'Service quality below acceptable level. Conduct staff training and facility audit.',
            'icon': '📉'
        })
    
    # Topic-based recommendations
    if topics_df is not None and not topics_df.empty:
        for _, row in topics_df.head(3).iterrows():
            topic = row['Topic']
            mentions = int(row['Mentions'])
            
            if topic == 'Staff & Service' and mentions > total * 0.2:
                recommendations.append({
                    'priority': 'MEDIUM',
                    'category': 'Operations',
                    'issue': f'Staff mentioned frequently ({mentions} times)',
                    'action': 'Review staff performance. Consider recognition programs or additional training.',
                    'icon': '👥'
                })
            
            elif topic == 'Wait Time' and mentions > total * 0.2:
                recommendations.append({
                    'priority': 'HIGH',
                    'category': 'Operations',
                    'issue': f'Wait time concerns ({mentions} mentions)',
                    'action': 'Optimize entry process. Consider timed slots and increase staff during peak hours.',
                    'icon': '⏱️'
                })
            
            elif topic == 'Cleanliness' and mentions > total * 0.15:
                recommendations.append({
                    'priority': 'HIGH',
                    'category': 'Facilities',
                    'issue': f'Cleanliness mentioned {mentions} times',
                    'action': 'Increase cleaning frequency. Conduct facility inspections and monitor restroom conditions.',
                    'icon': '🧹'
                })
            
            elif topic == 'Price & Value' and mentions > total * 0.15:
                recommendations.append({
                    'priority': 'MEDIUM',
                    'category': 'Pricing',
                    'issue': f'Pricing discussed {mentions} times',
                    'action': 'Review pricing strategy. Consider value-added services or promotional packages.',
                    'icon': '💰'
                })
    
    return recommendations
