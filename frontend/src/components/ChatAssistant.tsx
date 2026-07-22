import { useEffect, useRef, useState } from 'react';
import { MessageSquare, X, Send, Sparkles, Bot, User, Paperclip, FileText, Loader2 } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000';

interface Source {
  id: number;
  filename: string;
  doc_type: string;
}

interface Message {
  id: number;
  sender: 'user' | 'bot' | 'system';
  text: string;
  sources?: Source[];
}

const suggestedPrompts = [
  'What schemes am I eligible for?',
  'How do I apply for PM-KISAN?',
  'Find scholarships for students',
  'Health insurance options',
];

export function ChatAssistant() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { id: 0, sender: 'bot', text: 'Namaste! I\'m SchemeHub AI, your guide to government schemes. How can I help you today?' },
  ]);
  const [input, setInput] = useState('');
  const [typing, setTyping] = useState(false);
  const [uploading, setUploading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, typing]);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;
    const file = files[0];

    setUploading(true);
    const uploadMsgId = Date.now();

    // Append system message for upload progress
    setMessages((prev) => [
      ...prev,
      { id: uploadMsgId, sender: 'system', text: `📁 Uploading and indexing "${file.name}"...` }
    ]);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE}/api/upload`, {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === uploadMsgId
              ? { ...msg, text: `✅ "${file.name}" ingested successfully! (${result.chunks_count} chunks added)` }
              : msg
          )
        );
      } else {
        throw new Error(result.error || 'Ingestion failed');
      }
    } catch (error: any) {
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === uploadMsgId
            ? { ...msg, text: `❌ Failed to ingest "${file.name}". Error: ${error.message}` }
            : msg
        )
      );
    } finally {
      setUploading(false);
      if (event.target) event.target.value = ''; // clear input
    }
  };

  const sendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMsg: Message = { id: Date.now(), sender: 'user', text };
    const botMsgId = Date.now() + 1;
    const initialBotMsg: Message = { id: botMsgId, sender: 'bot', text: '' };

    setMessages((prev) => [...prev, userMsg, initialBotMsg]);
    setInput('');
    setTyping(true);

    try {
      const response = await fetch(`${API_BASE}/api/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
           question: text,
           history: messages
            .filter(m => m.sender !== 'system' && m.text)
            .slice(-6)
            .map(m => ({
              role: m.sender === 'user' ? 'user' : 'assistant',
              content: m.text
    }))
}),


      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.error || 'Server error occurred');
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n\n');
          buffer = lines.pop() || '';

          for (const line of lines) {
            if (!line.trim()) continue;

            const eventMatch = line.match(/^event:\s*(.+)$/m);
            const dataMatch = line.match(/^data:\s*(.+)$/m);

            const eventName = eventMatch ? eventMatch[1].trim() : 'message';
            const eventData = dataMatch ? dataMatch[1].trim() : '';

            if (eventName === 'sources') {
              const sourcesList = JSON.parse(eventData);
              setMessages((prev) =>
                prev.map((m) => (m.id === botMsgId ? { ...m, sources: sourcesList } : m))
              );
            } else if (eventName === 'content') {
              const contentObj = JSON.parse(eventData);
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === botMsgId ? { ...m, text: m.text + contentObj.text } : m
                )
              );
            } else if (eventName === 'error') {
              const errorObj = JSON.parse(eventData);
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === botMsgId ? { ...m, text: `❌ Error: ${errorObj.error}` } : m
                )
              );
            }
          }
        }
      }
    } catch (error: any) {
      setMessages((prev) =>
        prev.map((m) =>
          m.id === botMsgId
            ? { ...m, text: `❌ Network connection failed. Please ensure the backend is running. (${error.message})` }
            : m
        )
      );
    } finally {
      setTyping(false);
    }
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

          <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-4 space-y-4 bg-slate-50 dark:bg-slate-950">
            {messages.map((msg) => (
              <div key={msg.id} className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}>
                {msg.sender === 'system' ? (
                  <div className="w-full flex justify-center my-1">
                    <div className="px-3 py-1.5 rounded-lg text-xs bg-slate-200/50 dark:bg-slate-800/50 text-slate-500 dark:text-slate-400 border border-slate-200 dark:border-slate-700 text-center select-none font-medium max-w-[90%]">
                      {msg.text}
                    </div>
                  </div>
                ) : (
                  <div className={`flex gap-2 w-full ${msg.sender === 'user' ? 'justify-end' : ''}`}>
                    {msg.sender === 'bot' && (
                      <div className="w-7 h-7 rounded-full bg-primary-100 dark:bg-primary-500/15 flex items-center justify-center flex-shrink-0">
                        <Bot className="w-4 h-4 text-primary-600 dark:text-primary-400" />
                      </div>
                    )}
                    <div className="max-w-[75%] flex flex-col gap-1">
                      <div
                        className={`px-3.5 py-2.5 rounded-2xl text-sm leading-relaxed ${msg.sender === 'user'
                            ? 'bg-primary-600 text-white rounded-br-md'
                            : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 rounded-bl-md border border-slate-200 dark:border-slate-700 shadow-sm'
                          }`}
                      >
                        {msg.text || (typing && msg.id === messages[messages.length - 1].id ? '...' : '')}
                      </div>

                      {msg.sender === 'bot' && msg.sources && msg.sources.length > 0 && (
                        <div className="flex flex-col gap-1 mt-1 px-1">
                          <span className="text-[10px] font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider select-none">Sources:</span>
                          <div className="flex flex-wrap gap-1">
                            {msg.sources.map((src) => (
                              <div
                                key={src.id}
                                className="flex items-center gap-1 px-2 py-0.5 rounded text-[10px] bg-slate-200/60 dark:bg-slate-800 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700 max-w-[140px] truncate"
                                title={`Document: ${src.filename}`}
                              >
                                <FileText className="w-2.5 h-2.5 text-primary-500 flex-shrink-0" />
                                <span className="truncate">[{src.id}] {src.filename}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                    {msg.sender === 'user' && (
                      <div className="w-7 h-7 rounded-full bg-slate-200 dark:bg-slate-700 flex items-center justify-center flex-shrink-0">
                        <User className="w-4 h-4 text-slate-500 dark:text-slate-400" />
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
            {typing && messages[messages.length - 1].text === '' && (
              <div className="flex gap-2">
                <div className="w-7 h-7 rounded-full bg-primary-100 dark:bg-primary-500/15 flex items-center justify-center flex-shrink-0">
                  <Bot className="w-4 h-4 text-primary-600 dark:text-primary-400" />
                </div>
                <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl rounded-bl-md px-4 py-3 flex gap-1 shadow-sm">
                  <span className="w-2 h-2 rounded-full bg-slate-300 dark:bg-slate-600 animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-2 h-2 rounded-full bg-slate-300 dark:bg-slate-600 animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-2 h-2 rounded-full bg-slate-300 dark:bg-slate-600 animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            )}
          </div>

          {messages.length <= 2 && (
            <div className="px-4 py-2 border-t border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900">
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
            className="flex items-center gap-2 px-3 py-3 border-t border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900"
          >
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileUpload}
              accept=".pdf,.txt,.docx,.xlsx,.xls,.csv"
              className="hidden"
            />
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              disabled={uploading}
              className="w-10 h-10 rounded-full border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 flex items-center justify-center text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200 transition-colors flex-shrink-0 disabled:opacity-50"
              aria-label="Upload document"
            >
              {uploading ? (
                <Loader2 className="w-4 h-4 animate-spin text-primary-600 dark:text-primary-400" />
              ) : (
                <Paperclip className="w-4 h-4" />
              )}
            </button>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={uploading}
              placeholder="Type your message..."
              className="flex-1 px-3.5 py-2.5 rounded-full bg-slate-100 dark:bg-slate-800 text-sm text-slate-800 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 focus:bg-white dark:focus:bg-slate-850 focus:ring-2 focus:ring-primary-200 dark:focus:ring-primary-500/30 transition-all outline-none border border-transparent dark:border-slate-700"
            />
            <button
              type="submit"
              disabled={!input.trim() || uploading}
              className="w-10 h-10 rounded-full bg-primary-600 hover:bg-primary-700 disabled:bg-slate-100 dark:disabled:bg-slate-800 text-white disabled:text-slate-400 flex items-center justify-center transition-all flex-shrink-0 hover:scale-105 active:scale-95"
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

