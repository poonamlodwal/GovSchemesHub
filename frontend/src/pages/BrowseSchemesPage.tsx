import { useMemo, useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Search, SlidersHorizontal, X, ChevronLeft, ChevronRight, Grid3x3, List, Bookmark, Calendar, Building2, Users, ArrowRight } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Card } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { SchemeCard } from '../components/SchemeCard';
import { Breadcrumbs } from '../components/ui/Breadcrumbs';
import { schemes, categories } from '../data/schemes';

const sortOptions = [
  { value: 'relevance', label: 'Most Relevant' },
  { value: 'deadline', label: 'Deadline (Soonest)' },
  { value: 'title', label: 'Title (A-Z)' },
  { value: 'beneficiaries', label: 'Most Beneficiaries' },
];

const statusFilters = [
  { value: 'open', label: 'Open' },
  { value: 'upcoming', label: 'Upcoming' },
  { value: 'closed', label: 'Closed' },
];

const PAGE_SIZE = 6;

export function BrowseSchemesPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [search, setSearch] = useState(searchParams.get('q') || '');
  const [selectedCategory, setSelectedCategory] = useState(searchParams.get('category') || '');
  const [selectedStatus, setSelectedStatus] = useState<string[]>([]);
  const [sortBy, setSortBy] = useState('relevance');
  const [view, setView] = useState<'grid' | 'list'>('grid');
  const [page, setPage] = useState(1);
  const [showMobileFilters, setShowMobileFilters] = useState(false);

  useEffect(() => {
    setSearch(searchParams.get('q') || '');
    setSelectedCategory(searchParams.get('category') || '');
  }, [searchParams]);

  const filteredSchemes = useMemo(() => {
    let result = [...schemes];

    if (search) {
      const q = search.toLowerCase();
      result = result.filter(
        (s) =>
          s.title.toLowerCase().includes(q) ||
          s.description.toLowerCase().includes(q) ||
          s.tags.some((t) => t.toLowerCase().includes(q)) ||
          s.ministry.toLowerCase().includes(q)
      );
    }

    if (selectedCategory) {
      result = result.filter((s) => s.category === selectedCategory);
    }

    if (selectedStatus.length > 0) {
      result = result.filter((s) => selectedStatus.includes(s.status));
    }

    switch (sortBy) {
      case 'title':
        result.sort((a, b) => a.title.localeCompare(b.title));
        break;
      case 'deadline':
        result.sort((a, b) => a.deadline.localeCompare(b.deadline));
        break;
      case 'beneficiaries':
        result.sort((a, b) => b.beneficiaries.localeCompare(a.beneficiaries));
        break;
    }

    return result;
  }, [search, selectedCategory, selectedStatus, sortBy]);

  const totalPages = Math.ceil(filteredSchemes.length / PAGE_SIZE);
  const paginatedSchemes = filteredSchemes.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  useEffect(() => {
    setPage(1);
  }, [search, selectedCategory, selectedStatus, sortBy]);

  const toggleStatus = (status: string) => {
    setSelectedStatus((prev) =>
      prev.includes(status) ? prev.filter((s) => s !== status) : [...prev, status]
    );
  };

  const clearFilters = () => {
    setSearch('');
    setSelectedCategory('');
    setSelectedStatus([]);
    setSortBy('relevance');
    setSearchParams({});
  };

  const activeFilterCount = (search ? 1 : 0) + (selectedCategory ? 1 : 0) + selectedStatus.length;

  return (
    <div className="bg-slate-50 dark:bg-slate-950 min-h-screen">
      <div className="container-page py-6">
        <Breadcrumbs items={[{ label: 'Home', href: '/' }, { label: 'Browse Schemes' }]} />
      </div>

      <div className="container-page pb-6">
        <h1 className="font-heading font-bold text-3xl md:text-4xl text-slate-800 dark:text-slate-100 mb-2">
          Browse Government Schemes
        </h1>
        <p className="text-slate-500 dark:text-slate-400">Discover {schemes.length}+ schemes, scholarships, and subsidies tailored to your needs.</p>
      </div>

      <div className="container-page pb-12">
        <div className="grid lg:grid-cols-[280px_1fr] gap-6">
          {/* Sidebar Filters */}
          <aside className={`${showMobileFilters ? 'block' : 'hidden'} lg:block`}>
            <div className="lg:sticky lg:top-20 space-y-4">
              <Card className="p-5">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-heading font-semibold text-slate-800 dark:text-slate-100 flex items-center gap-2">
                    <SlidersHorizontal className="w-4 h-4" /> Filters
                  </h3>
                  {activeFilterCount > 0 && (
                    <button onClick={clearFilters} className="text-xs text-primary-600 hover:text-primary-700 dark:hover:text-primary-400 font-medium">
                      Clear all
                    </button>
                  )}
                </div>

                <div className="mb-5">
                  <label className="block text-sm font-medium text-slate-700 dark:text-slate-200 mb-2">Category</label>
                  <div className="space-y-1">
                    <button
                      onClick={() => setSelectedCategory('')}
                      className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${
                        !selectedCategory ? 'bg-primary-50 text-primary-700 font-medium' : 'text-slate-600 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800/60'
                      }`}
                    >
                      All Categories
                    </button>
                    {categories.map((cat) => (
                      <button
                        key={cat.id}
                        onClick={() => setSelectedCategory(cat.id)}
                        className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors flex items-center justify-between ${
                          selectedCategory === cat.id ? 'bg-primary-50 text-primary-700 font-medium' : 'text-slate-600 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800/60'
                        }`}
                      >
                        <span>{cat.name}</span>
                        <span className="text-xs text-slate-400 dark:text-slate-500">{cat.schemeCount}</span>
                      </button>
                    ))}
                  </div>
                </div>

                <div className="mb-2">
                  <label className="block text-sm font-medium text-slate-700 dark:text-slate-200 mb-2">Status</label>
                  <div className="space-y-1.5">
                    {statusFilters.map((status) => (
                      <label key={status.value} className="flex items-center gap-2.5 cursor-pointer group">
                        <input
                          type="checkbox"
                          checked={selectedStatus.includes(status.value)}
                          onChange={() => toggleStatus(status.value)}
                          className="w-4 h-4 rounded border-slate-300 text-primary-600 focus:ring-primary-500"
                        />
                        <span className="text-sm text-slate-600 dark:text-slate-200 group-hover:text-slate-800 transition-colors">{status.label}</span>
                      </label>
                    ))}
                  </div>
                </div>
              </Card>
            </div>
          </aside>

          {/* Main Content */}
          <div>
            {/* Search & Sort Bar */}
            <Card className="p-4 mb-5">
              <div className="flex flex-col sm:flex-row gap-3">
                <div className="flex-1">
                  <Input
                    placeholder="Search schemes..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    icon={<Search className="w-4 h-4" />}
                  />
                </div>
                <div className="flex gap-2">
                  <select
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value)}
                    className="px-3 py-2.5 rounded-lg border border-slate-300 bg-white dark:bg-slate-800 dark:text-slate-100 text-sm text-slate-700 dark:text-slate-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 transition-all outline-none"
                  >
                    {sortOptions.map((opt) => (
                      <option key={opt.value} value={opt.value}>{opt.label}</option>
                    ))}
                  </select>
                  <div className="flex rounded-lg border border-slate-300 overflow-hidden">
                    <button
                      onClick={() => setView('grid')}
                      className={`p-2.5 transition-colors ${view === 'grid' ? 'bg-primary-50 text-primary-600' : 'text-slate-400 dark:text-slate-500 hover:bg-slate-50 dark:hover:bg-slate-800/60'}`}
                      aria-label="Grid view"
                    >
                      <Grid3x3 className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => setView('list')}
                      className={`p-2.5 transition-colors ${view === 'list' ? 'bg-primary-50 text-primary-600' : 'text-slate-400 dark:text-slate-500 hover:bg-slate-50 dark:hover:bg-slate-800/60'}`}
                      aria-label="List view"
                    >
                      <List className="w-5 h-5" />
                    </button>
                  </div>
                  <button
                    onClick={() => setShowMobileFilters(!showMobileFilters)}
                    className="lg:hidden p-2.5 rounded-lg border border-slate-300 text-slate-600 dark:text-slate-200 relative"
                    aria-label="Filters"
                  >
                    <SlidersHorizontal className="w-5 h-5" />
                    {activeFilterCount > 0 && (
                      <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-primary-600 text-white text-[10px] font-bold flex items-center justify-center">
                        {activeFilterCount}
                      </span>
                    )}
                  </button>
                </div>
              </div>
            </Card>

            {/* Active Filters */}
            {activeFilterCount > 0 && (
              <div className="flex flex-wrap items-center gap-2 mb-4">
                <span className="text-xs text-slate-500 dark:text-slate-400">Active filters:</span>
                {search && (
                  <Badge variant="primary" className="gap-1">
                    "{search}"
                    <button onClick={() => setSearch('')}><X className="w-3 h-3" /></button>
                  </Badge>
                )}
                {selectedCategory && (
                  <Badge variant="primary" className="gap-1">
                    {categories.find((c) => c.id === selectedCategory)?.name}
                    <button onClick={() => setSelectedCategory('')}><X className="w-3 h-3" /></button>
                  </Badge>
                )}
                {selectedStatus.map((status) => (
                  <Badge key={status} variant="primary" className="gap-1">
                    {status}
                    <button onClick={() => toggleStatus(status)}><X className="w-3 h-3" /></button>
                  </Badge>
                ))}
              </div>
            )}

            {/* Results count */}
            <div className="flex items-center justify-between mb-4">
              <p className="text-sm text-slate-500 dark:text-slate-400">
                Showing <span className="font-medium text-slate-700 dark:text-slate-200">{paginatedSchemes.length}</span> of{' '}
                <span className="font-medium text-slate-700 dark:text-slate-200">{filteredSchemes.length}</span> schemes
              </p>
            </div>

            {/* Scheme Cards */}
            {paginatedSchemes.length > 0 ? (
              <>
                {view === 'grid' ? (
                  <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
                    {paginatedSchemes.map((scheme) => (
                      <SchemeCard key={scheme.id} scheme={scheme} />
                    ))}
                  </div>
                ) : (
                  <div className="space-y-3">
                    {paginatedSchemes.map((scheme) => (
                      <SchemeListCard key={scheme.id} scheme={scheme} />
                    ))}
                  </div>
                )}

                {/* Pagination */}
                {totalPages > 1 && (
                  <div className="flex items-center justify-center gap-2 mt-8">
                    <button
                      onClick={() => setPage((p) => Math.max(1, p - 1))}
                      disabled={page === 1}
                      className="p-2.5 rounded-lg border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800/60 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
                    >
                      <ChevronLeft className="w-5 h-5" />
                    </button>
                    {Array.from({ length: totalPages }, (_, i) => i + 1).map((pageNum) => (
                      <button
                        key={pageNum}
                        onClick={() => setPage(pageNum)}
                        className={`w-10 h-10 rounded-lg text-sm font-medium transition-all ${
                          page === pageNum
                            ? 'bg-primary-600 text-white shadow-soft'
                            : 'border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800/60'
                        }`}
                      >
                        {pageNum}
                      </button>
                    ))}
                    <button
                      onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                      disabled={page === totalPages}
                      className="p-2.5 rounded-lg border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800/60 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
                    >
                      <ChevronRight className="w-5 h-5" />
                    </button>
                  </div>
                )}
              </>
            ) : (
              <Card className="p-12 text-center">
                <div className="w-16 h-16 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center mx-auto mb-4">
                  <Search className="w-8 h-8 text-slate-300" />
                </div>
                <h3 className="font-heading font-semibold text-slate-800 dark:text-slate-100 text-lg mb-2">No schemes found</h3>
                <p className="text-sm text-slate-500 dark:text-slate-400 mb-4">Try adjusting your search or filters to find what you're looking for.</p>
                <Button variant="outline" size="sm" onClick={clearFilters}>Clear all filters</Button>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function SchemeListCard({ scheme }: { scheme: typeof schemes[0] }) {
  const statusConfig = {
    open: { variant: 'success' as const, label: 'Open' },
    upcoming: { variant: 'warning' as const, label: 'Upcoming' },
    closed: { variant: 'error' as const, label: 'Closed' },
  };
  const status = statusConfig[scheme.status];

  return (
    <Card hover className="p-5 group">
      <div className="flex items-start gap-4">
        <div className="flex-1 min-w-0">
          <div className="flex flex-wrap gap-1.5 mb-2">
            <Badge variant={status.variant} dot>{status.label}</Badge>
            <Badge variant="primary">{scheme.tags[0]}</Badge>
          </div>
          <h3 className="font-heading font-semibold text-slate-800 dark:text-slate-100 text-base mb-1 group-hover:text-primary-700 transition-colors">
            {scheme.title}
          </h3>
          <p className="text-sm text-slate-500 dark:text-slate-400 line-clamp-2 mb-3">{scheme.description}</p>
          <div className="flex flex-wrap items-center gap-4 text-xs text-slate-500 dark:text-slate-400">
            <div className="flex items-center gap-1.5">
              <Building2 className="w-3.5 h-3.5 text-slate-400 dark:text-slate-500" /> {scheme.ministry}
            </div>
            <div className="flex items-center gap-1.5">
              <Users className="w-3.5 h-3.5 text-slate-400 dark:text-slate-500" /> {scheme.beneficiaries}
            </div>
            <div className="flex items-center gap-1.5">
              <Calendar className="w-3.5 h-3.5 text-slate-400 dark:text-slate-500" /> {scheme.deadline}
            </div>
          </div>
        </div>
        <div className="flex flex-col items-end gap-2 flex-shrink-0">
          <button className="p-2 rounded-lg text-slate-400 dark:text-slate-500 hover:text-primary-600 hover:bg-primary-50 transition-all">
            <Bookmark className="w-4 h-4" />
          </button>
          <a href={`/schemes/${scheme.id}`} className="text-primary-600 hover:text-primary-700 dark:hover:text-primary-400 text-sm font-medium flex items-center gap-1">
            View <ArrowRight className="w-4 h-4" />
          </a>
        </div>
      </div>
    </Card>
  );
}
