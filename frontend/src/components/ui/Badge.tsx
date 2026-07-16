import type { ReactNode } from 'react';

type Variant = 'primary' | 'success' | 'warning' | 'error' | 'neutral' | 'saffron' | 'navy';
type Size = 'sm' | 'md';

interface BadgeProps {
  variant?: Variant;
  size?: Size;
  children: ReactNode;
  className?: string;
  dot?: boolean;
}

const variantClasses: Record<Variant, string> = {
  primary: 'bg-primary-100 text-primary-700 dark:bg-primary-500/15 dark:text-primary-300',
  success: 'bg-success-100 text-success-700 dark:bg-success-500/15 dark:text-success-300',
  warning: 'bg-warning-100 text-warning-700 dark:bg-warning-500/15 dark:text-warning-300',
  error: 'bg-error-100 text-error-700 dark:bg-error-500/15 dark:text-error-300',
  neutral: 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300',
  saffron: 'bg-saffron-100 text-saffron-700 dark:bg-saffron-500/15 dark:text-saffron-300',
  navy: 'bg-navy-100 text-navy-700 dark:bg-navy-500/15 dark:text-navy-300',
};

const dotClasses: Record<Variant, string> = {
  primary: 'bg-primary-500',
  success: 'bg-success-500',
  warning: 'bg-warning-500',
  error: 'bg-error-500',
  neutral: 'bg-slate-400',
  saffron: 'bg-saffron-500',
  navy: 'bg-navy-500',
};

const sizeClasses: Record<Size, string> = {
  sm: 'px-2 py-0.5 text-xs',
  md: 'px-2.5 py-1 text-xs',
};

export function Badge({ variant = 'neutral', size = 'md', children, className = '', dot = false }: BadgeProps) {
  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full font-medium ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}>
      {dot && <span className={`w-1.5 h-1.5 rounded-full ${dotClasses[variant]}`} />}
      {children}
    </span>
  );
}
