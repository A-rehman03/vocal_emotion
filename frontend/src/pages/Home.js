import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Brain, 
  Heart, 
  Mic, 
  MessageCircle, 
  Zap, 
  Shield, 
  Users, 
  BarChart3,
  ArrowRight,
  Play,
  Star
} from 'lucide-react';

const Home = () => {
  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Emotion Recognition',
      description: 'Advanced machine learning algorithms that accurately detect emotions from speech patterns, tone, and voice characteristics.',
      color: 'primary'
    },
    {
      icon: Heart,
      title: 'Emotionally Intelligent Responses',
      description: 'Get personalized responses that understand and adapt to your emotional state, creating more meaningful interactions.',
      color: 'secondary'
    },
    {
      icon: Mic,
      title: 'Real-Time Voice Analysis',
      description: 'Instant emotion detection from live voice input with minimal latency for seamless conversation flow.',
      color: 'emotion-excited'
    },
    {
      icon: MessageCircle,
      title: 'Natural Conversation Flow',
      description: 'Engage in natural, context-aware conversations that feel human and emotionally responsive.',
      color: 'emotion-calm'
    },
    {
      icon: Zap,
      title: 'Lightning Fast Processing',
      description: 'Optimized algorithms ensure quick response times while maintaining high accuracy in emotion detection.',
      color: 'emotion-happy'
    },
    {
      icon: Shield,
      title: 'Privacy & Security First',
      description: 'Your voice data is protected with enterprise-grade security and privacy controls.',
      color: 'emotion-confident'
    }
  ];

  const stats = [
    { number: '99.2%', label: 'Emotion Accuracy' },
    { number: '<100ms', label: 'Response Time' },
    { number: '8+', label: 'Emotions Detected' },
    { number: '24/7', label: 'Availability' }
  ];

  const testimonials = [
    {
      name: 'Sarah Johnson',
      role: 'Mental Health Counselor',
      content: 'Vocal Emotion AI has transformed how I understand my clients. The emotion recognition is incredibly accurate and helps me provide better support.',
      rating: 5
    },
    {
      name: 'Michael Chen',
      role: 'Customer Service Manager',
      content: 'Our customer satisfaction scores increased by 40% after implementing Vocal Emotion AI. It helps our agents respond with the right emotional tone.',
      rating: 5
    },
    {
      name: 'Emily Rodriguez',
      role: 'UX Researcher',
      content: 'The real-time emotion analysis is groundbreaking. It opens up so many possibilities for creating more empathetic user experiences.',
      rating: 5
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-primary-50 via-white to-secondary-50 py-20 lg:py-32 overflow-hidden">
        <div className="absolute inset-0 bg-grid-pattern opacity-5"></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          <div className="text-center max-w-4xl mx-auto">
            <div className="inline-flex items-center space-x-2 bg-primary-100 text-primary-700 px-4 py-2 rounded-full text-sm font-medium mb-6">
              <Brain className="h-4 w-4" />
              <span>AI-Powered Emotion Recognition</span>
            </div>
            
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
              Understand Emotions Through
              <span className="text-gradient block">Voice & AI</span>
            </h1>
            
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Experience the future of human-computer interaction with our advanced speech emotion recognition technology. 
              Get emotionally intelligent responses that truly understand how you feel.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link
                to="/register"
                className="btn-primary px-8 py-4 text-lg font-semibold flex items-center space-x-2 group"
              >
                <span>Get Started Free</span>
                <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform duration-200" />
              </Link>
              <button className="btn-outline px-8 py-4 text-lg font-semibold flex items-center space-x-2">
                <Play className="h-5 w-5" />
                <span>Watch Demo</span>
              </button>
            </div>
          </div>
        </div>
        
        {/* Floating Elements */}
        <div className="absolute top-20 left-10 animate-float">
          <div className="h-20 w-20 bg-primary-200 rounded-full opacity-20"></div>
        </div>
        <div className="absolute bottom-20 right-10 animate-float" style={{ animationDelay: '2s' }}>
          <div className="h-16 w-16 bg-secondary-200 rounded-full opacity-20"></div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-primary-600 mb-2">
                  {stat.number}
                </div>
                <div className="text-gray-600 font-medium">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Powerful Features for Emotion Recognition
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Our cutting-edge technology combines advanced AI with sophisticated speech analysis 
              to deliver unparalleled emotion recognition capabilities.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div key={index} className="card-hover group">
                  <div className={`h-12 w-12 bg-${feature.color}-100 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-200`}>
                    <Icon className={`h-6 w-6 text-${feature.color}-600`} />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Experience emotion recognition in three simple steps
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="h-16 w-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-primary-600">1</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Speak Naturally</h3>
              <p className="text-gray-600">
                Simply speak into your microphone or upload an audio file. Our system works with any voice input.
              </p>
            </div>
            
            <div className="text-center">
              <div className="h-16 w-16 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-secondary-600">2</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">AI Analysis</h3>
              <p className="text-gray-600">
                Our advanced AI analyzes your speech patterns, tone, and voice characteristics in real-time.
              </p>
            </div>
            
            <div className="text-center">
              <div className="h-16 w-16 bg-emotion-excited/20 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-emotion-excited">3</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Get Response</h3>
              <p className="text-gray-600">
                Receive emotionally intelligent responses that understand and adapt to your emotional state.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Loved by Users Worldwide
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              See what our users are saying about Vocal Emotion AI
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="card text-center">
                <div className="flex justify-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                <p className="text-gray-600 mb-6 italic">
                  "{testimonial.content}"
                </p>
                <div>
                  <div className="font-semibold text-gray-900">{testimonial.name}</div>
                  <div className="text-sm text-gray-500">{testimonial.role}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-primary-600 to-secondary-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Experience Emotion Recognition?
          </h2>
          <p className="text-xl text-primary-100 mb-8">
            Join thousands of users who are already experiencing the future of AI-powered emotion recognition.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/register"
              className="bg-white text-primary-600 hover:bg-gray-100 font-semibold px-8 py-4 rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2"
            >
              <span>Start Free Trial</span>
              <ArrowRight className="h-5 w-5" />
            </Link>
            <Link
              to="/contact"
              className="border-2 border-white text-white hover:bg-white hover:text-primary-600 font-semibold px-8 py-4 rounded-lg transition-colors duration-200"
            >
              Contact Sales
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
