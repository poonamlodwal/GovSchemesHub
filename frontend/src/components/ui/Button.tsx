import { forwardRef } from 'react';
import type { ButtonHTMLAttributes, ReactNode } from 'react';

type Variant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'saffron' | 'success' | 'danger';
type Size = 'sm' | 'md' | 'lg';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
  children: ReactNode;
  fullWidth?: boolean;
}

const variantClasses: Record<Variant, string> = {
  primary: 'bg-primary-600 text-white hover:bg-primary-700 shadow-soft',
  secondary: 'bg-navy-800 text-white hover:bg-navy-900 shadow-soft',
  outline: 'border-2 border-primary-600 text-primary-700 dark:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-500/10',
  ghost: 'text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800',
  saffron: 'bg-saffron-500 text-white hover:bg-saffron-600 shadow-soft',
  success: 'bg-success-600 text-white hover:bg-success-700 shadow-soft',
  danger: 'bg-error-500 text-white hover:bg-error-600 shadow-soft',
};

const sizeClasses: Record<Size, string> = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-5 py-2.5 text-sm',
  lg: 'px-7 py-3 text-base',
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'primary', size = 'md', children, fullWidth, className = '', ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={`relative overflow-hidden rounded-lg font-medium transition-all duration-200 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed ${variantClasses[variant]} ${sizeClasses[size]} ${fullWidth ? 'w-full' : ''} ${className}`}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';
