import { Link } from 'react-router-dom';
import { Mail, Phone, MapPin, Twitter, Facebook, Youtube, Linkedin, Send } from 'lucide-react';
import { showToast } from '../ui/Toast';

const footerSections = [
  {
    title: 'About',
    links: [
      { label: 'About SchemeHub', href: '/about' },
      { label: 'Our Mission', href: '/about' },
      { label: 'How It Works', href: '/about' },
      { label: 'Impact', href: '/about' },
      { label: 'Partners', href: '/about' },
    ],
  },
  {
    title: 'Quick Links',
    links: [
      { label: 'Browse Schemes', href: '/schemes' },
      { label: 'Categories', href: '/categories' },
      { label: 'Eligibility Checker', href: '/eligibility' },
      { label: 'Knowledge Base', href: '/about' },
      { label: 'User Dashboard', href: '/dashboard' },
    ],
  },
  {
    title: 'Government Departments',
    links: [
      { label: 'Ministry of Agriculture', href: '/schemes?category=farmers' },
      { label: 'Ministry of Health', href: '/schemes?category=healthcare' },
      { label: 'Ministry of Education', href: '/schemes?category=students' },
      { label: 'Ministry of Finance', href: '/schemes?category=entrepreneurs' },
      { label: 'Ministry of Housing', href: '/schemes?category=housing' },
    ],
  },
  {
    title: 'Help & Support',
    links: [
      { label: 'Contact Us', href: '/contact' },
      { label: 'FAQs', href: '/about' },
      { label: 'Feedback', href: '/contact' },
      { label: 'Privacy Policy', href: '/about' },
      { label: 'Terms of Service', href: '/about' },
    ],
  },
];

const socialLinks = [
  { icon: Twitter, href: '#', label: 'Twitter' },
  { icon: Facebook, href: '#', label: 'Facebook' },
  { icon: Youtube, href: '#', label: 'YouTube' },
  { icon: Linkedin, href: '#', label: 'LinkedIn' },
];

export function Footer() {
  return (
    <footer className="bg-navy-950 text-slate-300 mt-auto">
      <div className="border-b border-white/10">
        <div className="container-page py-12">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-8">
            <div className="lg:col-span-2">
              <Link to="/" className="flex items-center gap-2.5 mb-4">
                <img
                  src="/images/AdobeExpressPhotos_d168e8431e2143d387f26b5b622beebb_CopyEdited.png"
                  alt="SchemeHub Logo"
                  className="w-10 h-10 object-contain"
                />
                <div className="flex flex-col leading-none">
                  <span className="font-heading font-bold text-xl text-white">SchemeHub</span>
                  <span className="text-[10px] text-slate-400 tracking-wide">Discover Your Eligible Schemes</span>
                </div>
              </Link>
              <p className="text-sm text-slate-400 leading-relaxed max-w-xs">
                An AI-powered platform helping Indian citizens discover government schemes, scholarships, and services based on their eligibility.
              </p>
              <div className="mt-5 space-y-2">
                <a href="mailto:hello@schemehub.gov.in" className="flex items-center gap-2 text-sm text-slate-400 hover:text-white transition-colors">
                  <Mail className="w-4 h-4" /> hello@schemehub.gov.in
                </a>
                <a href="tel:1800-XXX-XXXX" className="flex items-center gap-2 text-sm text-slate-400 hover:text-white transition-colors">
                  <Phone className="w-4 h-4" /> 1800-XXX-XXXX (Toll Free)
                </a>
                <div className="flex items-center gap-2 text-sm text-slate-400">
                  <MapPin className="w-4 h-4" /> New Delhi, India
                </div>
              </div>
            </div>

            {footerSections.map((section) => (
              <div key={section.title}>
                <h4 className="font-heading font-semibold text-white text-sm mb-4">{section.title}</h4>
                <ul className="space-y-2.5">
                  {section.links.map((link) => (
                    <li key={link.label}>
                      <Link to={link.href} className="text-sm text-slate-400 hover:text-primary-400 transition-colors">
                        {link.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="container-page py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
          <div>
            <h4 className="font-heading font-semibold text-white text-sm mb-3">Subscribe for Updates</h4>
            <p className="text-sm text-slate-400 mb-3">Get notified about new schemes and deadlines.</p>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                showToast('success', 'Successfully subscribed to updates!');
                (e.target as HTMLFormElement).reset();
              }}
              className="flex gap-2 max-w-sm"
            >
              <input
                type="email"
                required
                placeholder="Enter your email"
                className="flex-1 px-4 py-2.5 rounded-lg bg-white/10 border border-white/20 text-sm text-white placeholder:text-slate-400 focus:bg-white/15 focus:border-primary-400 focus:ring-2 focus:ring-primary-500/30 transition-all"
              />
              <button
                type="submit"
                className="px-4 py-2.5 rounded-lg bg-primary-600 hover:bg-primary-500 text-white transition-colors flex items-center gap-1.5"
                aria-label="Subscribe"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
          </div>

          <div className="flex md:justify-end gap-3">
            {socialLinks.map((social) => (
              <a
                key={social.label}
                href={social.href}
                aria-label={social.label}
                className="w-10 h-10 rounded-lg bg-white/10 hover:bg-primary-600 flex items-center justify-center transition-all hover:scale-105"
              >
                <social.icon className="w-4 h-4 text-white" />
              </a>
            ))}
          </div>
        </div>
      </div>

      <div className="border-t border-white/10">
        <div className="container-page py-5">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-500">
            <p>© 2025 SchemeHub. A Government of India Initiative. All rights reserved.</p>
            <div className="flex items-center gap-4">
              <Link to="/about" className="hover:text-slate-300 transition-colors">Privacy Policy</Link>
              <Link to="/about" className="hover:text-slate-300 transition-colors">Terms</Link>
              <Link to="/about" className="hover:text-slate-300 transition-colors">Accessibility</Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
