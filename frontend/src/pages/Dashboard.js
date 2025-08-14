import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { 
  Brain, 
  MessageCircle, 
  Mic, 
  BarChart3, 
  TrendingUp, 
  Activity,
  Calendar,
  Clock
} from 'lucide-react';

const Dashboard = () => {
  const { user } = useAuth();

  const quickActions = [
    {
      title: 'Start Chat',
      description: 'Begin a conversation with our AI chatbot',
      icon: MessageCircle,
      path: '/chat',
      color: 'primary',
      gradient: 'from-primary-500 to-primary-600'
    },
    {
      title: 'Emotion Analysis',
      description: 'Analyze voice emotions in real-time',
      icon: Mic,
      path: '/emotion-analysis',
      color: 'secondary',
      gradient: 'from-secondary-500 to-secondary-600'
    },
    {
      title: 'View Analytics',
      description: 'Check your emotion recognition history',
      icon: BarChart3,
      path: '/analytics',
      color: 'emotion-excited',
      gradient: 'from-emotion-excited to-orange-600'
    }
  ];

  const stats = [
    {
      label: 'Total Conversations',
      value: '24',
      change: '+12%',
      changeType: 'positive',
      icon: MessageCircle
    },
    {
      label: 'Emotions Analyzed',
      value: '156',
      change: '+8%',
      changeType: 'positive',
      icon: Brain
    },
    {
      label: 'Accuracy Rate',
      value: '94.2%',
      change: '+2.1%',
      changeType: 'positive',
      icon: TrendingUp
    },
    {
      label: 'Active Sessions',
      value: '3',
      change: '0%',
      changeType: 'neutral',
      icon: Activity
    }
  ];

  const recentActivity = [
    {
      type: 'chat',
      description: 'Started a new conversation',
      time: '2 minutes ago',
      icon: MessageCircle
    },
    {
      type: 'emotion',
      description: 'Analyzed voice emotion: Happy (92% confidence)',
      time: '15 minutes ago',
      icon: Mic
    },
    {
      type: 'chat',
      description: 'Completed conversation session',
      time: '1 hour ago',
      icon: MessageCircle
    },
    {
      type: 'emotion',
      description: 'Analyzed voice emotion: Calm (87% confidence)',
      time: '2 hours ago',
      icon: Mic
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Welcome Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back, {user?.firstName || user?.username}! 👋
          </h1>
          <p className="text-gray-600">
            Here's what's happening with your Vocal Emotion AI experience today.
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <div key={index} className="card">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600 mb-1">
                      {stat.label}
                    </p>
                    <p className="text-2xl font-bold text-gray-900">
                      {stat.value}
                    </p>
                  </div>
                  <div className={`h-12 w-12 bg-${stat.color}-100 rounded-lg flex items-center justify-center`}>
                    <Icon className={`h-6 w-6 text-${stat.color}-600`} />
                  </div>
                </div>
                <div className="mt-4 flex items-center">
                  <span className={`text-sm font-medium ${
                    stat.changeType === 'positive' ? 'text-green-600' : 
                    stat.changeType === 'negative' ? 'text-red-600' : 'text-gray-600'
                  }`}>
                    {stat.change}
                  </span>
                  <span className="text-sm text-gray-500 ml-2">from last week</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Quick Actions */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Quick Actions
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {quickActions.map((action, index) => {
              const Icon = action.icon;
              return (
                <Link
                  key={index}
                  to={action.path}
                  className="card-hover group cursor-pointer"
                >
                  <div className={`h-12 w-12 bg-gradient-to-r ${action.gradient} rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-200`}>
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {action.title}
                  </h3>
                  <p className="text-gray-600">
                    {action.description}
                  </p>
                </Link>
              );
            })}
          </div>
        </div>

        {/* Recent Activity & Quick Stats */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Recent Activity */}
          <div className="card">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-gray-900">
                Recent Activity
              </h3>
              <Link
                to="/activity"
                className="text-sm text-primary-600 hover:text-primary-700 font-medium"
              >
                View all
              </Link>
            </div>
            <div className="space-y-4">
              {recentActivity.map((activity, index) => {
                const Icon = activity.icon;
                return (
                  <div key={index} className="flex items-start space-x-3">
                    <div className="h-8 w-8 bg-gray-100 rounded-full flex items-center justify-center flex-shrink-0">
                      <Icon className="h-4 w-4 text-gray-600" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-gray-900">
                        {activity.description}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        {activity.time}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Quick Stats */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-6">
              This Week's Summary
            </h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <Calendar className="h-5 w-5 text-gray-400" />
                  <span className="text-sm text-gray-600">Days Active</span>
                </div>
                <span className="text-sm font-semibold text-gray-900">5/7</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <Clock className="h-5 w-5 text-gray-400" />
                  <span className="text-sm text-gray-600">Total Time</span>
                </div>
                <span className="text-sm font-semibold text-gray-900">2h 34m</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <Brain className="h-5 w-5 text-gray-400" />
                  <span className="text-sm text-gray-600">AI Interactions</span>
                </div>
                <span className="text-sm font-semibold text-gray-900">47</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <TrendingUp className="h-5 w-5 text-gray-400" />
                  <span className="text-sm text-gray-600">Improvement</span>
                </div>
                <span className="text-sm font-semibold text-green-600">+15%</span>
              </div>
            </div>
          </div>
        </div>

        {/* Getting Started Tips */}
        <div className="mt-8 card bg-gradient-to-r from-primary-50 to-secondary-50 border-primary-200">
          <div className="flex items-start space-x-4">
            <div className="h-10 w-10 bg-primary-100 rounded-full flex items-center justify-center flex-shrink-0">
              <Brain className="h-5 w-5 text-primary-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Getting Started Tips
              </h3>
              <p className="text-gray-600 mb-4">
                New to Vocal Emotion AI? Here are some tips to get the most out of your experience:
              </p>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Try speaking naturally - our AI works best with conversational speech</li>
                <li>• Use the emotion analysis feature to understand your vocal patterns</li>
                <li>• Check your analytics to track your emotional journey over time</li>
                <li>• Don't hesitate to provide feedback to help improve our AI</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
