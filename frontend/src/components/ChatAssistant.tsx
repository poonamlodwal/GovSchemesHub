import { useEffect, useRef, useState } from 'react';
import { MessageSquare, X, Send, Sparkles, Bot, User } from 'lucide-react';

interface Message {
  id: number;
  sender: 'user' | 'bot';
  text: string;
}

const suggestedPrompts = [
  'What schemes am I eligible for?',
  'How do I apply for PM-KISAN?',
  'Find scholarships for students',
  'Health insurance options',
];

const botResponses: Record<string, string> = {
  'What schemes am I eligible for?': 'I can help you find schemes you\'re eligible for! Please use our AI Eligibility Checker — it asks a few quick questions about your age, income, occupation, and location to match you with relevant schemes. Would you like me to redirect you there?',
  'How do I apply for PM-KISAN?': 'To apply for PM-KISAN: 1) Visit the official PM-KISAN portal, 2) Click "New Farmer Registration", 3) Enter your Aadhaar number and verify with OTP, 4) Fill in personal and land details, 5) Submit and save your reference number. You\'ll need your Aadhaar, land records, and bank account details.',
  'Find scholarships for students': 'There are several scholarships available! The National Scholarship Portal (NSP) offers post-matric scholarships for SC/ST/OBC/Minority students. Sukanya Samriddhi Yojana is great for girl children\'s education savings. Would you like to see all education-related schemes?',
  'Health insurance options': 'Ayushman Bharat PMJAY provides ₹5 lakh health cover per family per year — completely free. PMJJBY offers life insurance at just ₹436/year. Would you like to check your eligibility for these schemes?',
};

const defaultResponse = 'I\'m here to help you discover government schemes! You can ask me about specific schemes, eligibility criteria, application processes, or use our AI Eligibility Checker for personalized recommendations. Try one of the suggested prompts below!';

export function ChatAssistant() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { id: 0, sender: 'bot', text: 'Namaste! I\'m SchemeHub AI, your guide to government schemes. How can I help you today?' },
  ]);
  const [input, setInput] = useState('');
  const [typing, setTyping] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, typing]);

  const sendMessage = (text: string) => {
    if (!text.trim()) return;
    const userMsg: Message = { id: Date.now(), sender: 'user', text };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setTyping(true);

    setTimeout(() => {
      const response = botResponses[text] || defaultResponse;
      const botMsg: Message = { id: Date.now() + 1, sender: 'bot', text: response };
      setMessages((prev) => [...prev, botMsg]);
      setTyping(false);
    }, 1200);
  };

  return (
    <>
      {!open && (
        <button
          onClick={() => setOpen(true)}
          className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-primary-600 hover:bg-primary-700 text-white shadow-elevated flex items-center justify-center transition-all hover:scale-105 group"
          aria-label="Open chat assistant"
        >
          <MessageSquare className="w-6 h-6" />
          <span className="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-saffron-500 text-white text-[10px] font-bold flex items-center justify-center ring-2 ring-white">AI</span>
          <span className="absolute inset-0 rounded-full animate-ping bg-primary-400 opacity-20" />
        </button>
      )}

      {open && (
        <div className="fixed bottom-6 right-6 z-50 w-[calc(100vw-3rem)] sm:w-96 h-[500px] max-h-[calc(100vh-3rem)] bg-white dark:bg-slate-900 rounded-2xl shadow-elevated flex flex-col overflow-hidden animate-scale-in border border-slate-200 dark:border-slate-800">
          <div className="flex items-center justify-between px-4 py-3.5 bg-gradient-to-r from-primary-600 to-navy-700 text-white">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-full bg-white/20 flex items-center justify-center">
                <Bot className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-heading font-semibold text-sm">SchemeHub AI Assistant</h3>
                <div className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-success-400 animate-pulse" />
                  <span className="text-xs text-white/80">Online now</span>
                </div>
              </div>
            </div>
            <button onClick={() => setOpen(false)} className="p-1.5 rounded-lg hover:bg-white/10 transition-colors">
              <X className="w-5 h-5" />
            </button>
          </div>

          <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-4 space-y-3 bg-slate-50 dark:bg-slate-950">
            {messages.map((msg) => (
              <div key={msg.id} className={`flex gap-2 ${msg.sender === 'user' ? 'justify-end' : ''}`}>
                {msg.sender === 'bot' && (
                  <div className="w-7 h-7 rounded-full bg-primary-100 dark:bg-primary-500/15 flex items-center justify-center flex-shrink-0">
                    <Bot className="w-4 h-4 text-primary-600 dark:text-primary-400" />
                  </div>
                )}
                <div
                  className={`max-w-[75%] px-3.5 py-2.5 rounded-2xl text-sm leading-relaxed ${
                    msg.sender === 'user'
                      ? 'bg-primary-600 text-white rounded-br-md'
                      : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 rounded-bl-md border border-slate-200 dark:border-slate-700'
                  }`}
                >
                  {msg.text}
                </div>
                {msg.sender === 'user' && (
                  <div className="w-7 h-7 rounded-full bg-slate-200 dark:bg-slate-700 flex items-center justify-center flex-shrink-0">
                    <User className="w-4 h-4 text-slate-500 dark:text-slate-400" />
                  </div>
                )}
              </div>
            ))}
            {typing && (
              <div className="flex gap-2">
                <div className="w-7 h-7 rounded-full bg-primary-100 flex items-center justify-center flex-shrink-0">
                  <Bot className="w-4 h-4 text-primary-600" />
                </div>
                <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl rounded-bl-md px-4 py-3 flex gap-1">
                  <span className="w-2 h-2 rounded-full bg-slate-300 dark:bg-slate-600 animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-2 h-2 rounded-full bg-slate-300 dark:bg-slate-600 animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-2 h-2 rounded-full bg-slate-300 dark:bg-slate-600 animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            )}
          </div>

          {messages.length <= 2 && (
            <div className="px-4 py-2 border-t border-slate-100 dark:border-slate-800">
              <div className="flex items-center gap-1.5 mb-2">
                <Sparkles className="w-3.5 h-3.5 text-saffron-500" />
                <span className="text-xs font-medium text-slate-500 dark:text-slate-400">Suggested prompts</span>
              </div>
              <div className="flex flex-wrap gap-1.5 mb-2">
                {suggestedPrompts.map((prompt) => (
                  <button
                    key={prompt}
                    onClick={() => sendMessage(prompt)}
                    className="px-2.5 py-1.5 text-xs rounded-full bg-primary-50 dark:bg-primary-500/10 text-primary-700 dark:text-primary-300 hover:bg-primary-100 dark:hover:bg-primary-500/20 transition-colors"
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </div>
          )}

          <form
            onSubmit={(e) => {
              e.preventDefault();
              sendMessage(input);
            }}
            className="flex items-center gap-2 px-3 py-3 border-t border-slate-100 bg-white"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 px-3.5 py-2.5 rounded-full bg-slate-100 dark:bg-slate-800 text-sm text-slate-800 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 focus:bg-white dark:focus:bg-slate-800 focus:ring-2 focus:ring-primary-200 dark:focus:ring-primary-500/30 transition-all outline-none"
            />
            <button
              type="submit"
              className="w-10 h-10 rounded-full bg-primary-600 hover:bg-primary-700 text-white flex items-center justify-center transition-colors flex-shrink-0"
              aria-label="Send message"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      )}
    </>
  );
}
