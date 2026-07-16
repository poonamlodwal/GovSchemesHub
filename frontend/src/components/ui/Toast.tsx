import { useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import { CheckCircle, XCircle, Info, AlertTriangle, X } from 'lucide-react';

type ToastType = 'success' | 'error' | 'info' | 'warning';

interface ToastItem {
  id: number;
  type: ToastType;
  message: string;
}

let toastId = 0;
const listeners: ((toast: ToastItem) => void)[] = [];

export function showToast(type: ToastType, message: string) {
  const toast = { id: ++toastId, type, message };
  listeners.forEach((l) => l(toast));
}

const config: Record<ToastType, { icon: ReactNode; bg: string; text: string }> = {
  success: { icon: <CheckCircle className="w-5 h-5" />, bg: 'bg-success-50 border-success-200 dark:bg-success-500/10 dark:border-success-500/30', text: 'text-success-700 dark:text-success-300' },
  error: { icon: <XCircle className="w-5 h-5" />, bg: 'bg-error-50 border-error-200 dark:bg-error-500/10 dark:border-error-500/30', text: 'text-error-700 dark:text-error-300' },
  info: { icon: <Info className="w-5 h-5" />, bg: 'bg-primary-50 border-primary-200 dark:bg-primary-500/10 dark:border-primary-500/30', text: 'text-primary-700 dark:text-primary-300' },
  warning: { icon: <AlertTriangle className="w-5 h-5" />, bg: 'bg-warning-50 border-warning-200 dark:bg-warning-500/10 dark:border-warning-500/30', text: 'text-warning-700 dark:text-warning-300' },
};

export function ToastContainer() {
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  useEffect(() => {
    const listener = (toast: ToastItem) => {
      setToasts((prev) => [...prev, toast]);
      setTimeout(() => {
        setToasts((prev) => prev.filter((t) => t.id !== toast.id));
      }, 4000);
    };
    listeners.push(listener);
    return () => {
      const idx = listeners.indexOf(listener);
      if (idx > -1) listeners.splice(idx, 1);
    };
  }, []);

  return (
    <div className="fixed bottom-6 right-6 z-[60] flex flex-col gap-3 max-w-sm">
      {toasts.map((toast) => {
        const c = config[toast.type];
        return (
          <div
            key={toast.id}
            className={`flex items-center gap-3 px-4 py-3 rounded-xl border shadow-card animate-slide-up ${c.bg} ${c.text}`}
          >
            {c.icon}
            <span className="text-sm font-medium flex-1">{toast.message}</span>
            <button
              onClick={() => setToasts((prev) => prev.filter((t) => t.id !== toast.id))}
              className="opacity-60 hover:opacity-100 transition-opacity"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        );
      })}
    </div>
  );
}
