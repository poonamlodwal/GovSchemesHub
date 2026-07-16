import { Link } from 'react-router-dom';
import { ArrowRight, ChevronRight } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Breadcrumbs } from '../components/ui/Breadcrumbs';
import { categories, schemes } from '../data/schemes';

const iconMap: Record<string, string> = {
  GraduationCap: '🎓', Heart: '❤️', Wheat: '🌾', Stethoscope: '🩺', Briefcase: '💼',
  Home: '🏠', UserRound: '🧓', BookOpen: '📚', Rocket: '🚀', Accessibility: '♿',
  Users: '👥', Wrench: '🔧',
};

const colorMap: Record<string, { bg: string; text: string; border: string }> = {
  primary: { bg: 'bg-primary-50 dark:bg-primary-500/10', text: 'text-primary-600', border: 'group-hover:border-primary-300' },
  saffron: { bg: 'bg-saffron-50', text: 'text-saffron-600', border: 'group-hover:border-saffron-300' },
  success: { bg: 'bg-success-50', text: 'text-success-600', border: 'group-hover:border-success-300' },
  error: { bg: 'bg-error-50', text: 'text-error-600', border: 'group-hover:border-error-300' },
  navy: { bg: 'bg-navy-50', text: 'text-navy-600', border: 'group-hover:border-navy-300' },
};

export function CategoriesPage() {
  return (
    <div className="bg-slate-50 dark:bg-slate-950 min-h-screen">
      <div className="container-page py-6">
        <Breadcrumbs items={[{ label: 'Home', href: '/' }, { label: 'Categories' }]} />
      </div>

      <div className="container-page pb-6">
        <Badge variant="primary" className="mb-3">Browse Categories</Badge>
        <h1 className="font-heading font-bold text-3xl md:text-4xl text-slate-800 dark:text-slate-100 mb-2">
          Explore Schemes by Category
        </h1>
        <p className="text-slate-500 dark:text-slate-400 max-w-2xl">
          Find government schemes tailored to your needs. Browse through {categories.length} categories covering all sections of society.
        </p>
      </div>

      <div className="container-page pb-12">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {categories.map((cat) => {
            const colors = colorMap[cat.color];
            const categorySchemes = schemes.filter((s) => s.category === cat.id);
            return (
              <Link key={cat.id} to={`/schemes?category=${cat.id}`}>
                <Card hover className={`p-6 h-full group border ${colors.border}`}>
                  <div className="flex items-start justify-between mb-4">
                    <div className={`w-14 h-14 rounded-2xl flex items-center justify-center text-3xl ${colors.bg}`}>
                      {iconMap[cat.icon]}
                    </div>
                    <Badge variant="primary">{cat.schemeCount} schemes</Badge>
                  </div>
                  <h3 className="font-heading font-semibold text-lg text-slate-800 dark:text-slate-100 mb-2">{cat.name}</h3>
                  <p className="text-sm text-slate-500 dark:text-slate-400 mb-4 leading-relaxed">{cat.description}</p>

                  {categorySchemes.length > 0 && (
                    <div className="space-y-1.5 mb-4">
                      {categorySchemes.slice(0, 2).map((s) => (
                        <div key={s.id} className="flex items-center gap-1.5 text-xs text-slate-500 dark:text-slate-400">
                          <ChevronRight className="w-3 h-3 text-slate-300" />
                          <span className="truncate">{s.shortTitle}</span>
                        </div>
                      ))}
                    </div>
                  )}

                  <div className={`flex items-center gap-1.5 text-sm font-medium ${colors.text} pt-3 border-t border-slate-100 dark:border-slate-800`}>
                    Browse {cat.name} schemes
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </div>
                </Card>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
}
