// @trace TASK-013
// @trace TASK-039
// @trace TASK-040
// @trace TASK-018
// @trace TASK-041
// @trace TASK-042
import { useState, useEffect } from 'react'
import { UserManagement } from './components/UserManagement'
import { AuthForms } from './components/AuthForms'
import { CampaignForm } from './components/CampaignForm'
import { CampaignDashboard } from './components/CampaignDashboard'
import { CampaignList } from './components/CampaignList'
import './App.css'

interface User {
  id: number;
  username: string;
  email: string;
  status: string;
  role: string;
}

function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [user, setUser] = useState<User | null>(null);
  const [activeCampaignId, setActiveCampaignId] = useState<number | null>(null);
  const [isCreatingCampaign, setIsCreatingCampaign] = useState<boolean>(false);

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
      .then(data => setUser(data))
      .catch(() => {
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
        setActiveCampaignId(null);
        setIsCreatingCampaign(false);
      });
    } else {
      localStorage.removeItem('token');
      setUser(null);
      setActiveCampaignId(null);
      setIsCreatingCampaign(false);
    }
  }, [token]);

  const handleLoginSuccess = (newToken: string) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    setActiveCampaignId(null);
    setIsCreatingCampaign(false);
  };

  return (
    <div className="min-h-screen">
      {token && user && (
        <div className="p-4 flex justify-between items-center">
          <div className="text-fantasy-accent font-bold">
            Welcome, {user.username} ({user.role})
          </div>
          <button 
            onClick={handleLogout}
            className="bg-fantasy-dark border border-fantasy-accent text-fantasy-accent px-4 py-2 rounded hover:bg-fantasy-accent hover:text-fantasy-dark transition-colors font-bold uppercase text-sm tracking-wide"
          >
            Logout
          </button>
        </div>
      )}
      
      {!token ? (
        <AuthForms onLoginSuccess={handleLoginSuccess} />
      ) : user?.role === 'Admin' ? (
        <UserManagement />
      ) : user ? (
        activeCampaignId ? (
          <div className="p-8">
            <CampaignDashboard 
              campaignId={activeCampaignId} 
              onBack={() => setActiveCampaignId(null)} 
            />
          </div>
        ) : isCreatingCampaign ? (
          <div className="p-8">
            <button 
              onClick={() => setIsCreatingCampaign(false)}
              className="mb-6 text-fantasy-accent hover:text-fantasy-text transition-colors text-sm uppercase tracking-wider font-bold max-w-md mx-auto block w-full text-left"
            >
              &larr; Back to Campaigns
            </button>
            <CampaignForm onSuccess={(id) => {
              setIsCreatingCampaign(false);
              setActiveCampaignId(id);
            }} />
          </div>
        ) : (
          <div className="p-8">
            <CampaignList 
              onSelectCampaign={(id) => setActiveCampaignId(id)}
              onCreateNew={() => setIsCreatingCampaign(true)}
            />
          </div>
        )
      ) : (
        <div className="p-8 text-center text-fantasy-accent animate-pulse">Loading...</div>
      )}
    </div>
  )
}

export default App
