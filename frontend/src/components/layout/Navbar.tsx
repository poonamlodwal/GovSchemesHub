import { useEffect, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Menu, X, Search, Sparkles, User, LayoutDashboard, Sun, Moon } from 'lucide-react';
import { Logo } from './Logo';
import { Button } from '../ui/Button';
import { useTheme } from '../../context/ThemeContext';

const navLinks = [
  { label: 'Home', href: '/' },
  { label: 'Browse Schemes', href: '/schemes' },
  { label: 'Categories', href: '/categories' },
  { label: 'Eligibility Checker', href: '/eligibility' },
  { label: 'About', href: '/about' },
  { label: 'Contact', href: '/contact' },
];

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    setMobileOpen(false);
    setSearchOpen(false);
  }, [location.pathname]);

  const isActive = (href: string) => location.pathname === href;

  return (
    <>
      <header
        className={`fixed top-0 left-0 right-0 z-40 transition-all duration-300 ${
          scrolled
            ? 'bg-white/95 dark:bg-slate-900/95 backdrop-blur-md shadow-card border-b border-slate-200/60 dark:border-slate-800/60'
            : 'bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm'
        }`}
      >
        <div className="container-page">
          <div className="flex h-16 items-center justify-between gap-4">
            <Logo />

            <nav className="hidden lg:flex items-center gap-1">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  to={link.href}
                  className={`px-3.5 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                    isActive(link.href)
                      ? 'text-primary-700 dark:text-primary-400 bg-primary-50 dark:bg-primary-500/10'
                      : 'text-slate-600 dark:text-slate-300 hover:text-primary-700 dark:hover:text-primary-400 hover:bg-slate-50 dark:hover:bg-slate-800/60'
                  }`}
                >
                  {link.label}
                </Link>
              ))}
            </nav>

            <div className="flex items-center gap-2">
              <button
                onClick={toggleTheme}
                className="p-2.5 rounded-lg text-slate-500 dark:text-slate-400 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-slate-50 dark:hover:bg-slate-800/60 transition-all"
                aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
              >
                {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>

              <button
                onClick={() => setSearchOpen(!searchOpen)}
                className="p-2.5 rounded-lg text-slate-500 dark:text-slate-400 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-slate-50 dark:hover:bg-slate-800/60 transition-all"
                aria-label="Search"
              >
                <Search className="w-5 h-5" />
              </button>

              <Link to="/eligibility" className="hidden sm:block">
                <Button size="sm" variant="primary" className="gap-1.5">
                  <Sparkles className="w-4 h-4" />
                  Check Eligibility
                </Button>
              </Link>

              <Link to="/dashboard" className="hidden sm:block">
                <Button size="sm" variant="ghost" className="gap-1.5">
                  <User className="w-4 h-4" />
                  Sign In
                </Button>
              </Link>

              <button
                onClick={() => setMobileOpen(!mobileOpen)}
                className="lg:hidden p-2.5 rounded-lg text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800/60 transition-all"
                aria-label="Menu"
              >
                {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
              </button>
            </div>
          </div>
        </div>

        {searchOpen && (
          <div className="absolute top-full left-0 right-0 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 shadow-card animate-slide-down">
            <div className="container-page py-4">
              <div className="relative max-w-2xl mx-auto">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  autoFocus
                  type="text"
                  placeholder="Search for schemes, scholarships, subsidies..."
                  className="w-full pl-12 pr-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-sm text-slate-800 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 focus:bg-white dark:focus:bg-slate-800 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 dark:focus:ring-primary-500/30 transition-all"
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                      navigate(`/schemes?q=${encodeURIComponent((e.target as HTMLInputElement).value)}`);
                      setSearchOpen(false);
                    }
                  }}
                />
              </div>
              <div className="max-w-2xl mx-auto mt-3 flex flex-wrap gap-2">
                <span className="text-xs text-slate-400 dark:text-slate-500 py-1">Popular:</span>
                {['PM-KISAN', 'Scholarships', 'Ayushman Bharat', 'Housing'].map((tag) => (
                  <button
                    key={tag}
                    onClick={() => {
                      navigate(`/schemes?q=${encodeURIComponent(tag)}`);
                      setSearchOpen(false);
                    }}
                    className="px-2.5 py-1 text-xs rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-primary-50 dark:hover:bg-primary-500/10 hover:text-primary-700 dark:hover:text-primary-400 transition-colors"
                  >
                    {tag}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {mobileOpen && (
          <div className="lg:hidden absolute top-full left-0 right-0 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 shadow-elevated animate-slide-down">
            <nav className="container-page py-4 flex flex-col gap-1">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  to={link.href}
                  className={`px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                    isActive(link.href)
                      ? 'text-primary-700 dark:text-primary-400 bg-primary-50 dark:bg-primary-500/10'
                      : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800/60'
                  }`}
                >
                  {link.label}
                </Link>
              ))}
              <div className="flex gap-2 mt-3 pt-3 border-t border-slate-100 dark:border-slate-800">
                <Link to="/eligibility" className="flex-1">
                  <Button size="sm" fullWidth className="gap-1.5">
                    <Sparkles className="w-4 h-4" />
                    Check Eligibility
                  </Button>
                </Link>
                <Link to="/dashboard" className="flex-1">
                  <Button size="sm" variant="outline" fullWidth className="gap-1.5">
                    <LayoutDashboard className="w-4 h-4" />
                    Dashboard
                  </Button>
                </Link>
              </div>
            </nav>
          </div>
        )}
      </header>
      <div className="h-16" />
    </>
  );
}
