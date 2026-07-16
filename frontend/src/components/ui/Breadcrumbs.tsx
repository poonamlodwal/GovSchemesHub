import { Link } from 'react-router-dom';

interface BreadcrumbItem {
  label: string;
  href?: string;
}

interface BreadcrumbsProps {
  items: BreadcrumbItem[];
}

export function Breadcrumbs({ items }: BreadcrumbsProps) {
  return (
    <nav aria-label="Breadcrumb" className="flex items-center gap-2 text-sm">
      {items.map((item, index) => (
        <div key={index} className="flex items-center gap-2">
          {index > 0 && <span className="text-slate-300 dark:text-slate-600">/</span>}
          {item.href ? (
            <Link to={item.href} className="text-slate-500 dark:text-slate-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
              {item.label}
            </Link>
          ) : (
            <span className="text-slate-800 dark:text-slate-100 font-medium">{item.label}</span>
          )}
        </div>
      ))}
    </nav>
  );
}
