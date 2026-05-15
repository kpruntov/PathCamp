// @trace TASK-013
// @trace TASK-039
// @trace TASK-040
// @trace TASK-018
// @trace TASK-041
// @trace TASK-042
// @trace TASK-043
import { useState, useEffect } from 'react'
import { UserManagement } from './components/UserManagement'
import { AuthForms } from './components/AuthForms'
import { CampaignForm } from './components/CampaignForm'
import { CampaignDashboard } from './components/CampaignDashboard'
import { CampaignList } from './components/CampaignList'
import { GlobalCampaignList } from './components/GlobalCampaignList'
import './App.css'

interface User {
  id: number;
  username: string;
  email: string;
  status: string;
  role: string;
}

type ViewState = 'global' | 'my_campaigns' | 'create_campaign' | 'admin' | 'auth';

function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [user, setUser] = useState<User | null>(null);
  const [activeCampaignId, setActiveCampaignId] = useState<number | null>(null);
  const [view, setView] = useState<ViewState>('global');

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
      fetch('/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then(res => {
        if (!res.ok) throw new Error('Invalid token');
        return res.json();
      })
      .then(data => {
        setUser(data);
        if (data.role === 'Admin') setView('admin');
      })
      .catch(() => {
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
        setActiveCampaignId(null);
        setView('global');
      });
    } else {
      localStorage.removeItem('token');
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setUser(null);
      setActiveCampaignId(null);
      setView('global');
    }
  }, [token]);

  const handleLoginSuccess = (newToken: string) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
    setView('global');
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    setActiveCampaignId(null);
    setView('global');
  };

  const renderContent = () => {
    if (activeCampaignId) {
      return (
        <div className="p-8">
          <CampaignDashboard 
            campaignId={activeCampaignId} 
            onBack={() => setActiveCampaignId(null)} 
          />
        </div>
      );
    }

    switch (view) {
      case 'auth':
        return <AuthForms onLoginSuccess={handleLoginSuccess} />;
      case 'admin':
        return user?.role === 'Admin' ? <UserManagement /> : <div className="p-8 text-center text-red-500">Access Denied</div>;
      case 'create_campaign':
        return (
          <div className="p-8">
            <button 
              onClick={() => setView('my_campaigns')}
              className="mb-6 text-fantasy-accent hover:text-fantasy-text transition-colors text-sm uppercase tracking-wider font-bold max-w-md mx-auto block w-full text-left"
            >
              &larr; Back to My Campaigns
            </button>
            <CampaignForm onSuccess={(id) => {
              setView('my_campaigns');
              setActiveCampaignId(id);
            }} />
          </div>
        );
      case 'my_campaigns':
        return (
          <div className="p-8">
            <CampaignList 
              onSelectCampaign={(id) => setActiveCampaignId(id)}
              onCreateNew={() => setView('create_campaign')}
            />
          </div>
        );
      case 'global':
      default:
        return (
          <div className="p-8">
            <GlobalCampaignList 
              onSelectCampaign={(id) => setActiveCampaignId(id)}
            />
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen">
      <div className="p-4 flex justify-between items-center border-b border-fantasy-accent/30 bg-fantasy-dark/80">
        <div className="flex gap-6 items-center">
          <button onClick={() => { setActiveCampaignId(null); setView('global'); }} className="text-xl font-bold text-fantasy-accent uppercase tracking-widest">
            Pathcamp
          </button>
          <div className="flex gap-4">
            <button 
              onClick={() => { setActiveCampaignId(null); setView('global'); }}
              className={`text-sm uppercase tracking-wide font-bold transition-colors ${view === 'global' && !activeCampaignId ? 'text-fantasy-text' : 'text-fantasy-accent/60 hover:text-fantasy-accent'}`}
            >
              Global
            </button>
            {user && user.role !== 'Admin' && (
              <button 
                onClick={() => { setActiveCampaignId(null); setView('my_campaigns'); }}
                className={`text-sm uppercase tracking-wide font-bold transition-colors ${view === 'my_campaigns' && !activeCampaignId ? 'text-fantasy-text' : 'text-fantasy-accent/60 hover:text-fantasy-accent'}`}
              >
                My Campaigns
              </button>
            )}
            {user && user.role === 'Admin' && (
              <button 
                onClick={() => { setActiveCampaignId(null); setView('admin'); }}
                className={`text-sm uppercase tracking-wide font-bold transition-colors ${view === 'admin' ? 'text-fantasy-text' : 'text-fantasy-accent/60 hover:text-fantasy-accent'}`}
              >
                Admin
              </button>
            )}
          </div>
        </div>

        <div>
          {token && user ? (
            <div className="flex items-center gap-4">
              <div className="text-fantasy-text/80 text-sm">
                {user.username} ({user.role})
              </div>
              <button 
                onClick={handleLogout}
                className="bg-transparent border border-fantasy-accent text-fantasy-accent px-3 py-1 rounded hover:bg-fantasy-accent hover:text-fantasy-dark transition-colors font-bold uppercase text-xs tracking-wide"
              >
                Logout
              </button>
            </div>
          ) : (
            <button 
              onClick={() => { setActiveCampaignId(null); setView('auth'); }}
              className="bg-fantasy-accent text-fantasy-dark px-4 py-2 rounded hover:bg-fantasy-text transition-colors font-bold uppercase text-sm tracking-wide"
            >
              Login / Register
            </button>
          )}
        </div>
      </div>
      
      {renderContent()}
    </div>
  )
}

export default App