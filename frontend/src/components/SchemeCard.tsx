import { Link } from 'react-router-dom';
import { Bookmark, Building2, Calendar, Users } from 'lucide-react';
import type { Scheme } from '../data/schemes';
import { Badge } from './ui/Badge';
import { Card } from './ui/Card';
import { showToast } from './ui/Toast';

const statusConfig = {
  open: { variant: 'success' as const, label: 'Open' },
  upcoming: { variant: 'warning' as const, label: 'Upcoming' },
  closed: { variant: 'error' as const, label: 'Closed' },
};

export function SchemeCard({ scheme, showMatch = false }: { scheme: Scheme; showMatch?: boolean }) {
  const status = statusConfig[scheme.status];

  const handleBookmark = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    showToast('success', `${scheme.shortTitle} saved to your dashboard`);
  };

  return (
    <Link to={`/schemes/${scheme.id}`} className="block h-full">
      <Card hover className="h-full flex flex-col p-5">
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex flex-wrap gap-1.5">
            <Badge variant={status.variant} dot>{status.label}</Badge>
            <Badge variant="primary">{scheme.tags[0]}</Badge>
          </div>
          <button
            onClick={handleBookmark}
            className="p-1.5 rounded-lg text-slate-400 dark:text-slate-500 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-500/10 transition-all flex-shrink-0"
            aria-label="Bookmark"
          >
            <Bookmark className="w-4 h-4" />
          </button>
        </div>

        <h3 className="font-heading font-semibold text-slate-800 dark:text-slate-100 text-base leading-snug mb-2 line-clamp-2">
          {scheme.title}
        </h3>
        <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed mb-4 line-clamp-2 flex-1">
          {scheme.description}
        </p>

        <div className="space-y-2 pt-3 border-t border-slate-100 dark:border-slate-800">
          <div className="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400">
            <Building2 className="w-3.5 h-3.5 text-slate-400 dark:text-slate-500" />
            <span className="truncate">{scheme.ministry}</span>
          </div>
          <div className="flex items-center justify-between gap-2 text-xs text-slate-500">
            <div className="flex items-center gap-1.5">
              <Users className="w-3.5 h-3.5 text-slate-400 dark:text-slate-500" />
              <span>{scheme.beneficiaries}</span>
            </div>
            <div className="flex items-center gap-1.5">
              <Calendar className="w-3.5 h-3.5 text-slate-400 dark:text-slate-500" />
              <span>{scheme.deadline}</span>
            </div>
          </div>
        </div>

        {showMatch && scheme.matchScore && (
          <div className="mt-3 pt-3 border-t border-slate-100 dark:border-slate-800">
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs font-medium text-slate-600 dark:text-slate-300">Eligibility Match</span>
              <span className="text-xs font-bold text-success-600">{scheme.matchScore}%</span>
            </div>
            <div className="w-full h-1.5 rounded-full bg-slate-100 dark:bg-slate-800 overflow-hidden">
              <div
                className="h-full rounded-full bg-gradient-to-r from-success-400 to-success-600 transition-all duration-1000"
                style={{ width: `${scheme.matchScore}%` }}
              />
            </div>
          </div>
        )}
      </Card>
    </Link>
  );
}
