import { useState } from 'react';
import { Mail, Phone, MapPin, Clock, Send, MessageSquare, Building2 } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Card } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { Breadcrumbs } from '../components/ui/Breadcrumbs';
import { showToast } from '../components/ui/Toast';

export function ContactPage() {
  const [form, setForm] = useState({ name: '', email: '', subject: '', message: '', category: 'general' });
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      showToast('success', 'Message sent! We\'ll get back to you within 48 hours.');
      setForm({ name: '', email: '', subject: '', message: '', category: 'general' });
    }, 1500);
  };

  const contactInfo = [
    { icon: Mail, label: 'Email', value: 'hello@schemehub.gov.in', href: 'mailto:hello@schemehub.gov.in' },
    { icon: Phone, label: 'Phone', value: '1800-XXX-XXXX (Toll Free)', href: 'tel:1800XXXXXXX' },
    { icon: MapPin, label: 'Address', value: 'New Delhi, India', href: '#' },
    { icon: Clock, label: 'Hours', value: 'Mon-Sat, 9 AM - 6 PM IST', href: '#' },
  ];

  return (
    <div className="bg-slate-50 dark:bg-slate-950 min-h-screen">
      <div className="container-page py-6">
        <Breadcrumbs items={[{ label: 'Home', href: '/' }, { label: 'Contact' }]} />
      </div>

      <div className="container-page pb-6">
        <Badge variant="primary" className="mb-3">Get in Touch</Badge>
        <h1 className="font-heading font-bold text-3xl md:text-4xl text-slate-800 dark:text-slate-100 mb-2">Contact Us</h1>
        <p className="text-slate-500 dark:text-slate-400 max-w-2xl">Have a question, suggestion, or feedback? We'd love to hear from you. Our team is here to help.</p>
      </div>

      <div className="container-page pb-12">
        <div className="grid lg:grid-cols-[1fr_1.5fr] gap-6">
          {/* Contact Info */}
          <div className="space-y-4">
            <Card className="p-6">
              <h3 className="font-heading font-semibold text-slate-800 dark:text-slate-100 mb-4 flex items-center gap-2">
                <MessageSquare className="w-5 h-5 text-primary-600" /> Contact Information
              </h3>
              <div className="space-y-4">
                {contactInfo.map((info) => (
                  <a
                    key={info.label}
                    href={info.href}
                    className="flex items-start gap-3 p-3 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800/60 transition-colors group"
                  >
                    <div className="w-10 h-10 rounded-lg bg-primary-50 dark:bg-primary-500/10 text-primary-600 flex items-center justify-center flex-shrink-0 group-hover:bg-primary-100 transition-colors">
                      <info.icon className="w-5 h-5" />
                    </div>
                    <div>
                      <div className="text-xs text-slate-400 dark:text-slate-500 mb-0.5">{info.label}</div>
                      <div className="text-sm font-medium text-slate-700 dark:text-slate-200">{info.value}</div>
                    </div>
                  </a>
                ))}
              </div>
            </Card>

            <Card className="p-6">
              <h3 className="font-heading font-semibold text-slate-800 dark:text-slate-100 mb-4 flex items-center gap-2">
                <Building2 className="w-5 h-5 text-primary-600" /> Regional Offices
              </h3>
              <div className="space-y-3">
                {[
                  { city: 'New Delhi', address: 'Central HQ, New Delhi', phone: '+91-11-XXXX-XXXX' },
                  { city: 'Mumbai', address: 'Western Regional Office', phone: '+91-22-XXXX-XXXX' },
                  { city: 'Bengaluru', address: 'Southern Regional Office', phone: '+91-80-XXXX-XXXX' },
                ].map((office) => (
                  <div key={office.city} className="p-3 rounded-lg bg-slate-50 dark:bg-slate-950">
                    <div className="text-sm font-medium text-slate-700 dark:text-slate-200 mb-0.5">{office.city}</div>
                    <div className="text-xs text-slate-500 dark:text-slate-400">{office.address}</div>
                    <div className="text-xs text-slate-400 dark:text-slate-500 mt-1">{office.phone}</div>
                  </div>
                ))}
              </div>
            </Card>

            <Card className="p-6 bg-gradient-to-br from-primary-600 to-navy-800 text-white border-0">
              <h3 className="font-heading font-semibold text-lg mb-2">Need Quick Help?</h3>
              <p className="text-sm text-primary-100 mb-4">Try our AI Chat Assistant — available 24/7 in the bottom right corner.</p>
              <div className="flex items-center gap-2 text-sm">
                <span className="w-2 h-2 rounded-full bg-success-400 animate-pulse" />
                <span className="text-primary-100">AI Assistant is online</span>
              </div>
            </Card>
          </div>

          {/* Contact Form */}
          <Card className="p-8">
            <h3 className="font-heading font-semibold text-xl text-slate-800 dark:text-slate-100 mb-6">Send Us a Message</h3>
            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="grid sm:grid-cols-2 gap-4">
                <Input
                  label="Full Name"
                  required
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  placeholder="Enter your name"
                />
                <Input
                  label="Email Address"
                  type="email"
                  required
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                  placeholder="you@example.com"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-200 mb-1.5">Category</label>
                <div className="flex flex-wrap gap-2">
                  {[
                    { value: 'general', label: 'General Inquiry' },
                    { value: 'feedback', label: 'Feedback' },
                    { value: 'technical', label: 'Technical Issue' },
                    { value: 'scheme', label: 'Scheme Question' },
                  ].map((cat) => (
                    <button
                      key={cat.value}
                      type="button"
                      onClick={() => setForm({ ...form, category: cat.value })}
                      className={`px-3.5 py-2 rounded-lg text-sm font-medium transition-all ${
                        form.category === cat.value
                          ? 'bg-primary-600 text-white'
                          : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200'
                      }`}
                    >
                      {cat.label}
                    </button>
                  ))}
                </div>
              </div>

              <Input
                label="Subject"
                required
                value={form.subject}
                onChange={(e) => setForm({ ...form, subject: e.target.value })}
                placeholder="What is this about?"
              />

              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-200 mb-1.5">Message</label>
                <textarea
                  required
                  rows={5}
                  value={form.message}
                  onChange={(e) => setForm({ ...form, message: e.target.value })}
                  placeholder="Tell us more..."
                  className="w-full rounded-lg border border-slate-300 bg-white dark:bg-slate-800 px-4 py-2.5 text-sm text-slate-800 dark:text-slate-100 placeholder:text-slate-400 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 transition-all outline-none resize-none"
                />
              </div>

              <Button type="submit" disabled={loading} className="gap-2 w-full sm:w-auto">
                {loading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Sending...
                  </>
                ) : (
                  <>
                    <Send className="w-4 h-4" /> Send Message
                  </>
                )}
              </Button>
            </form>
          </Card>
        </div>
      </div>

      {/* Map placeholder */}
      <section className="container-page pb-12">
        <Card className="overflow-hidden">
          <div className="relative h-64 bg-gradient-to-br from-slate-100 to-slate-200 flex items-center justify-center">
            <div className="text-center">
              <MapPin className="w-12 h-12 text-primary-400 mx-auto mb-2" />
              <p className="text-sm text-slate-500 dark:text-slate-400">New Delhi, India</p>
              <p className="text-xs text-slate-400 dark:text-slate-500">Interactive map would appear here</p>
            </div>
            <div className="absolute inset-0 opacity-5" style={{
              backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%231e3a8a' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
            }} />
          </div>
        </Card>
      </section>
    </div>
  );
}
