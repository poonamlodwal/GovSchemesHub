import { useEffect } from 'react';
import type { ReactNode } from 'react';
import { X } from 'lucide-react';

interface ModalProps {
  open: boolean;
  onClose: () => void;
  children: ReactNode;
  title?: string;
  maxWidth?: string;
}

export function Modal({ open, onClose, children, title, maxWidth = 'max-w-md' }: ModalProps) {
  useEffect(() => {
    if (open) {
      document.body.style.overflow = 'hidden';
      const handleEsc = (e: KeyboardEvent) => e.key === 'Escape' && onClose();
      window.addEventListener('keydown', handleEsc);
      return () => {
        document.body.style.overflow = '';
        window.removeEventListener('keydown', handleEsc);
      };
    }
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 animate-fade-in" role="dialog" aria-modal="true">
      <div className="absolute inset-0 bg-slate-900/50 dark:bg-black/70 backdrop-blur-sm" onClick={onClose} />
      <div className={`relative bg-white dark:bg-slate-900 rounded-2xl shadow-elevated w-full ${maxWidth} max-h-[90vh] overflow-y-auto animate-scale-in border border-slate-200 dark:border-slate-800`}>
        {title && (
          <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100 dark:border-slate-800">
            <h3 className="text-lg font-semibold text-slate-800 dark:text-slate-100">{title}</h3>
            <button onClick={onClose} className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors" aria-label="Close">
              <X className="w-5 h-5 text-slate-500 dark:text-slate-400" />
            </button>
          </div>
        )}
        {!title && (
          <button onClick={onClose} className="absolute top-4 right-4 p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors z-10" aria-label="Close">
            <X className="w-5 h-5 text-slate-500 dark:text-slate-400" />
          </button>
        )}
        {children}
      </div>
    </div>
  );
}
