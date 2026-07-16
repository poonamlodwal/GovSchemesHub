import { useNavigate } from 'react-router-dom';
import { Search, Sparkles, ArrowRight, Mic, TrendingUp, Shield, Zap, Users, FileText, Award, ChevronRight, Star, Quote, Bell, ArrowUpRight, BookOpen, Home } from 'lucide-react';
import { HeroCarousel } from '../components/ui/HeroCarousel';
import { Link } from 'react-router-dom';
import { useState } from 'react';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Card } from '../components/ui/Card';
import { Counter } from '../components/ui/Counter';
import { Accordion } from '../components/ui/Accordion';
import { SchemeCard } from '../components/SchemeCard';
import { categories, schemes, stats, testimonials, latestUpdates, knowledgeBaseArticles, faqData, popularSearches } from '../data/schemes';

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  GraduationCap: ({ className }) => <span className={className}>🎓</span>,
  Heart: ({ className }) => <span className={className}>❤️</span>,
  Wheat: ({ className }) => <span className={className}>🌾</span>,
  Stethoscope: ({ className }) => <span className={className}>🩺</span>,
  Briefcase: ({ className }) => <span className={className}>💼</span>,
  Home: ({ className }) => <span className={className}>🏠</span>,
  UserRound: ({ className }) => <span className={className}>🧓</span>,
  BookOpen: ({ className }) => <span className={className}>📚</span>,
  Rocket: ({ className }) => <span className={className}>🚀</span>,
  Accessibility: ({ className }) => <span className={className}>♿</span>,
  Users: ({ className }) => <span className={className}>👥</span>,
  Wrench: ({ className }) => <span className={className}>🔧</span>,
};

const colorMap: Record<string, string> = {
  primary: 'bg-primary-50 text-primary-600 group-hover:bg-primary-100 dark:bg-primary-900/40 dark:text-primary-400 dark:group-hover:bg-primary-900/60',
  saffron: 'bg-saffron-50 text-saffron-600 group-hover:bg-saffron-100 dark:bg-saffron-900/40 dark:text-saffron-400 dark:group-hover:bg-saffron-900/60',
  success: 'bg-success-50 text-success-600 group-hover:bg-success-100 dark:bg-success-900/40 dark:text-success-400 dark:group-hover:bg-success-900/60',
  error: 'bg-error-50 text-error-600 group-hover:bg-error-100 dark:bg-error-900/40 dark:text-error-400 dark:group-hover:bg-error-900/60',
  navy: 'bg-navy-50 text-navy-600 group-hover:bg-navy-100 dark:bg-navy-900/40 dark:text-navy-400 dark:group-hover:bg-navy-900/60',
};

export function HomePage() {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    navigate(`/schemes${searchQuery ? `?q=${encodeURIComponent(searchQuery)}` : ''}`);
  };

  const featuredSchemes = schemes.filter((s) => s.featured).slice(0, 6);

  return (
    <div>
      {/* Hero Section */}
      <section className="relative overflow-hidden gradient-hero">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-10 w-72 h-72 rounded-full bg-white/20 blur-3xl" />
          <div className="absolute bottom-10 right-20 w-96 h-96 rounded-full bg-saffron-300/30 blur-3xl" />
        </div>
        <div className="container-page relative py-12 lg:py-20">
          <div className="grid lg:grid-cols-[1.1fr_1fr] gap-8 lg:gap-12 items-center">
            {/* Left: Search & Content */}
            <div className="max-w-2xl">
              <Badge variant="primary" className="mb-5 bg-white/10 text-primary-200 border border-white/20">
                <Sparkles className="w-3.5 h-3.5" />
                AI-Powered Scheme Discovery
              </Badge>
              <h1 className="font-heading font-bold text-white text-3xl sm:text-4xl md:text-5xl lg:text-6xl leading-tight mb-5 text-balance">
                Find Government Schemes
                <br />
                <span className="bg-gradient-to-r from-saffron-300 to-saffron-500 bg-clip-text text-transparent">
                  You're Eligible For
                </span>
              </h1>
              <p className="text-base md:text-lg text-primary-100 mb-7 leading-relaxed">
                SchemeHub uses AI to match you with the right government schemes, scholarships, subsidies, and services — all in one place, in just a few clicks.
              </p>

              {/* Global Search */}
              <form onSubmit={handleSearch} className="max-w-2xl">
                <div className="relative flex items-center bg-white dark:bg-slate-900 rounded-2xl shadow-elevated p-2">
                  <Search className="absolute left-5 w-5 h-5 text-slate-400 dark:text-slate-500 pointer-events-none" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search 1200+ schemes, scholarships, subsidies..."
                    className="flex-1 pl-12 pr-4 py-3 text-sm text-slate-800 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 bg-transparent outline-none"
                  />
                  <button
                    type="button"
                    className="p-2.5 text-slate-400 dark:text-slate-500 hover:text-primary-600 dark:hover:text-primary-400 transition-colors hidden sm:block"
                    aria-label="Voice search"
                  >
                    <Mic className="w-5 h-5" />
                  </button>
                  <Button type="submit" className="gap-1.5" size="md">
                    <Search className="w-4 h-4" />
                    <span className="hidden sm:inline">Search</span>
                  </Button>
                </div>
              </form>

              {/* Quick Search Filters */}
              <div className="mt-5 flex flex-wrap items-center gap-2">
                <span className="text-sm text-primary-200">Popular:</span>
                {popularSearches.slice(0, 5).map((term) => (
                  <button
                    key={term}
                    onClick={() => navigate(`/schemes?q=${encodeURIComponent(term)}`)}
                    className="px-3 py-1.5 text-xs rounded-full bg-white/10 text-primary-100 hover:bg-white/20 transition-all border border-white/10"
                  >
                    {term}
                  </button>
                ))}
              </div>
            </div>

            {/* Right: Hero Carousel */}
            <div className="h-[280px] sm:h-[360px] lg:h-[460px]">
              <HeroCarousel />
            </div>
          </div>
        </div>

        {/* Wave separator */}
        <div className="relative">
          <svg className="w-full h-12 md:h-20" viewBox="0 0 1440 100" fill="none" preserveAspectRatio="none">
            <path d="M0 100V40C240 80 480 100 720 100C960 100 1200 80 1440 40V100H0Z" fill="white" className="dark:fill-slate-900" />
          </svg>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="container-page -mt-4 pb-12">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {stats.map((stat, i) => (
            <Card key={i} className="p-6 text-center card-hover">
              <div className="text-3xl lg:text-4xl font-heading font-bold gradient-text mb-1">
                <Counter value={stat.value} suffix={stat.suffix} />
              </div>
              <div className="text-sm text-slate-500 dark:text-slate-400 font-medium">{stat.label}</div>
            </Card>
          ))}
        </div>
      </section>

      {/* Categories Section */}
      <section className="container-page section-padding">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <Badge variant="primary" className="mb-3">Browse by Category</Badge>
          <h2 className="font-heading font-bold text-3xl md:text-4xl text-slate-800 dark:text-slate-100 mb-3">
            Find Schemes for Your Needs
          </h2>
          <p className="text-slate-500 dark:text-slate-400">
            Explore government schemes across 12 categories designed for different sections of society.
          </p>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
          {categories.map((cat) => {
            const Icon = iconMap[cat.icon];
            return (
              <Link key={cat.id} to={`/schemes?category=${cat.id}`}>
                <Card hover className="p-5 h-full group">
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 transition-colors ${colorMap[cat.color]}`}>
                    {Icon ? <Icon className="text-2xl" /> : null}
                  </div>
                  <h3 className="font-heading font-semibold text-slate-800 dark:text-slate-100 text-sm mb-1">{cat.name}</h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400 line-clamp-2 mb-3">{cat.description}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-medium text-primary-600">{cat.schemeCount} schemes</span>
                    <ArrowRight className="w-4 h-4 text-slate-300 group-hover:text-primary-600 dark:group-hover:text-primary-400 group-hover:translate-x-1 transition-all" />
                  </div>
                </Card>
              </Link>
            );
          })}
        </div>
      </section>

      {/* Featured Schemes */}
      <section className="bg-slate-50 dark:bg-slate-950 section-padding">
        <div className="container-page">
          <div className="flex items-end justify-between mb-12 flex-wrap gap-4">
            <div>
              <Badge variant="saffron" className="mb-3">
                <Star className="w-3.5 h-3.5" /> Featured
              </Badge>
              <h2 className="font-heading font-bold text-3xl md:text-4xl text-slate-800 dark:text-slate-100">
                Popular Government Schemes
              </h2>
            </div>
            <Link to="/schemes">
              <Button variant="outline" size="sm" className="gap-1.5">
                View All Schemes <ArrowRight className="w-4 h-4" />
              </Button>
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {featuredSchemes.map((scheme) => (
              <SchemeCard key={scheme.id} scheme={scheme} />
            ))}
          </div>
        </div>
      </section>

      {/* How SchemeHub Works */}
      <section className="container-page section-padding">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <Badge variant="navy" className="mb-3">How It Works</Badge>
          <h2 className="font-heading font-bold text-3xl md:text-4xl text-slate-800 dark:text-slate-100 mb-3">
            Find Your Schemes in 3 Simple Steps
          </h2>
          <p className="text-slate-500 dark:text-slate-400">No paperwork. No queues. Just answer a few questions and get matched instantly.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            { icon: Search, step: '01', title: 'Search or Browse', desc: 'Use our smart search or browse by category to explore 1200+ government schemes and services.', color: 'primary' },
            { icon: Sparkles, step: '02', title: 'Check Eligibility', desc: 'Answer a few quick questions and our AI matches you with schemes you qualify for — with confidence scores.', color: 'saffron' },
            { icon: FileText, step: '03', title: 'Apply with Guidance', desc: 'Get step-by-step application guidance, document checklists, and direct links to official portals.', color: 'success' },
          ].map((item, i) => (
            <div key={i} className="relative">
              <Card className="p-8 h-full card-hover">
                <div className="flex items-center gap-4 mb-5">
                  <div className={`w-14 h-14 rounded-2xl flex items-center justify-center ${
                    item.color === 'primary' ? 'bg-primary-100 text-primary-600 dark:bg-primary-900/40 dark:text-primary-400' :
                    item.color === 'saffron' ? 'bg-saffron-100 text-saffron-600 dark:bg-saffron-900/40 dark:text-saffron-400' :
                    'bg-success-100 text-success-600 dark:bg-success-900/40 dark:text-success-400'
                  }`}>
                    <item.icon className="w-7 h-7" />
                  </div>
                  <span className="font-heading font-bold text-4xl text-slate-200 dark:text-slate-700">{item.step}</span>
                </div>
                <h3 className="font-heading font-semibold text-lg text-slate-800 dark:text-slate-100 mb-2">{item.title}</h3>
                <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">{item.desc}</p>
              </Card>
              {i < 2 && (
                <div className="hidden md:flex absolute top-1/2 -right-3 -translate-y-1/2 z-10">
                  <ChevronRight className="w-6 h-6 text-slate-300" />
                </div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* AI Eligibility Assistant Preview */}
      <section className="bg-gradient-to-br from-navy-900 via-primary-900 to-primary-800 relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-10 left-1/4 w-64 h-64 rounded-full bg-saffron-400 blur-3xl" />
          <div className="absolute bottom-10 right-1/4 w-80 h-80 rounded-full bg-primary-400 blur-3xl" />
        </div>
        <div className="container-page relative py-20">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <Badge variant="saffron" className="mb-4 bg-saffron-500/20 text-saffron-300 border border-saffron-400/30">
                <Sparkles className="w-3.5 h-3.5" /> AI-Powered
              </Badge>
              <h2 className="font-heading font-bold text-white text-3xl md:text-4xl mb-4">
                Meet the AI Eligibility Assistant
              </h2>
              <p className="text-primary-100 text-lg mb-6 leading-relaxed">
                Our intelligent assistant asks you a few simple questions about your background and instantly matches you with government schemes you're eligible for — with confidence scores and personalized recommendations.
              </p>
              <div className="space-y-3 mb-8">
                {['8-question smart questionnaire', 'AI-powered eligibility matching', 'Confidence score for each match', 'Direct application links and guidance'].map((feature) => (
                  <div key={feature} className="flex items-center gap-3 text-primary-100">
                    <div className="w-5 h-5 rounded-full bg-success-500/20 flex items-center justify-center flex-shrink-0">
                      <ChevronRight className="w-3 h-3 text-success-400" />
                    </div>
                    <span className="text-sm">{feature}</span>
                  </div>
                ))}
              </div>
              <Link to="/eligibility">
                <Button variant="saffron" size="lg" className="gap-2">
                  <Sparkles className="w-5 h-5" />
                  Try Eligibility Checker
                </Button>
              </Link>
            </div>
            <div className="relative">
              <Card className="p-6 bg-white/95 dark:bg-slate-900/95 backdrop-blur-sm">
                <div className="flex items-center gap-3 mb-5 pb-4 border-b border-slate-100 dark:border-slate-800">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary-500 to-navy-600 flex items-center justify-center">
                    <Sparkles className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h3 className="font-heading font-semibold text-slate-800 dark:text-slate-100 text-sm">SchemeHub AI Assistant</h3>
                    <span className="text-xs text-success-600 flex items-center gap-1">
                      <span className="w-1.5 h-1.5 rounded-full bg-success-500 animate-pulse" /> Analyzing your profile...
                    </span>
                  </div>
                </div>
                <div className="space-y-3">
                  <div className="bg-slate-100 dark:bg-slate-800 rounded-xl rounded-bl-md px-4 py-3 text-sm text-slate-700 dark:text-slate-200 max-w-[80%]">
                    What is your annual family income?
                  </div>
                  <div className="flex justify-end">
                    <div className="bg-primary-600 text-white rounded-xl rounded-br-md px-4 py-3 text-sm max-w-[80%]">
                      Between ₹1-3 lakh
                    </div>
                  </div>
                  <div className="bg-slate-100 dark:bg-slate-800 rounded-xl rounded-bl-md px-4 py-3 text-sm text-slate-700 dark:text-slate-200 max-w-[85%]">
                    <span className="font-medium">Great! Based on your profile, I found 7 matching schemes.</span>
                    <div className="mt-3 space-y-2">
                      {[
                        { name: 'PM-KISAN', score: 95 },
                        { name: 'Ayushman Bharat', score: 88 },
                        { name: 'NSP Scholarship', score: 82 },
                      ].map((m) => (
                        <div key={m.name} className="flex items-center justify-between bg-white dark:bg-slate-900 rounded-lg px-3 py-2">
                          <span className="text-xs font-medium text-slate-700 dark:text-slate-200">{m.name}</span>
                          <Badge variant="success" size="sm">{m.score}% match</Badge>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Popular Services */}
      <section className="container-page section-padding">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <Badge variant="success" className="mb-3">Popular Services</Badge>
          <h2 className="font-heading font-bold text-3xl md:text-4xl text-slate-800 dark:text-slate-100 mb-3">
            Quick Access to Key Services
          </h2>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {[
            { icon: Award, title: 'Scholarships', desc: 'Find education funding', link: '/schemes?category=students' },
            { icon: Shield, title: 'Insurance', desc: 'Health & life coverage', link: '/schemes?category=healthcare' },
            { icon: Zap, title: 'Subsidies', desc: 'Direct benefit transfer', link: '/schemes?category=farmers' },
            { icon: Users, title: 'Pension', desc: 'Senior citizen support', link: '/schemes?category=senior-citizens' },
            { icon: TrendingUp, title: 'Business Loans', desc: 'Start your enterprise', link: '/schemes?category=entrepreneurs' },
            { icon: Home, title: 'Housing', desc: 'Affordable homes', link: '/schemes?category=housing' },
            { icon: FileText, title: 'Documents', desc: 'Caste, income certificates', link: '/about' },
            { icon: BookOpen, title: 'Skill Training', desc: 'Free certification courses', link: '/schemes?category=skill-dev' },
          ].map((service) => (
            <Link key={service.title} to={service.link}>
              <Card hover className="p-5 h-full group">
                <div className="w-10 h-10 rounded-lg bg-primary-50 text-primary-600 dark:bg-primary-900/40 dark:text-primary-400 flex items-center justify-center mb-3 group-hover:bg-primary-100 dark:group-hover:bg-primary-900/60 transition-colors">
                  <service.icon className="w-5 h-5" />
                </div>
                <h3 className="font-heading font-semibold text-slate-800 dark:text-slate-100 text-sm mb-1">{service.title}</h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">{service.desc}</p>
              </Card>
            </Link>
          ))}
        </div>
      </section>

      {/* Testimonials */}
      <section className="bg-slate-50 dark:bg-slate-950 section-padding">
        <div className="container-page">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <Badge variant="saffron" className="mb-3">Success Stories</Badge>
            <h2 className="font-heading font-bold text-3xl md:text-4xl text-slate-800 dark:text-slate-100 mb-3">
              Real Impact, Real People
            </h2>
            <p className="text-slate-500 dark:text-slate-400">See how SchemeHub is helping citizens across India discover and access government schemes.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {testimonials.map((t, i) => (
              <Card key={i} className="p-6 h-full">
                <Quote className="w-8 h-8 text-primary-200 mb-4" />
                <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed mb-5">"{t.text}"</p>
                <div className="flex items-center gap-3 pt-4 border-t border-slate-100 dark:border-slate-800">
                  <img src={t.avatar} alt={t.name} className="w-11 h-11 rounded-full object-cover" loading="lazy" />
                  <div>
                    <div className="font-heading font-semibold text-slate-800 dark:text-slate-100 text-sm">{t.name}</div>
                    <div className="text-xs text-slate-500 dark:text-slate-400">{t.role}</div>
                  </div>
                  <Badge variant="primary" size="sm" className="ml-auto">{t.scheme}</Badge>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Knowledge Base + Latest Updates */}
      <section className="container-page section-padding">
        <div className="grid lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <Badge variant="navy" className="mb-3">Knowledge Base</Badge>
            <h2 className="font-heading font-bold text-2xl md:text-3xl text-slate-800 dark:text-slate-100 mb-6">
              Government Terms, Explained Simply
            </h2>
            <div className="grid sm:grid-cols-2 gap-3">
              {knowledgeBaseArticles.map((article, i) => (
                <Card key={i} hover className="p-4 group">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <h3 className="font-medium text-slate-800 dark:text-slate-100 text-sm mb-1 group-hover:text-primary-700 dark:group-hover:text-primary-400 transition-colors">{article.title}</h3>
                      <div className="flex items-center gap-2 text-xs text-slate-400 dark:text-slate-500">
                        <Badge variant="neutral" size="sm">{article.category}</Badge>
                        <span>{article.readTime} read</span>
                      </div>
                    </div>
                    <ArrowUpRight className="w-4 h-4 text-slate-300 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors flex-shrink-0" />
                  </div>
                </Card>
              ))}
            </div>
          </div>
          <div>
            <Badge variant="warning" className="mb-3">
              <Bell className="w-3.5 h-3.5" /> Latest Updates
            </Badge>
            <h2 className="font-heading font-bold text-2xl md:text-3xl text-slate-800 dark:text-slate-100 mb-6">
              Stay Informed
            </h2>
            <Card className="divide-y divide-slate-100 dark:divide-slate-800">
              {latestUpdates.map((update, i) => (
                <div key={i} className="p-4 hover:bg-slate-50 dark:hover:bg-slate-800/60 transition-colors cursor-pointer">
                  <div className="flex items-center gap-2 mb-1.5">
                    <Badge variant={update.type === 'new' ? 'success' : update.type === 'event' ? 'saffron' : 'primary'} size="sm">
                      {update.type === 'new' ? 'New' : update.type === 'event' ? 'Event' : 'Update'}
                    </Badge>
                    <span className="text-xs text-slate-400 dark:text-slate-500">{update.date}</span>
                  </div>
                  <p className="text-sm text-slate-700 dark:text-slate-200 font-medium leading-snug">{update.title}</p>
                  <span className="text-xs text-slate-400 dark:text-slate-500">{update.category}</span>
                </div>
              ))}
            </Card>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="bg-slate-50 dark:bg-slate-950 section-padding">
        <div className="container-page max-w-3xl">
          <div className="text-center mb-10">
            <Badge variant="primary" className="mb-3">FAQ</Badge>
            <h2 className="font-heading font-bold text-3xl md:text-4xl text-slate-800 dark:text-slate-100 mb-3">
              Frequently Asked Questions
            </h2>
            <p className="text-slate-500 dark:text-slate-400">Everything you need to know about SchemeHub and how it works.</p>
          </div>
          <Accordion items={faqData} defaultOpen={0} />
        </div>
      </section>

      {/* CTA Section */}
      <section className="container-page section-padding">
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-primary-600 to-navy-800 p-10 md:p-16 text-center">
          <div className="absolute inset-0 opacity-10">
            <div className="absolute top-0 right-0 w-64 h-64 rounded-full bg-saffron-400 blur-3xl" />
            <div className="absolute bottom-0 left-0 w-80 h-80 rounded-full bg-white blur-3xl" />
          </div>
          <div className="relative">
            <h2 className="font-heading font-bold text-white text-2xl md:text-4xl mb-4">
              Ready to Discover Your Eligible Schemes?
            </h2>
            <p className="text-primary-100 text-lg mb-8 max-w-xl mx-auto">
              Join 50+ lakh citizens who have found government schemes they qualify for using SchemeHub's AI-powered platform.
            </p>
            <div className="flex flex-wrap items-center justify-center gap-3">
              <Link to="/eligibility">
                <Button variant="saffron" size="lg" className="gap-2">
                  <Sparkles className="w-5 h-5" />
                  Check My Eligibility
                </Button>
              </Link>
              <Link to="/schemes">
                <Button variant="ghost" size="lg" className="text-white hover:bg-white/10 gap-2">
                  Browse All Schemes <ArrowRight className="w-5 h-5" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
