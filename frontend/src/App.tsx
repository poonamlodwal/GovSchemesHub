import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { useEffect } from 'react';
import { ThemeProvider } from './context/ThemeContext';
import { Navbar } from './components/layout/Navbar';
import { Footer } from './components/layout/Footer';
import { ChatAssistant } from './components/ChatAssistant';
import { ToastContainer } from './components/ui/Toast';
import { HomePage } from './pages/HomePage';
import { BrowseSchemesPage } from './pages/BrowseSchemesPage';
import { SchemeDetailsPage } from './pages/SchemeDetailsPage';
import { CategoriesPage } from './pages/CategoriesPage';
import { EligibilityCheckerPage } from './pages/EligibilityCheckerPage';
import { AboutPage } from './pages/AboutPage';
import { ContactPage } from './pages/ContactPage';

function ScrollToTop() {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);
  return null;
}

function App() {
  return (
    <ThemeProvider>
    <BrowserRouter>
      <ScrollToTop />
      <div className="min-h-screen flex flex-col bg-white dark:bg-slate-950 transition-colors duration-300">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/schemes" element={<BrowseSchemesPage />} />
            <Route path="/schemes/:id" element={<SchemeDetailsPage />} />
            <Route path="/categories" element={<CategoriesPage />} />
            <Route path="/eligibility" element={<EligibilityCheckerPage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/contact" element={<ContactPage />} />
            <Route path="/dashboard" element={<HomePage />} />
            <Route path="*" element={<HomePage />} />
          </Routes>
        </main>
        <Footer />
        <ChatAssistant />
        <ToastContainer />
      </div>
    </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
