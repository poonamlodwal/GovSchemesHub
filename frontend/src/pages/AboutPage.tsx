import { Link } from 'react-router-dom';
import { Target, Eye, Heart, Users, ShieldCheck, Sparkles, ArrowRight, CheckCircle2, Building2, Handshake } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Card } from '../components/ui/Card';
import { Breadcrumbs } from '../components/ui/Breadcrumbs';
import { Counter } from '../components/ui/Counter';
import { Accordion } from '../components/ui/Accordion';
import { faqData, stats } from '../data/schemes';

const timeline = [
  { year: '2023', title: 'SchemeHub Conceptualized', desc: 'Vision to create a unified platform for government scheme discovery.' },
  { year: '2024', title: 'AI Engine Launched', desc: 'First AI-powered eligibility checker deployed for public use.' },
  { year: '2024', title: '50 Lakh Users', desc: 'Reached 50 lakh active users discovering schemes across India.' },
  { year: '2025', title: '1200+ Schemes', desc: 'Catalogued over 1200 schemes from 50+ ministries and departments.' },
];

const partners = [
  'Ministry of Agriculture', 'Ministry of Health', 'Ministry of Education',
  'Ministry of Finance', 'Ministry of Housing', 'Ministry of Skill Development',
  'NITI Aayog', 'Digital India', 'MyGov', 'National e-Governance Division',
];

export function AboutPage() {
  return (
    <div className="bg-slate-50 dark:bg-slate-950 min-h-screen">
      <div className="container-page py-6">
        <Breadcrumbs items={[{ label: 'Home', href: '/' }, { label: 'About' }]} />
      </div>

      {/* Hero */}
      <section className="container-page pb-12">
        <div className="max-w-3xl">
          <Badge variant="primary" className="mb-3">About SchemeHub</Badge>
          <h1 className="font-heading font-bold text-3xl md:text-5xl text-slate-800 dark:text-slate-100 mb-4 text-balance">
            Bridging the Gap Between Citizens and Government Services
          </h1>
          <p className="text-lg text-slate-500 dark:text-slate-400 leading-relaxed">
            SchemeHub is an AI-powered platform that helps Indian citizens discover government schemes, scholarships, subsidies, and services they're eligible for, making governance more transparent, accessible, and inclusive.
          </p>
        </div>
      </section>

      {/* Mission & Vision */}
      <section className="container-page section-padding">
        <div className="grid md:grid-cols-2 gap-6">
          <Card className="p-8">
            <div className="w-14 h-14 rounded-2xl bg-primary-100 text-primary-600 flex items-center justify-center mb-5">
              <Target className="w-7 h-7" />
            </div>
            <h2 className="font-heading font-bold text-xl text-slate-800 dark:text-slate-100 mb-3">Our Mission</h2>
            <p className="text-slate-600 dark:text-slate-200 leading-relaxed">
              To ensure every Indian citizen can easily discover and access government schemes they're eligible for — eliminating the information gap that prevents millions from receiving the benefits they deserve.
            </p>
          </Card>
          <Card className="p-8">
            <div className="w-14 h-14 rounded-2xl bg-saffron-100 text-saffron-600 flex items-center justify-center mb-5">
              <Eye className="w-7 h-7" />
            </div>
            <h2 className="font-heading font-bold text-xl text-slate-800 dark:text-slate-100 mb-3">Our Vision</h2>
            <p className="text-slate-600 dark:text-slate-200 leading-relaxed">
              A future where accessing government services is as simple as searching the internet — where no eligible citizen misses out on benefits because they didn't know a scheme existed.
            </p>
          </Card>
        </div>
      </section>

      {/* Impact Stats */}
      <section className="bg-gradient-to-br from-navy-900 to-primary-800 relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-10 left-1/4 w-64 h-64 rounded-full bg-saffron-400 blur-3xl" />
        </div>
        <div className="container-page relative py-16">
          <div className="text-center mb-10">
            <Badge variant="saffron" className="mb-3 bg-saffron-500/20 text-saffron-300 border border-saffron-400/30">Our Impact</Badge>
            <h2 className="font-heading font-bold text-3xl md:text-4xl text-white">Making a Real Difference</h2>
          </div>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {stats.map((stat, i) => (
              <div key={i} className="text-center">
                <div className="text-4xl lg:text-5xl font-heading font-bold text-white mb-1">
                  <Counter value={stat.value} suffix={stat.suffix} />
                </div>
                <div className="text-sm text-primary-200">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How SchemeHub Works */}
      <section className="container-page section-padding">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <Badge variant="navy" className="mb-3">How It Works</Badge>
          <h2 className="font-heading font-bold text-3xl md:text-4xl text-slate-800 dark:text-slate-100 mb-3">
            A Simple 3-Step Process
          </h2>
        </div>
        <div className="grid md:grid-cols-3 gap-6">
          {[
            { icon: Users, title: 'Tell Us About You', desc: 'Answer a few simple questions about your background, income, occupation, and location.', color: 'primary' },
            { icon: Sparkles, title: 'AI Matches You', desc: 'Our AI engine analyzes your profile and matches you with eligible schemes using official criteria.', color: 'saffron' },
            { icon: CheckCircle2, title: 'Apply with Confidence', desc: 'Get step-by-step guidance, document checklists, and direct links to official application portals.', color: 'success' },
          ].map((item, i) => (
            <Card key={i} className="p-8 text-center card-hover">
              <div className={`w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-5 ${
                item.color === 'primary' ? 'bg-primary-100 text-primary-600' :
                item.color === 'saffron' ? 'bg-saffron-100 text-saffron-600' : 'bg-success-100 text-success-600'
              }`}>
                <item.icon className="w-8 h-8" />
              </div>
              <h3 className="font-heading font-semibold text-lg text-slate-800 dark:text-slate-100 mb-2">{item.title}</h3>
              <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">{item.desc}</p>
            </Card>
          ))}
        </div>
      </section>

      {/* Timeline */}
      <section className="bg-slate-50 dark:bg-slate-950 section-padding">
        <div className="container-page max-w-3xl">
          <div className="text-center mb-12">
            <Badge variant="primary" className="mb-3">Our Journey</Badge>
            <h2 className="font-heading font-bold text-3xl md:text-4xl text-slate-800 dark:text-slate-100">The SchemeHub Timeline</h2>
          </div>
          <div className="relative">
            <div className="absolute left-4 md:left-1/2 top-0 bottom-0 w-0.5 bg-slate-200 md:-translate-x-1/2" />
            <div className="space-y-8">
            {timeline.map((item, i) => (
              <div key={i} className={`relative flex gap-6 ${i % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse'}`}>
                <div className="absolute left-4 md:left-1/2 w-3 h-3 rounded-full bg-primary-600 ring-4 ring-white md:-translate-x-1/2 mt-2" />
                <div className={`flex-1 pl-12 md:pl-0 ${i % 2 === 0 ? 'md:pr-12 md:text-right' : 'md:pl-12'}`}>
                  <Card className="p-5 inline-block w-full">
                    <Badge variant="primary" className="mb-2">{item.year}</Badge>
                    <h3 className="font-heading font-semibold text-slate-800 dark:text-slate-100 mb-1">{item.title}</h3>
                    <p className="text-sm text-slate-500 dark:text-slate-400">{item.desc}</p>
                  </Card>
                </div>
                <div className="hidden md:block flex-1" />
              </div>
            ))}
            </div>
          </div>
        </div>
      </section>

      {/* Values */}
      <section className="container-page section-padding">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <Badge variant="success" className="mb-3">Our Values</Badge>
          <h2 className="font-heading font-bold text-3xl md:text-4xl text-slate-800 dark:text-slate-100">What We Stand For</h2>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {[
            { icon: ShieldCheck, title: 'Trust & Transparency', desc: 'Accurate, verified information from official government sources.' },
            { icon: Heart, title: 'Citizen-First', desc: 'Designed for simplicity and accessibility for all citizens.' },
            { icon: Sparkles, title: 'Innovation', desc: 'AI-powered solutions for complex government service discovery.' },
            { icon: Handshake, title: 'Inclusivity', desc: 'Serving every section of society — rural, urban, and marginalized.' },
          ].map((value, i) => (
            <Card key={i} className="p-6 card-hover">
              <div className="w-12 h-12 rounded-xl bg-primary-50 dark:bg-primary-500/10 text-primary-600 flex items-center justify-center mb-4">
                <value.icon className="w-6 h-6" />
              </div>
              <h3 className="font-heading font-semibold text-slate-800 dark:text-slate-100 mb-2">{value.title}</h3>
              <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">{value.desc}</p>
            </Card>
          ))}
        </div>
      </section>

      {/* Partners */}
      <section className="bg-slate-50 dark:bg-slate-950 section-padding">
        <div className="container-page">
          <div className="text-center mb-12">
            <Badge variant="navy" className="mb-3">
              <Building2 className="w-3.5 h-3.5" /> Partners
            </Badge>
            <h2 className="font-heading font-bold text-3xl md:text-4xl text-slate-800 dark:text-slate-100">Government Partners</h2>
            <p className="text-slate-500 dark:text-slate-400 mt-2 max-w-xl mx-auto">We work with government ministries and departments to ensure accurate, up-to-date scheme information.</p>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
            {partners.map((partner) => (
              <Card key={partner} className="p-4 text-center hover:bg-primary-50/50 dark:hover:bg-primary-500/10 transition-colors">
                <div className="w-10 h-10 rounded-lg bg-primary-100 text-primary-600 flex items-center justify-center mx-auto mb-2">
                  <Building2 className="w-5 h-5" />
                </div>
                <span className="text-xs font-medium text-slate-600 dark:text-slate-200">{partner}</span>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="container-page section-padding max-w-3xl">
        <div className="text-center mb-10">
          <Badge variant="primary" className="mb-3">FAQ</Badge>
          <h2 className="font-heading font-bold text-3xl md:text-4xl text-slate-800 dark:text-slate-100">Frequently Asked Questions</h2>
        </div>
        <Accordion items={faqData} defaultOpen={0} />
      </section>

      {/* CTA */}
      <section className="container-page pb-16">
        <div className="rounded-2xl bg-gradient-to-br from-primary-600 to-navy-800 p-10 md:p-14 text-center">
          <h2 className="font-heading font-bold text-white text-2xl md:text-3xl mb-4">
            Ready to Discover Your Eligible Schemes?
          </h2>
          <p className="text-primary-100 mb-6 max-w-lg mx-auto">
            Join millions of citizens who have found government benefits they qualify for.
          </p>
          <Link to="/eligibility">
            <Button variant="saffron" size="lg" className="gap-2">
              <Sparkles className="w-5 h-5" /> Check My Eligibility <ArrowRight className="w-5 h-5" />
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
}
