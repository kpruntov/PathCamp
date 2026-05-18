// @trace TASK-042
// @trace TASK-045
import { useState, useEffect } from 'react';

interface Campaign {
  id: number;
  name: string;
  description: string | null;
  party_size: number;
  party_level: number;
  created_at: string;
}

interface CampaignListProps {
  onSelectCampaign: (id: number) => void;
  onCreateNew: () => void;
}

export function CampaignList({ onSelectCampaign, onCreateNew }: CampaignListProps) {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCampaigns = async () => {
      const token = localStorage.getItem('token');
      if (!token) return;

      try {
        const response = await fetch('/campaigns', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          throw new Error('Failed to fetch campaigns');
        }

        const data = await response.json();
        setCampaigns(data);
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchCampaigns();
  }, []);

  const handleDelete = async (e: React.MouseEvent, id: number, name: string) => {
    e.stopPropagation();
    if (!window.confirm(`Are you sure you want to permanently delete campaign "${name}"? This action cannot be undone.`)) {
      return;
    }

    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      const response = await fetch(`/campaigns/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to delete campaign');
      }

      setCampaigns(campaigns.filter(c => c.id !== id));
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (err: any) {
      alert(err.message);
    }
  };

  if (loading) {
    return <div className="text-center text-fantasy-accent animate-pulse">Loading campaigns...</div>;
  }

  if (error) {
    return <div className="text-red-500 text-center">{error}</div>;
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6 border-b border-fantasy-accent/30 pb-4">
        <h2 className="text-2xl font-bold text-fantasy-accent uppercase tracking-wider">Your Campaigns</h2>
        <button
          onClick={onCreateNew}
          className="bg-fantasy-accent text-fantasy-dark font-bold uppercase tracking-wide px-4 py-2 rounded hover:bg-fantasy-text transition-colors text-sm"
        >
          + New Campaign
        </button>
      </div>

      {campaigns.length === 0 ? (
        <div className="text-center p-8 bg-black/40 border border-fantasy-accent/30 rounded text-fantasy-text/60">
          You haven't forged any campaigns yet.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {campaigns.map(campaign => (
            <div 
              key={campaign.id} 
              className="bg-fantasy-dark border border-fantasy-accent/50 p-5 rounded hover:border-fantasy-accent transition-colors cursor-pointer relative group"
              onClick={() => onSelectCampaign(campaign.id)}
            >
              <div className="flex justify-between items-start mb-2">
                <h3 className="text-xl font-bold text-fantasy-text">{campaign.name}</h3>
                <button
                  onClick={(e) => handleDelete(e, campaign.id, campaign.name)}
                  className="text-red-500 hover:text-red-400 bg-red-500/10 hover:bg-red-500/20 px-2 py-1 rounded text-xs opacity-0 group-hover:opacity-100 transition-opacity"
                  title="Delete Campaign"
                >
                  Delete
                </button>
              </div>
              {campaign.description && (
                <p className="text-fantasy-text/80 text-sm mb-4 line-clamp-2">{campaign.description}</p>
              )}
              <div className="flex justify-between text-xs text-fantasy-accent/70 font-bold uppercase tracking-wider mt-auto">
                <span>Party: {campaign.party_size}</span>
                <span>Level: {campaign.party_level}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
