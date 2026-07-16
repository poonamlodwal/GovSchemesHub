import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, ArrowRight, ArrowLeft, CheckCircle2, RefreshCw, Calendar, User, Wallet, Briefcase, GraduationCap, MapPin, Users, HeartHandshake, Award, TrendingUp } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Card } from '../components/ui/Card';
import { Breadcrumbs } from '../components/ui/Breadcrumbs';
import { SchemeCard } from '../components/SchemeCard';
import { eligibilityQuestions, schemes, type Scheme } from '../data/schemes';

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  Calendar, User, Wallet, Briefcase, GraduationCap, MapPin, Users, HeartHandshake,
};

export function EligibilityCheckerPage() {
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string | string[]>>({});
  const [showResults, setShowResults] = useState(false);
  const [matchedSchemes, setMatchedSchemes] = useState<(Scheme & { matchScore: number })[]>([]);

  const question = eligibilityQuestions[currentStep];
  const progress = ((currentStep + 1) / eligibilityQuestions.length) * 100;
  const isMulti = question?.type === 'multi-choice';

  const handleAnswer = (value: string) => {
    if (isMulti) {
      const current = (answers[question.id] as string[]) || [];
      if (value === 'None of the above') {
        setAnswers({ ...answers, [question.id]: ['None of the above'] });
      } else {
        const filtered = current.filter((v) => v !== 'None of the above');
        setAnswers({
          ...answers,
          [question.id]: filtered.includes(value)
            ? filtered.filter((v) => v !== value)
            : [...filtered, value],
        });
      }
    } else {
      setAnswers({ ...answers, [question.id]: value });
    }
  };

  const isAnswered = isMulti
    ? (answers[question.id] as string[])?.length > 0
    : !!answers[question.id];

  const handleNext = () => {
    if (currentStep < eligibilityQuestions.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      calculateMatches();
    }
  };

  const calculateMatches = () => {
    const occupation = answers.occupation as string;
    const income = answers.income as string;
    const category = answers.category as string;
    const special = (answers.special as string[]) || [];

    const scored = schemes.map((scheme) => {
      let score = 50;
      const reasons: string[] = [];

      if (occupation === 'Farmer' && scheme.category === 'farmers') { score += 30; reasons.push('Farmer'); }
      if (occupation === 'Student' && (scheme.category === 'students' || scheme.category === 'education')) { score += 30; reasons.push('Student'); }
      if (occupation === 'Business Owner' && scheme.category === 'entrepreneurs') { score += 25; reasons.push('Business owner'); }
      if (occupation === 'Retired' && scheme.category === 'senior-citizens') { score += 30; reasons.push('Senior citizen'); }
      if ((answers.gender === 'Female') && scheme.category === 'women') { score += 25; reasons.push('Women'); }

      if (income === 'Below ₹1 lakh' || income === '₹1-3 lakh') { score += 15; }
      if (income === '₹3-6 lakh') { score += 8; }

      if (category === 'SC' || category === 'ST' || category === 'OBC' || category === 'Minority') {
        if (scheme.tags.some((t) => t.includes('SC') || t.includes('ST') || t.includes('Minority'))) {
          score += 20;
        }
      }

      if (special.includes('Person with Disability') && scheme.category === 'disability') { score += 25; }
      if (special.includes('Senior Citizen (60+)') && scheme.category === 'senior-citizens') { score += 25; }
      if (special.includes('Widow') || special.includes('Single Woman')) {
        if (scheme.category === 'women') { score += 15; }
      }

      score = Math.min(score, 98);
      return { ...scheme, matchScore: score };
    });

    const matches = scored.filter((s) => s.matchScore >= 60).sort((a, b) => b.matchScore - a.matchScore);
    setMatchedSchemes(matches);
    setShowResults(true);
  };

  const handleRestart = () => {
    setCurrentStep(0);
    setAnswers({});
    setShowResults(false);
    setMatchedSchemes([]);
  };

  if (showResults) {
    return (
      <div className="bg-slate-50 dark:bg-slate-950 min-h-screen">
        <div className="container-page py-6">
          <Breadcrumbs items={[{ label: 'Home', href: '/' }, { label: 'Eligibility Results' }]} />
        </div>

        <div className="container-page pb-12">
          <div className="text-center max-w-2xl mx-auto mb-10">
            <div className="w-16 h-16 rounded-full bg-success-100 flex items-center justify-center mx-auto mb-4">
              <CheckCircle2 className="w-8 h-8 text-success-600" />
            </div>
            <h1 className="font-heading font-bold text-3xl md:text-4xl text-slate-800 dark:text-slate-100 mb-3">
              Your Eligibility Results
            </h1>
            <p className="text-slate-500 dark:text-slate-400">
              Based on your responses, we found <span className="font-bold text-primary-600">{matchedSchemes.length} schemes</span> you may be eligible for.
            </p>
          </div>

          {matchedSchemes.length > 0 ? (
            <>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                {[
                  { label: 'Schemes Matched', value: matchedSchemes.length, icon: Award, color: 'primary' },
                  { label: 'High Confidence', value: matchedSchemes.filter((s) => s.matchScore >= 80).length, icon: TrendingUp, color: 'success' },
                  { label: 'Medium Confidence', value: matchedSchemes.filter((s) => s.matchScore >= 65 && s.matchScore < 80).length, icon: Sparkles, color: 'saffron' },
                  { label: 'Categories', value: new Set(matchedSchemes.map((s) => s.category)).size, icon: Briefcase, color: 'navy' },
                ].map((stat) => (
                  <Card key={stat.label} className="p-4 text-center">
                    <stat.icon className={`w-6 h-6 mx-auto mb-2 ${
                      stat.color === 'primary' ? 'text-primary-600' :
                      stat.color === 'success' ? 'text-success-600' :
                      stat.color === 'saffron' ? 'text-saffron-600' : 'text-navy-600'
                    }`} />
                    <div className="text-2xl font-heading font-bold text-slate-800 dark:text-slate-100">{stat.value}</div>
                    <div className="text-xs text-slate-500 dark:text-slate-400">{stat.label}</div>
                  </Card>
                ))}
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
                {matchedSchemes.map((scheme) => (
                  <SchemeCard key={scheme.id} scheme={scheme} showMatch />
                ))}
              </div>
            </>
          ) : (
            <Card className="p-12 text-center max-w-lg mx-auto">
              <p className="text-slate-500 dark:text-slate-400 mb-4">No high-confidence matches found. Try adjusting your answers or browse all schemes manually.</p>
              <Link to="/schemes"><Button>Browse All Schemes</Button></Link>
            </Card>
          )}

          <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
            <Button variant="outline" className="gap-2" onClick={handleRestart}>
              <RefreshCw className="w-4 h-4" /> Retake Assessment
            </Button>
            <Link to="/schemes">
              <Button variant="ghost" className="gap-2 border border-slate-200 dark:border-slate-800">
                Browse All Schemes <ArrowRight className="w-4 h-4" />
              </Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const Icon = iconMap[question.icon] || Sparkles;

  return (
    <div className="bg-slate-50 dark:bg-slate-950 min-h-screen">
      <div className="container-page py-6">
        <Breadcrumbs items={[{ label: 'Home', href: '/' }, { label: 'Eligibility Checker' }]} />
      </div>

      <div className="container-page pb-12">
        <div className="max-w-2xl mx-auto">
          <div className="text-center mb-8">
            <Badge variant="saffron" className="mb-3">
              <Sparkles className="w-3.5 h-3.5" /> AI-Powered
            </Badge>
            <h1 className="font-heading font-bold text-3xl md:text-4xl text-slate-800 dark:text-slate-100 mb-2">
              AI Eligibility Checker
            </h1>
            <p className="text-slate-500 dark:text-slate-400">Answer a few questions to discover schemes you're eligible for.</p>
          </div>

          {/* Progress Bar */}
          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-slate-600 dark:text-slate-300">
                Question {currentStep + 1} of {eligibilityQuestions.length}
              </span>
              <span className="text-sm text-slate-400 dark:text-slate-500">{Math.round(progress)}% complete</span>
            </div>
            <div className="w-full h-2 rounded-full bg-slate-200 overflow-hidden">
              <div
                className="h-full rounded-full bg-gradient-to-r from-primary-500 to-primary-600 transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>

          {/* Question Card */}
          <Card className="p-8 animate-fade-in">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 rounded-xl bg-primary-50 dark:bg-primary-500/10 text-primary-600 flex items-center justify-center">
                <Icon className="w-6 h-6" />
              </div>
              <h2 className="font-heading font-semibold text-xl text-slate-800 dark:text-slate-100">{question.question}</h2>
            </div>

            {question.type === 'number' ? (
              <input
                type="number"
                value={(answers[question.id] as string) || ''}
                onChange={(e) => handleAnswer(e.target.value)}
                placeholder={question.placeholder}
                className="w-full px-4 py-3 rounded-xl border border-slate-300 text-lg text-slate-800 dark:text-slate-100 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 transition-all outline-none"
                autoFocus
              />
            ) : (
              <div className={`grid ${isMulti ? 'grid-cols-1 sm:grid-cols-2' : 'grid-cols-1 sm:grid-cols-2'} gap-2`}>
                {question.options?.map((option) => {
                  const isSelected = isMulti
                    ? (answers[question.id] as string[])?.includes(option)
                    : answers[question.id] === option;
                  return (
                    <button
                      key={option}
                      onClick={() => handleAnswer(option)}
                      className={`flex items-center justify-between gap-2 px-4 py-3.5 rounded-xl border-2 text-left text-sm font-medium transition-all ${
                        isSelected
                          ? 'border-primary-500 bg-primary-50 dark:bg-primary-500/10 text-primary-700'
                          : 'border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 hover:border-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800/60'
                      }`}
                    >
                      <span>{option}</span>
                      {isSelected && <CheckCircle2 className="w-5 h-5 text-primary-600 flex-shrink-0" />}
                    </button>
                  );
                })}
              </div>
            )}

            <div className="flex items-center justify-between mt-8 pt-6 border-t border-slate-100 dark:border-slate-800">
              <button
                onClick={() => currentStep > 0 && setCurrentStep(currentStep - 1)}
                disabled={currentStep === 0}
                className="flex items-center gap-1.5 text-sm text-slate-500 dark:text-slate-400 hover:text-slate-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
              >
                <ArrowLeft className="w-4 h-4" /> Back
              </button>
              <Button
                onClick={handleNext}
                disabled={!isAnswered}
                className="gap-2"
              >
                {currentStep === eligibilityQuestions.length - 1 ? 'See Results' : 'Next'}
                <ArrowRight className="w-4 h-4" />
              </Button>
            </div>
          </Card>

          <p className="text-center text-xs text-slate-400 dark:text-slate-500 mt-4">
            Your answers are processed securely and never shared. Results are indicative — always verify on the official portal.
          </p>
        </div>
      </div>
    </div>
  );
}
