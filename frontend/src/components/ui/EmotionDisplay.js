import React from 'react';
import { 
  Smile, 
  Frown, 
  Meh, 
  Heart, 
  Zap, 
  AlertCircle, 
  TrendingUp, 
  Sparkles,
  Brain
} from 'lucide-react';

const emotionIcons = {
  happy: Smile,
  sad: Frown,
  angry: Frown,
  neutral: Meh,
  excited: Zap,
  calm: Heart,
  anxious: AlertCircle,
  confident: TrendingUp,
  disgust: Frown,
  fear: AlertCircle,
  surprise: Sparkles
};

const emotionColors = {
  happy: {
    bg: 'bg-yellow-50',
    border: 'border-yellow-200',
    text: 'text-yellow-800',
    icon: 'text-yellow-600',
    progress: 'bg-yellow-500'
  },
  sad: {
    bg: 'bg-blue-50',
    border: 'border-blue-200',
    text: 'text-blue-800',
    icon: 'text-blue-600',
    progress: 'bg-blue-500'
  },
  angry: {
    bg: 'bg-red-50',
    border: 'border-red-200',
    text: 'text-red-800',
    icon: 'text-red-600',
    progress: 'bg-red-500'
  },
  neutral: {
    bg: 'bg-gray-50',
    border: 'border-gray-200',
    text: 'text-gray-800',
    icon: 'text-gray-600',
    progress: 'bg-gray-500'
  },
  excited: {
    bg: 'bg-orange-50',
    border: 'border-orange-200',
    text: 'text-orange-800',
    icon: 'text-orange-600',
    progress: 'bg-orange-500'
  },
  calm: {
    bg: 'bg-green-50',
    border: 'border-green-200',
    text: 'text-green-800',
    icon: 'text-green-600',
    progress: 'bg-green-500'
  },
  anxious: {
    bg: 'bg-purple-50',
    border: 'border-purple-200',
    text: 'text-purple-800',
    icon: 'text-purple-600',
    progress: 'bg-purple-500'
  },
  confident: {
    bg: 'bg-indigo-50',
    border: 'border-indigo-200',
    text: 'text-indigo-800',
    icon: 'text-indigo-600',
    progress: 'bg-indigo-500'
  },
  disgust: {
    bg: 'bg-red-50',
    border: 'border-red-200',
    text: 'text-red-800',
    icon: 'text-red-600',
    progress: 'bg-red-500'
  },
  fear: {
    bg: 'bg-purple-50',
    border: 'border-purple-200',
    text: 'text-purple-800',
    icon: 'text-purple-600',
    progress: 'bg-purple-500'
  },
  surprise: {
    bg: 'bg-pink-50',
    border: 'border-pink-200',
    text: 'text-pink-800',
    icon: 'text-pink-600',
    progress: 'bg-pink-500'
  }
};

const EmotionDisplay = ({ 
  emotion, 
  confidence, 
  size = 'lg',
  showConfidence = true,
  animated = true,
  className = ''
}) => {
  const IconComponent = emotionIcons[emotion] || Brain;
  const colors = emotionColors[emotion] || emotionColors.neutral;
  
  const sizeClasses = {
    sm: {
      container: 'w-12 h-12',
      icon: 'h-6 w-6',
      text: 'text-sm',
      confidence: 'text-xs'
    },
    md: {
      container: 'w-16 h-16',
      icon: 'h-8 w-8',
      text: 'text-base',
      confidence: 'text-sm'
    },
    lg: {
      container: 'w-24 h-24',
      icon: 'h-12 w-12',
      text: 'text-2xl',
      confidence: 'text-lg'
    },
    xl: {
      container: 'w-32 h-32',
      icon: 'h-16 w-16',
      text: 'text-3xl',
      confidence: 'text-xl'
    }
  };

  const currentSize = sizeClasses[size];

  return (
    <div className={`flex flex-col items-center space-y-3 ${className}`}>
      <div className={`
        ${currentSize.container} 
        ${colors.bg} 
        ${colors.border} 
        border-2 
        rounded-full 
        flex items-center justify-center
        ${animated ? 'animate-scale-in hover-lift' : ''}
        transition-all duration-300
      `}>
        <IconComponent className={`${currentSize.icon} ${colors.icon}`} />
      </div>
      
      <div className="text-center">
        <h3 className={`${currentSize.text} font-bold ${colors.text} capitalize`}>
          {emotion}
        </h3>
        {showConfidence && (
          <p className={`${currentSize.confidence} font-semibold text-primary-600`}>
            {Math.round(confidence * 100)}% Confidence
          </p>
        )}
      </div>
    </div>
  );
};

export const EmotionBreakdown = ({ emotions, className = '' }) => {
  const sortedEmotions = Object.entries(emotions || {})
    .sort((a, b) => b[1] - a[1]);

  return (
    <div className={`space-y-3 ${className}`}>
      <h4 className="font-semibold text-gray-900 mb-4">Emotion Breakdown</h4>
      {sortedEmotions.map(([emotion, confidence]) => {
        const IconComponent = emotionIcons[emotion] || Brain;
        const colors = emotionColors[emotion] || emotionColors.neutral;
        
        return (
          <div key={emotion} className="flex items-center space-x-3 animate-fade-in-up">
            <div className="flex items-center space-x-2 min-w-0 flex-1">
              <IconComponent className={`h-5 w-5 ${colors.icon}`} />
              <span className="font-medium text-gray-700 capitalize">{emotion}</span>
            </div>
            <div className="flex-1 bg-gray-200 rounded-full h-2 overflow-hidden">
              <div
                className={`h-2 rounded-full ${colors.progress} transition-all duration-1000 ease-out`}
                style={{ width: `${confidence * 100}%` }}
              />
            </div>
            <span className="text-sm font-semibold text-gray-600 min-w-0">
              {Math.round(confidence * 100)}%
            </span>
          </div>
        );
      })}
    </div>
  );
};

export default EmotionDisplay;
