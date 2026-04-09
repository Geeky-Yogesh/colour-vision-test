"""
Score Tracker Module - Track and manage test scores over time
"""

import streamlit as st
from datetime import datetime
import pandas as pd
from typing import List, Dict, Any

class ScoreTracker:
    """Handle score tracking and session management"""
    
    @staticmethod
    def initialize_session():
        """Initialize score tracking session"""
        if 'performance_data' not in st.session_state:
            st.session_state.performance_data = {
                'sessions': [],
                'current_session': None,
                'best_score': 0,
                'average_score': 0,
                'total_tests': 0
            }
    
    @staticmethod
    def start_session(test_type: str):
        """Start a new testing session"""
        session_id = f"{test_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session = {
            'session_id': session_id,
            'test_type': test_type,
            'start_time': datetime.now(),
            'scores': [],
            'details': [],
            'completed': False
        }
        
        st.session_state.performance_data['current_session'] = session
        return session_id
    
    @staticmethod
    def add_score(score: float, details: Dict[str, Any] = None):
        """Add a score to current session"""
        if 'performance_data' not in st.session_state:
            ScoreTracker.initialize_session()
        
        if 'current_session' not in st.session_state.performance_data or st.session_state.performance_data['current_session'] is None:
            return
        
        current_session = st.session_state.performance_data['current_session']
        
        # Ensure scores list exists
        if 'scores' not in current_session:
            current_session['scores'] = []
        if 'details' not in current_session:
            current_session['details'] = []
        
        score_entry = {
            'timestamp': datetime.now(),
            'score': score,
            'details': details or {}
        }
        
        current_session['scores'].append(score_entry)
        if details:
            current_session['details'].append(details)
    
    @staticmethod
    def add_ishihara_result(plate_number: int, shown_value: str, user_answer: str, is_correct: bool):
        """Add specific Ishihara test result"""
        if 'performance_data' not in st.session_state:
            ScoreTracker.initialize_session()
        
        if 'current_session' not in st.session_state.performance_data or st.session_state.performance_data['current_session'] is None:
            # Start a new session if none exists
            ScoreTracker.start_session("Ishihara")
        
        details = {
            'plate_number': plate_number,
            'shown_value': shown_value,
            'user_answer': user_answer,
            'is_correct': is_correct
        }
        
        score = 1.0 if is_correct else 0.0
        ScoreTracker.add_score(score, details)
    
    @staticmethod
    def end_session():
        """End current session and update statistics"""
        if 'performance_data' not in st.session_state:
            ScoreTracker.initialize_session()
            return
        
        if 'current_session' not in st.session_state.performance_data or st.session_state.performance_data['current_session'] is None:
            return
        
        current_session = st.session_state.performance_data['current_session']
        current_session['end_time'] = datetime.now()
        current_session['completed'] = True
        
        # Calculate session statistics
        if current_session['scores']:
            scores = [s['score'] for s in current_session['scores']]
            current_session['average_score'] = sum(scores) / len(scores)
            current_session['max_score'] = max(scores)
            current_session['min_score'] = min(scores)
        
        # Add to sessions list
        st.session_state.performance_data['sessions'].append(current_session)
        
        # Update overall statistics
        ScoreTracker.update_overall_stats()
        
        # Clear current session
        st.session_state.performance_data['current_session'] = None
    
    @staticmethod
    def update_overall_stats():
        """Update overall performance statistics"""
        data = st.session_state.performance_data
        all_scores = []
        
        for session in data['sessions']:
            if session['scores']:
                all_scores.extend([s['score'] for s in session['scores']])
        
        if all_scores:
            data['best_score'] = max(all_scores)
            data['average_score'] = sum(all_scores) / len(all_scores)
            data['total_tests'] = len(all_scores)
    
    @staticmethod
    def get_performance_history() -> pd.DataFrame:
        """Get performance history as DataFrame"""
        if 'performance_data' not in st.session_state:
            ScoreTracker.initialize_session()
            return pd.DataFrame()
        
        data = st.session_state.performance_data
        
        rows = []
        for session in data['sessions']:
            for score_entry in session['scores']:
                rows.append({
                    'session_id': session['session_id'],
                    'test_type': session['test_type'],
                    'timestamp': score_entry['timestamp'],
                    'score': score_entry['score'],
                    'session_average': session.get('average_score', 0)
                })
        
        return pd.DataFrame(rows)
    
    @staticmethod
    def get_session_details(session_id: str) -> Dict[str, Any]:
        """Get detailed information for a specific session"""
        if 'performance_data' not in st.session_state:
            ScoreTracker.initialize_session()
            return None
        
        for session in st.session_state.performance_data['sessions']:
            if session['session_id'] == session_id:
                return session
        return None
    
    @staticmethod
    def get_best_sessions(limit: int = 5) -> List[Dict[str, Any]]:
        """Get top performing sessions"""
        if 'performance_data' not in st.session_state:
            ScoreTracker.initialize_session()
            return []
        
        sessions = st.session_state.performance_data['sessions']
        completed_sessions = [s for s in sessions if s['completed'] and 'average_score' in s]
        
        # Sort by average score
        completed_sessions.sort(key=lambda x: x['average_score'], reverse=True)
        return completed_sessions[:limit]
    
    @staticmethod
    def clear_all_data():
        """Clear all performance data"""
        st.session_state.performance_data = {
            'sessions': [],
            'current_session': None,
            'best_score': 0,
            'average_score': 0,
            'total_tests': 0
        }
    
    @staticmethod
    def export_data() -> str:
        """Export performance data as CSV string"""
        df = ScoreTracker.get_performance_history()
        return df.to_csv(index=False)
