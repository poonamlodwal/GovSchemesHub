import { Link } from 'react-router-dom';

export function Logo({ className = '', iconOnly = false }: { className?: string; iconOnly?: boolean }) {
  return (
    <Link to="/" className={`flex items-center gap-2.5 group ${className}`}>
      <div className="relative flex-shrink-0">
        <img
          src="/images/AdobeExpressPhotos_d168e8431e2143d387f26b5b622beebb_CopyEdited.png"
          alt="SchemeHub Logo"
          className="w-10 h-10 object-contain transition-transform group-hover:scale-105"
        />
      </div>
      {!iconOnly && (
        <div className="flex flex-col leading-none">
          <span className="font-heading font-bold text-xl text-slate-800 dark:text-white tracking-tight">SchemeHub</span>
          <span className="text-[10px] text-slate-400 dark:text-slate-500 font-medium tracking-wide">Discover Your Eligible Schemes</span>
        </div>
      )}
    </Link>
  );
}
