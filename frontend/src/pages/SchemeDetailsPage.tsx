import { useParams, Link } from 'react-router-dom';
import { useState } from 'react';
import {
  Building2, Calendar, Users, Bookmark, Share2, ExternalLink, CheckCircle2,
  FileText, Gift, ListChecks, HelpCircle, ChevronRight, ArrowLeft, Sparkles, ShieldCheck, Clock
} from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Card } from '../components/ui/Card';
import { Accordion } from '../components/ui/Accordion';
import { Breadcrumbs } from '../components/ui/Breadcrumbs';
import { SchemeCard } from '../components/SchemeCard';
import { showToast } from '../components/ui/Toast';
import { schemes, categories } from '../data/schemes';

const statusConfig = {
  open: { variant: 'success' as const, label: 'Open', icon: CheckCircle2 },
  upcoming: { variant: 'warning' as const, label: 'Upcoming', icon: Clock },
  closed: { variant: 'error' as const, label: 'Closed', icon: Clock },
};

const tabs = [
  { id: 'overview', label: 'Overview', icon: FileText },
  { id: 'eligibility', label: 'Eligibility', icon: CheckCircle2 },
  { id: 'documents', label: 'Documents', icon: ListChecks },
  { id: 'benefits', label: 'Benefits', icon: Gift },
  { id: 'process', label: 'How to Apply', icon: ListChecks },
  { id: 'faqs', label: 'FAQs', icon: HelpCircle },
];

export function SchemeDetailsPage() {
  const { id } = useParams();
  const [activeTab, setActiveTab] = useState('overview');
  const [bookmarked, setBookmarked] = useState(false);

  const scheme = schemes.find((s) => s.id === id);

  if (!scheme) {
    return (
      <div className="container-page py-20 text-center">
        <h1 className="font-heading font-bold text-2xl text-slate-800 dark:text-slate-100 mb-3">Scheme Not Found</h1>
        <p className="text-slate-500 dark:text-slate-400 mb-6">The scheme you're looking for doesn't exist or has been removed.</p>
        <Link to="/schemes"><Button>Browse All Schemes</Button></Link>
      </div>
    );
  }

  const status = statusConfig[scheme.status];
  const category = categories.find((c) => c.id === scheme.category);
  const similarSchemes = schemes.filter((s) => s.category === scheme.category && s.id !== scheme.id).slice(0, 3);

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({ title: scheme.title, url: window.location.href });
    } else {
      navigator.clipboard.writeText(window.location.href);
      showToast('success', 'Link copied to clipboard!');
    }
  };

  return (
    <div className="bg-slate-50 dark:bg-slate-950 min-h-screen">
      {/* Hero Section */}
      <section className="gradient-hero relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-10 right-20 w-72 h-72 rounded-full bg-saffron-300 blur-3xl" />
        </div>
        <div className="container-page relative py-10">
          <div className="mb-6">
            <Breadcrumbs
              items={[
                { label: 'Home', href: '/' },
                { label: 'Schemes', href: '/schemes' },
                { label: scheme.shortTitle },
              ]}
            />
          </div>
          <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6">
            <div className="max-w-3xl">
              <div className="flex flex-wrap gap-2 mb-4">
                <Badge variant={status.variant} dot>{status.label}</Badge>
                <Badge variant="primary">{category?.name || scheme.category}</Badge>
                {scheme.tags.map((tag) => (
                  <Badge key={tag} variant="neutral">{tag}</Badge>
                ))}
              </div>
              <h1 className="font-heading font-bold text-white text-3xl md:text-4xl mb-3 leading-tight">
                {scheme.title}
              </h1>
              <p className="text-primary-100 text-lg leading-relaxed">{scheme.description}</p>
            </div>
            <div className="flex gap-2 flex-shrink-0">
              <Button
                variant={bookmarked ? 'primary' : 'ghost'}
                className="text-white hover:bg-white/10 border border-white/20 gap-2"
                onClick={() => {
                  setBookmarked(!bookmarked);
                  showToast(bookmarked ? 'info' : 'success', bookmarked ? 'Removed from saved' : 'Saved to dashboard');
                }}
              >
                <Bookmark className={`w-4 h-4 ${bookmarked ? 'fill-current' : ''}`} />
                {bookmarked ? 'Saved' : 'Save'}
              </Button>
              <Button variant="ghost" className="text-white hover:bg-white/10 border border-white/20 gap-2" onClick={handleShare}>
                <Share2 className="w-4 h-4" /> Share
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Quick Info Bar */}
      <section className="border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
        <div className="container-page py-5">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { icon: Building2, label: 'Ministry', value: scheme.ministry },
              { icon: Users, label: 'Beneficiaries', value: scheme.beneficiaries },
              { icon: Calendar, label: 'Deadline', value: scheme.deadline },
              { icon: ShieldCheck, label: 'Status', value: status.label },
            ].map((item) => (
              <div key={item.label} className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-lg bg-primary-50 text-primary-600 flex items-center justify-center flex-shrink-0">
                  <item.icon className="w-5 h-5" />
                </div>
                <div className="min-w-0">
                  <div className="text-xs text-slate-400 dark:text-slate-500 mb-0.5">{item.label}</div>
                  <div className="text-sm font-medium text-slate-700 dark:text-slate-200 truncate">{item.value}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <div className="container-page py-8">
        <div className="grid lg:grid-cols-[1fr_320px] gap-8">
          {/* Main Content */}
          <div>
            {/* Tabs */}
            <div className="flex gap-1 overflow-x-auto scrollbar-hide border-b border-slate-200 dark:border-slate-800 mb-6">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-all whitespace-nowrap ${
                    activeTab === tab.id
                      ? 'border-primary-600 text-primary-700'
                      : 'border-transparent text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200'
                  }`}
                >
                  <tab.icon className="w-4 h-4" />
                  {tab.label}
                </button>
              ))}
            </div>

            {/* Tab Content */}
            <div className="animate-fade-in">
              {activeTab === 'overview' && (
                <Card className="p-6">
                  <h2 className="font-heading font-semibold text-xl text-slate-800 dark:text-slate-100 mb-4">Scheme Overview</h2>
                  <p className="text-slate-600 dark:text-slate-300 leading-relaxed mb-6">{scheme.description}</p>
                  <div className="grid sm:grid-cols-2 gap-4">
                    <div className="bg-slate-50 dark:bg-slate-950 rounded-xl p-4">
                      <div className="text-xs text-slate-400 dark:text-slate-500 mb-1">Ministry</div>
                      <div className="text-sm font-medium text-slate-700 dark:text-slate-200">{scheme.ministry}</div>
                    </div>
                    <div className="bg-slate-50 dark:bg-slate-950 rounded-xl p-4">
                      <div className="text-xs text-slate-400 dark:text-slate-500 mb-1">Department</div>
                      <div className="text-sm font-medium text-slate-700 dark:text-slate-200">{scheme.department}</div>
                    </div>
                  </div>
                </Card>
              )}

              {activeTab === 'eligibility' && (
                <Card className="p-6">
                  <h2 className="font-heading font-semibold text-xl text-slate-800 dark:text-slate-100 mb-4">Eligibility Criteria</h2>
                  <div className="space-y-3">
                    {scheme.eligibility.map((criteria, i) => (
                      <div key={i} className="flex items-start gap-3 p-3 bg-success-50 rounded-lg">
                        <CheckCircle2 className="w-5 h-5 text-success-600 flex-shrink-0 mt-0.5" />
                        <span className="text-sm text-slate-700 dark:text-slate-200">{criteria}</span>
                      </div>
                    ))}
                  </div>
                  <div className="mt-6 p-4 bg-primary-50 rounded-xl border border-primary-100">
                    <div className="flex items-center gap-2 mb-2">
                      <Sparkles className="w-4 h-4 text-primary-600" />
                      <span className="text-sm font-medium text-primary-700">Not sure if you're eligible?</span>
                    </div>
                    <p className="text-sm text-slate-600 dark:text-slate-300 mb-3">Use our AI Eligibility Checker to find out instantly.</p>
                    <Link to="/eligibility">
                      <Button size="sm" className="gap-1.5">
                        <Sparkles className="w-4 h-4" /> Check My Eligibility
                      </Button>
                    </Link>
                  </div>
                </Card>
              )}

              {activeTab === 'documents' && (
                <Card className="p-6">
                  <h2 className="font-heading font-semibold text-xl text-slate-800 dark:text-slate-100 mb-4">Required Documents</h2>
                  <div className="space-y-2">
                    {scheme.documents.map((doc, i) => (
                      <div key={i} className="flex items-center gap-3 p-3 border border-slate-200 dark:border-slate-800 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800/60 transition-colors">
                        <div className="w-9 h-9 rounded-lg bg-primary-50 text-primary-600 flex items-center justify-center flex-shrink-0">
                          <FileText className="w-4 h-4" />
                        </div>
                        <span className="text-sm text-slate-700 dark:text-slate-200">{doc}</span>
                        <CheckCircle2 className="w-4 h-4 text-success-500 ml-auto flex-shrink-0" />
                      </div>
                    ))}
                  </div>
                </Card>
              )}

              {activeTab === 'benefits' && (
                <Card className="p-6">
                  <h2 className="font-heading font-semibold text-xl text-slate-800 dark:text-slate-100 mb-4">Scheme Benefits</h2>
                  <div className="p-5 bg-gradient-to-br from-saffron-50 to-saffron-100 rounded-xl border border-saffron-200">
                    <div className="flex items-center gap-3 mb-3">
                      <div className="w-12 h-12 rounded-xl bg-saffron-500 text-white flex items-center justify-center">
                        <Gift className="w-6 h-6" />
                      </div>
                      <h3 className="font-heading font-semibold text-slate-800 dark:text-slate-100">Key Benefit</h3>
                    </div>
                    <p className="text-slate-700 dark:text-slate-200 text-lg font-medium">{scheme.benefits}</p>
                  </div>
                </Card>
              )}

              {activeTab === 'process' && (
                <Card className="p-6">
                  <h2 className="font-heading font-semibold text-xl text-slate-800 dark:text-slate-100 mb-6">Application Process</h2>
                  <div className="relative">
                    {scheme.applicationProcess.map((step, i) => (
                      <div key={i} className="flex gap-4 pb-6 last:pb-0">
                        <div className="flex flex-col items-center">
                          <div className="w-9 h-9 rounded-full bg-primary-600 text-white flex items-center justify-center text-sm font-bold flex-shrink-0">
                            {i + 1}
                          </div>
                          {i < scheme.applicationProcess.length - 1 && (
                            <div className="w-0.5 flex-1 bg-slate-200 mt-2" />
                          )}
                        </div>
                        <div className="pt-1">
                          <p className="text-sm text-slate-700 dark:text-slate-200 leading-relaxed">{step}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                  <a href={scheme.officialLink} target="_blank" rel="noopener noreferrer" className="mt-6 inline-block">
                    <Button className="gap-2">
                      <ExternalLink className="w-4 h-4" /> Visit Official Portal
                    </Button>
                  </a>
                </Card>
              )}

              {activeTab === 'faqs' && (
                <Card className="p-6">
                  <h2 className="font-heading font-semibold text-xl text-slate-800 dark:text-slate-100 mb-4">Frequently Asked Questions</h2>
                  <Accordion items={scheme.faqs} defaultOpen={0} />
                </Card>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <aside className="space-y-4">
            <Card className="p-5 lg:sticky lg:top-20">
              <h3 className="font-heading font-semibold text-slate-800 dark:text-slate-100 mb-4">Quick Actions</h3>
              <div className="space-y-2">
                <Link to="/eligibility" className="block">
                  <Button fullWidth className="gap-2 mb-2">
                    <Sparkles className="w-4 h-4" /> Check Eligibility
                  </Button>
                </Link>
                <a href={scheme.officialLink} target="_blank" rel="noopener noreferrer" className="block">
                  <Button variant="outline" fullWidth className="gap-2 mb-2">
                    <ExternalLink className="w-4 h-4" /> Official Portal
                  </Button>
                </a>
                <Button
                  variant="ghost"
                  fullWidth
                  className="gap-2 border border-slate-200 dark:border-slate-800"
                  onClick={() => {
                    setBookmarked(!bookmarked);
                    showToast(bookmarked ? 'info' : 'success', bookmarked ? 'Removed from saved' : 'Saved to dashboard');
                  }}
                >
                  <Bookmark className={`w-4 h-4 ${bookmarked ? 'fill-current text-primary-600' : ''}`} />
                  {bookmarked ? 'Saved to Dashboard' : 'Save Scheme'}
                </Button>
              </div>

              <div className="mt-5 pt-5 border-t border-slate-100 dark:border-slate-800 space-y-3">
                <div>
                  <div className="text-xs text-slate-400 dark:text-slate-500 mb-1">Ministry</div>
                  <div className="text-sm text-slate-700 dark:text-slate-200">{scheme.ministry}</div>
                </div>
                <div>
                  <div className="text-xs text-slate-400 dark:text-slate-500 mb-1">Department</div>
                  <div className="text-sm text-slate-700 dark:text-slate-200">{scheme.department}</div>
                </div>
                <div>
                  <div className="text-xs text-slate-400 dark:text-slate-500 mb-1">Beneficiaries</div>
                  <div className="text-sm text-slate-700 dark:text-slate-200">{scheme.beneficiaries}</div>
                </div>
                <div>
                  <div className="text-xs text-slate-400 dark:text-slate-500 mb-1">Deadline</div>
                  <div className="text-sm text-slate-700 dark:text-slate-200">{scheme.deadline}</div>
                </div>
              </div>
            </Card>
          </aside>
        </div>
      </div>

      {/* Similar Schemes */}
      {similarSchemes.length > 0 && (
        <section className="container-page pb-12">
          <div className="flex items-end justify-between mb-6">
            <h2 className="font-heading font-bold text-2xl text-slate-800 dark:text-slate-100">Similar Schemes</h2>
            <Link to={`/schemes?category=${scheme.category}`}>
              <Button variant="outline" size="sm" className="gap-1.5">
                View All <ChevronRight className="w-4 h-4" />
              </Button>
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {similarSchemes.map((s) => (
              <SchemeCard key={s.id} scheme={s} />
            ))}
          </div>
        </section>
      )}

      <div className="container-page pb-8">
        <Link to="/schemes" className="inline-flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400 hover:text-primary-600 transition-colors">
          <ArrowLeft className="w-4 h-4" /> Back to Browse Schemes
        </Link>
      </div>
    </div>
  );
}
