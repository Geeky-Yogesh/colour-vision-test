"""
Result Interpreter Module - Automatic interpretation of test results
"""

import streamlit as st
from typing import Dict, Any, Tuple
from datetime import datetime

class ResultInterpreter:
    """Handle automatic interpretation of test results"""
    
    # Interpretation thresholds
    ISHIHARA_THRESHOLDS = {
        'normal': {'min': 85, 'max': 100, 'color': 'green', 'icon': '✅'},
        'mild': {'min': 60, 'max': 84, 'color': 'orange', 'icon': '⚠️'},
        'significant': {'min': 0, 'max': 59, 'color': 'red', 'icon': '❌'}
    }
    
    WEBCAM_THRESHOLDS = {
        'excellent': {'min': 90, 'max': 100, 'color': 'green', 'icon': '🌟'},
        'good': {'min': 75, 'max': 89, 'color': 'blue', 'icon': '👍'},
        'moderate': {'min': 60, 'max': 74, 'color': 'orange', 'icon': '📊'},
        'needs_improvement': {'min': 0, 'max': 59, 'color': 'red', 'icon': '📈'}
    }
    
    @staticmethod
    def interpret_ishihara_score(score_percentage: float) -> Dict[str, Any]:
        """Interpret Ishihara test score"""
        
        if score_percentage >= ISHIHARA_THRESHOLDS['normal']['min']:
            category = 'normal'
            diagnosis = "Normal Colour Vision"
            recommendation = "Your colour vision appears to be normal. Regular testing recommended for monitoring."
        elif score_percentage >= ISHIHARA_THRESHOLDS['mild']['min']:
            category = 'mild'
            diagnosis = "Mild Colour Vision Deficiency"
            recommendation = "Consider consulting an eye specialist for professional evaluation."
        else:
            category = 'significant'
            diagnosis = "Significant Colour Vision Deficiency"
            recommendation = "Professional medical consultation recommended for comprehensive evaluation."
        
        threshold_info = ISHIHARA_THRESHOLDS[category]
        
        return {
            'score': score_percentage,
            'category': category,
            'diagnosis': diagnosis,
            'recommendation': recommendation,
            'color': threshold_info['color'],
            'icon': threshold_info['icon'],
            'interpretation': f"{threshold_info['icon']} {diagnosis}"
        }
    
    @staticmethod
    def interpret_webcam_score(score_percentage: float, test_mode: str) -> Dict[str, Any]:
        """Interpret webcam test score"""
        
        if score_percentage >= WEBCAM_THRESHOLDS['excellent']['min']:
            category = 'excellent'
            performance = "Excellent Color Recognition"
            recommendation = "Outstanding performance! Your color recognition skills are excellent."
        elif score_percentage >= WEBCAM_THRESHOLDS['good']['min']:
            category = 'good'
            performance = "Good Color Recognition"
            recommendation = "Good performance! Continue practicing to maintain skills."
        elif score_percentage >= WEBCAM_THRESHOLDS['moderate']['min']:
            category = 'moderate'
            performance = "Moderate Color Recognition"
            recommendation = "Room for improvement. Consider regular practice exercises."
        else:
            category = 'needs_improvement'
            performance = "Needs Improvement"
            recommendation = "Additional practice recommended. Consider professional guidance."
        
        threshold_info = WEBCAM_THRESHOLDS[category]
        
        return {
            'score': score_percentage,
            'test_mode': test_mode,
            'category': category,
            'performance': performance,
            'recommendation': recommendation,
            'color': threshold_info['color'],
            'icon': threshold_info['icon'],
            'interpretation': f"{threshold_info['icon']} {performance}"
        }
    
    @staticmethod
    def interpret_overall_performance() -> Dict[str, Any]:
        """Interpret overall performance across all tests"""
        data = st.session_state.performance_data
        
        if data['total_tests'] == 0:
            return {
                'status': 'no_data',
                'message': 'No test data available for interpretation.',
                'color': 'gray'
            }
        
        avg_score = data['average_score']
        
        # Determine overall category
        if avg_score >= 85:
            category = 'excellent'
            status = "Excellent Overall Performance"
            message = "Outstanding performance across all test types!"
            color = 'green'
        elif avg_score >= 70:
            category = 'good'
            status = "Good Overall Performance"
            message = "Strong performance with room for continued improvement."
            color = 'blue'
        elif avg_score >= 50:
            category = 'moderate'
            status = "Moderate Overall Performance"
            message = "Decent performance. Regular practice recommended."
            color = 'orange'
        else:
            category = 'needs_improvement'
            status = "Needs Improvement"
            message = "Additional practice and professional guidance recommended."
            color = 'red'
        
        return {
            'status': category,
            'message': status,
            'description': message,
            'color': color,
            'average_score': avg_score,
            'total_tests': data['total_tests'],
            'best_score': data['best_score']
        }
    
    @staticmethod
    def get_improvement_suggestions(performance_data: Dict[str, Any]) -> list:
        """Get personalized improvement suggestions"""
        suggestions = []
        
        avg_score = performance_data.get('average_score', 0)
        
        if avg_score < 50:
            suggestions.extend([
                "🎯 Focus on basic color identification exercises",
                "📚 Learn about different types of colour blindness",
                "👁️ Consider professional eye examination",
                "🔄 Practice regularly with different lighting conditions"
            ])
        elif avg_score < 70:
            suggestions.extend([
                "🎨 Practice with color matching games",
                "📱 Use colour vision training apps",
                "💡 Test in various lighting environments",
                "🔍 Focus on distinguishing similar colors"
            ])
        elif avg_score < 85:
            suggestions.extend([
                "⚡ Challenge yourself with harder tests",
                "🎯 Time yourself to improve speed",
                "🌈 Practice with subtle color variations",
                "📊 Track progress to identify patterns"
            ])
        else:
            suggestions.extend([
                "🌟 Maintain excellent performance",
                "🎯 Try advanced colour vision tests",
                "👥 Help others with colour vision training",
                "📚 Learn about colour theory and perception"
            ])
        
        return suggestions
    
    @staticmethod
    def show_interpretation_result(interpretation: Dict[str, Any]):
        """Display interpretation result with appropriate styling"""
        
        # Use the appropriate color for styling
        color = interpretation['color']
        
        if color == 'green':
            st.success(interpretation['interpretation'])
        elif color == 'blue':
            st.info(interpretation['interpretation'])
        elif color == 'orange':
            st.warning(interpretation['interpretation'])
        elif color == 'red':
            st.error(interpretation['interpretation'])
        else:
            st.write(interpretation['interpretation'])
        
        # Show recommendation
        if 'recommendation' in interpretation:
            st.info(f"💡 **Recommendation:** {interpretation['recommendation']}")
    
    @staticmethod
    def generate_performance_report() -> str:
        """Generate a comprehensive performance report"""
        data = st.session_state.performance_data
        
        if data['total_tests'] == 0:
            return "No test data available for report generation."
        
        overall = ResultInterpreter.interpret_overall_performance()
        
        report = f"""
# Colour Vision Test Performance Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overall Performance
{overall['message']}

**Statistics:**
- Total Tests Completed: {data['total_tests']}
- Average Score: {data['average_score']:.1f}%
- Best Score: {data['best_score']:.1f}%
- Completed Sessions: {len([s for s in data['sessions'] if s['completed']])}

## Performance Analysis
"""
        
        # Add test type breakdown
        from .score_tracker import ScoreTracker
        df = ScoreTracker.get_performance_history()
        
        if not df.empty:
            type_stats = df.groupby('test_type')['score'].agg(['mean', 'count']).round(2)
            
            for test_type, stats in type_stats.iterrows():
                report += f"""
### {test_type}
- Average Score: {stats['mean']*100:.1f}%
- Tests Completed: {int(stats['count'])}
"""
        
        # Add improvement suggestions
        suggestions = ResultInterpreter.get_improvement_suggestions(overall)
        if suggestions:
            report += "\n## Recommendations\n"
            for suggestion in suggestions:
                report += f"- {suggestion}\n"
        
        return report
